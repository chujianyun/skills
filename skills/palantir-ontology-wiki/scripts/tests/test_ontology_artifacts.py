"""Behavior checks for file delivery, graph fidelity, and offline HTML safety."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rdflib import Graph, OWL, RDF


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("ontology_artifacts", ROOT / "scripts/ontology_artifacts.py")
ARTIFACTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARTIFACTS)
PREFIXES = """@prefix ex: <https://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:ontology a owl:Ontology ; rdfs:label "测试"@zh .
"""


class OntologyArtifactsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, content):
        path = self.root / "model.ttl"
        path.write_text(content, encoding="utf-8")
        return path

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = ARTIFACTS.main([str(arg) for arg in args])
        return status, out.getvalue(), err.getvalue()

    def test_example_counts_and_link_direction_match_turtle(self):
        source = ROOT / "assets/example-ontology.ttl"
        model = ARTIFACTS.build_model(source)
        graph = Graph().parse(source, format="turtle")
        self.assertEqual(model["counts"], {"classes": 4, "objectProperties": 3,
                         "dataProperties": 2, "individuals": 3, "triples": len(graph)})
        self.assertEqual(len(model["triples"]), len(graph))
        self.assertFalse(model["warnings"])
        self.assertEqual(len(model["edges"]), 4)
        expected = "https://example.org/ontology/maintenance#"
        self.assertIn({"source": expected + "WorkOrder", "target": expected + "Equipment",
                       "label": "维护设备", "property": expected + "maintains"}, model["edges"])
        self.assertIn([expected + "hasWorkOrder", str(RDF.type), str(OWL.ObjectProperty)], model["triples"])

    def test_anonymous_restrictions_and_literals_are_preserved_deterministically(self):
        source = self.source(PREFIXES + """
ex:Person a owl:Class ; rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty ex:parent ; owl:someValuesFrom ex:Person ] .
ex:parent a owl:ObjectProperty ; rdfs:domain ex:Person ; rdfs:range ex:Person .
ex:age a owl:DatatypeProperty ; rdfs:domain ex:Person ; rdfs:range xsd:integer .
ex:one a ex:Person ; ex:age 12 ; rdfs:label "个体"@zh .
""")
        model = ARTIFACTS.build_model(source)
        again = ARTIFACTS.build_model(source)
        self.assertEqual(model, again)
        self.assertEqual(len(model["triples"]), len(Graph().parse(source, format="turtle")))
        self.assertTrue(any(row[1] == str(OWL.someValuesFrom) for row in model["triples"]))
        self.assertTrue(any('"12"^^' in row[2] for row in model["triples"]))
        self.assertEqual(model["counts"]["individuals"], 1)
        self.assertTrue(any(node["kinds"] == ["匿名表达式"] for node in model["nodes"]))

    def test_html_embeds_exact_graph_and_escapes_script_breakout(self):
        source = self.source(PREFIXES + '''ex:A a owl:Class ; rdfs:label "</script><script>window.pwned=1</script>" .''')
        model = ARTIFACTS.build_model(source)
        output = self.root / "model.html"
        ARTIFACTS.render_html(model, output, source)
        html = output.read_text(encoding="utf-8")
        payload = html.split('<script id="ontology-data" type="application/json">', 1)[1].split("</script>", 1)[0]
        self.assertNotIn("</script>", payload)
        self.assertEqual(json.loads(payload), model)
        self.assertIn("connect-src 'none'", html)
        self.assertNotIn("innerHTML", html)
        self.assertNotIn("<script src=", html)

    def test_existing_output_is_unchanged_without_overwrite(self):
        source = self.source(PREFIXES + "ex:A a owl:Class .")
        output = self.root / "model.html"
        output.write_text("previous", encoding="utf-8")
        status, stdout, stderr = self.run_cli(source, "--html", output)
        self.assertEqual(status, 1)
        self.assertEqual(stdout, "")
        self.assertIn("ERROR", stderr)
        self.assertEqual(output.read_text(), "previous")
        status, _, _ = self.run_cli(source, "--html", output, "--overwrite")
        self.assertEqual(status, 0)
        self.assertIn("<!doctype html>", output.read_text())

    def test_source_and_link_aliases_cannot_be_overwritten(self):
        source = self.source(PREFIXES + "ex:A a owl:Class .")
        before = source.read_bytes()
        alias = self.root / "alias.html"
        alias.symlink_to(source)
        hardlink = self.root / "hardlink.html"
        hardlink.hardlink_to(source)
        for output in (source, alias, hardlink):
            with self.subTest(output=output):
                status, stdout, _ = self.run_cli(source, "--html", output, "--overwrite")
                self.assertEqual(status, 1)
                self.assertEqual(stdout, "")
                self.assertEqual(source.read_bytes(), before)

    def test_invalid_input_never_creates_html_or_success_report(self):
        cases = ("", "not valid turtle", PREFIXES, PREFIXES + "ex:A rdfs:label 'ordinary RDF' .")
        for content in cases:
            with self.subTest(content=content):
                source = self.source(content)
                output = self.root / "output.html"
                status, stdout, stderr = self.run_cli(source, "--html", output)
                self.assertEqual(status, 1)
                self.assertEqual(stdout, "")
                self.assertIn("ERROR", stderr)
                self.assertFalse(output.exists())

    def test_imports_and_external_references_are_reported_without_network(self):
        source = self.source(PREFIXES + """
ex:ontology owl:imports <https://example.invalid/remote> .
ex:A a owl:Class ; rdfs:subClassOf <https://example.invalid/ExternalClass> .
ex:p a owl:ObjectProperty .
""")
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            model = ARTIFACTS.build_model(source)
        warnings = "\n".join(model["warnings"])
        self.assertIn("未展开 owl:imports", warnings)
        self.assertIn("外部引用未在当前文件定义", warnings)
        self.assertIn("属性缺少 rdfs:domain", warnings)
        self.assertIn("属性缺少 rdfs:range", warnings)
        self.assertIn("未运行", model["validation"])

    def test_dependency_failure_is_actionable_and_does_not_create_output(self):
        source = self.source(PREFIXES + "ex:A a owl:Class .")
        output = self.root / "model.html"
        with patch.dict("sys.modules", {"rdflib": None}):
            status, stdout, stderr = self.run_cli(source, "--html", output)
        self.assertEqual(status, 1)
        self.assertEqual(stdout, "")
        self.assertIn("pip install", stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
