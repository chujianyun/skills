#!/usr/bin/env python3
"""Validate a local OWL/Turtle artifact and optionally render an offline HTML view."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def load_rdflib():
    try:
        import rdflib
    except ImportError as exc:
        raise ValueError(
            "缺少 RDFLib；请在独立环境安装：python -m pip install 'rdflib>=7,<8'"
        ) from exc
    if rdflib.__version__.split(".")[0] != "7":
        raise ValueError("需要 RDFLib 7.x；请使用独立环境安装 'rdflib>=7,<8'")
    return rdflib


def build_model(source: Path) -> dict:
    rdf = load_rdflib()
    from rdflib.compare import to_canonical_graph

    RDF, RDFS, OWL = rdf.RDF, rdf.RDFS, rdf.OWL
    raw = source.read_bytes()
    text = raw.decode("utf-8-sig")
    graph = rdf.Graph()
    # A local string + an explicit Turtle parser cannot fetch imports or remote contexts.
    graph.parse(data=text, format="turtle", publicID=source.resolve().as_uri())
    if not graph:
        raise ValueError("本体为空")
    ontologies = sorted(graph.subjects(RDF.type, OWL.Ontology), key=str)
    if not ontologies or not all(isinstance(term, rdf.URIRef) for term in ontologies):
        raise ValueError("交付基线要求命名的 owl:Ontology 声明")
    schema_types = {
        OWL.Class: "类", RDFS.Class: "类", OWL.ObjectProperty: "对象属性",
        OWL.DatatypeProperty: "数据属性", OWL.AnnotationProperty: "注释属性",
        OWL.NamedIndividual: "实例", OWL.Ontology: "本体",
    }
    owl_entities = set().union(*(
        set(graph.subjects(RDF.type, term))
        for term in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty)
    ))
    if not owl_entities:
        raise ValueError("交付基线要求显式声明 OWL 类或属性，不能仅有普通 RDF 实例")

    canonical = to_canonical_graph(graph)
    triples = sorted(canonical, key=lambda row: tuple(term.n3() for term in row))

    def key(term):
        return "_:" + str(term) if isinstance(term, rdf.BNode) else str(term)

    def short(term):
        if isinstance(term, rdf.BNode):
            return key(term)
        try:
            prefix, _, local = graph.compute_qname(term, generate=False)
            return f"{prefix}:{local}"
        except (ValueError, KeyError):
            return str(term)

    def label(term):
        labels = sorted(canonical.objects(term, RDFS.label), key=lambda v: (
            0 if (getattr(v, "language", "") or "").startswith("zh") else 1, v.n3()
        ))
        return str(labels[0]) if labels else short(term)

    # Keep every RDF term, including anonymous expressions and typed/language literals.
    terms = {term for triple in triples for term in triple}
    kinds = {}
    for term in terms:
        if isinstance(term, rdf.Literal):
            kinds[term] = ["值"]
        else:
            kinds[term] = sorted({schema_types[t] for t in canonical.objects(term, RDF.type)
                                  if t in schema_types})
    classes = set(canonical.subjects(RDF.type, OWL.Class)) | set(canonical.subjects(RDF.type, RDFS.Class))
    for subject, _, class_ in canonical.triples((None, RDF.type, None)):
        if class_ in classes and not kinds[subject]:
            kinds[subject] = ["实例"]
    nodes = []
    for term in sorted(terms, key=lambda term: term.n3()):
        is_literal = isinstance(term, rdf.Literal)
        nodes.append({
            "id": key(term) if not is_literal else term.n3(),
            "label": str(term) if is_literal else label(term),
            "short": term.n3() if is_literal else short(term),
            "kinds": kinds[term] or (["匿名表达式"] if isinstance(term, rdf.BNode) else ["资源"]),
            "literal": is_literal,
        })

    def term_id(term):
        return term.n3() if isinstance(term, rdf.Literal) else key(term)

    edges = []
    for child, parent in canonical.subject_objects(RDFS.subClassOf):
        if child in classes and parent in classes and all(isinstance(t, rdf.URIRef) for t in (child, parent)):
            edges.append({"source": key(child), "target": key(parent), "label": "是一种", "property": str(RDFS.subClassOf)})
    for prop in sorted(canonical.subjects(RDF.type, OWL.ObjectProperty), key=str):
        for domain in sorted(canonical.objects(prop, RDFS.domain), key=str):
            for range_ in sorted(canonical.objects(prop, RDFS.range), key=str):
                if domain in classes and range_ in classes and all(isinstance(t, rdf.URIRef) for t in (domain, range_)):
                    edges.append({"source": key(domain), "target": key(range_), "label": label(prop), "property": key(prop)})
    warnings = []
    for term in sorted(owl_entities, key=str):
        if not list(graph.objects(term, RDFS.label)):
            warnings.append(f"实体缺少 rdfs:label：{term}")
    for type_ in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for prop in sorted(graph.subjects(RDF.type, type_), key=str):
            for predicate in (RDFS.domain, RDFS.range):
                if not list(graph.objects(prop, predicate)):
                    warnings.append(f"属性缺少 {short(predicate)}：{prop}")
    for imported in sorted(graph.objects(None, OWL.imports), key=str):
        warnings.append(f"未展开 owl:imports：{imported}")
    defined = set(graph.subjects())
    builtins = (str(RDF), str(RDFS), str(OWL), str(rdf.XSD))
    references = set().union(*(set(graph.objects(None, predicate)) for predicate in (
        RDFS.domain, RDFS.range, RDFS.subClassOf, OWL.inverseOf, OWL.onClass, OWL.onProperty
    )))
    for term in sorted(references, key=str):
        if isinstance(term, rdf.URIRef) and term not in defined and not str(term).startswith(builtins):
            warnings.append(f"外部引用未在当前文件定义：{term}")
    if any(isinstance(term, rdf.URIRef) and str(term).startswith("file:") for term in terms):
        warnings.append("包含本机 file: IRI；新模型请使用绝对业务 IRI，检查是否缺少 @base")
    primary = ontologies[0]
    return {
        "title": label(primary), "ontologies": [str(term) for term in ontologies],
        "namespaces": {prefix: str(uri) for prefix, uri in graph.namespaces()
                       if any(isinstance(term, rdf.URIRef) and str(term).startswith(str(uri)) for term in terms)},
        "source": source.name, "sha256": hashlib.sha256(raw).hexdigest(),
        "counts": {
            "classes": len(classes),
            "objectProperties": len(set(canonical.subjects(RDF.type, OWL.ObjectProperty))),
            "dataProperties": len(set(canonical.subjects(RDF.type, OWL.DatatypeProperty))),
            "individuals": sum("实例" in node["kinds"] for node in nodes),
            "triples": len(canonical),
        },
        "nodes": nodes, "edges": sorted(edges, key=lambda row: tuple(row.values())),
        "triples": [[term_id(term) for term in row] for row in triples],
        "warnings": warnings,
        "validation": "Turtle 解析及基础结构检查通过；未运行 OWL profile 检查、推理器或 Foundry 导入。",
    }


def render_html(model: dict, target: Path, source: Path, overwrite: bool = False):
    if target.resolve() == source.resolve() or (target.exists() and target.samefile(source)):
        raise ValueError("HTML 输出不能覆盖输入 TTL")
    if target.is_symlink():
        raise ValueError("HTML 输出不能写入符号链接；请选择新路径")
    if target.suffix.lower() != ".html":
        raise ValueError("HTML 输出路径必须使用 .html 后缀")
    template = (Path(__file__).resolve().parents[1] / "assets" / "ontology-viewer.html").read_text(encoding="utf-8")
    marker = "__ONTOLOGY_DATA__"
    if template.count(marker) != 1:
        raise ValueError("HTML 模板的数据占位符必须恰好出现一次")
    payload = json.dumps(model, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    rendered = template.replace(marker, payload)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects existing files unless overwrite was explicitly authorized.
    with target.open("w" if overwrite else "x", encoding="utf-8") as handle:
        handle.write(rendered)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ttl", type=Path, help="本地 UTF-8 Turtle 文件")
    parser.add_argument("--html", type=Path, help="可选的独立离线 HTML 路径")
    parser.add_argument("--overwrite", action="store_true", help="仅在已获授权后覆盖既有 HTML")
    args = parser.parse_args(argv)
    try:
        model = build_model(args.ttl)
        if args.html:
            render_html(model, args.html, args.ttl, args.overwrite)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    report = {key: model[key] for key in ("source", "sha256", "ontologies", "namespaces", "counts", "warnings", "validation")}
    if args.html:
        report["html"] = str(args.html)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
