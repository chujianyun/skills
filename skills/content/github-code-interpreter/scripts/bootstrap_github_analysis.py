#!/usr/bin/env python3
"""
GitHub 源码解读 - 仓库分析和初始化脚本

功能：
1. 解析 GitHub URL
2. 检查仓库是否已在本地
3. 如果不在，提示克隆
4. 创建分析目录
5. 生成仓库结构信息
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime


def parse_github_url(url):
    """解析 GitHub URL，提取 owner 和 repo"""
    patterns = [
        r'github\.com/([^/]+)/([^/]+?)(\.git)?/?$',  # https://github.com/user/repo
        r'github\.com/([^/]+)/([^/]+?)$',             # https://github.com/user/repo
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            groups = match.groups()
            # 处理可能包含 .git 的情况
            owner = groups[0]
            repo = groups[1].replace('.git', '') if len(groups) > 1 else ''
            return owner, repo

    raise ValueError(f"无法解析 GitHub URL: {url}")


def check_repo_exists(github_dir, owner, repo):
    """检查仓库是否已在本地"""
    repo_path = Path(github_dir) / repo
    if repo_path.exists():
        # 检查是否是 git 仓库
        git_dir = repo_path / '.git'
        if git_dir.exists():
            return True, str(repo_path)

    return False, None


def get_repo_info(repo_path):
    """获取仓库基本信息"""
    info = {
        'name': Path(repo_path).name,
        'path': str(repo_path),
        'last_commit': None,
        'branch': None,
        'file_stats': {}
    }

    try:
        # 获取当前分支
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info['branch'] = result.stdout.strip()

        # 获取最后提交时间
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ci'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info['last_commit'] = result.stdout.strip()

    except Exception as e:
        info['error'] = str(e)

    return info


def generate_structure_file(repo_path, output_path, max_depth=3):
    """生成仓库结构文件"""
    try:
        # 排除的目录
        exclude_dirs = {
            'node_modules', 'target', '__pycache__', 'dist', 'build',
            '.git', '.vscode', '.idea', 'vendor', 'venv', 'env'
        }

        result = subprocess.run(
            ['tree', '-L', str(max_depth), '-I',
             ','.join(exclude_dirs), '-a'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            return True
        else:
            # 如果 tree 命令不可用，使用 find 替代
            result = subprocess.run(
                ['find', '.', '-type', 'd', '-maxdepth', str(max_depth),
                 '-not', '-path', '*/.*'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Directory Structure\n\n")
                f.write(result.stdout)
            return True

    except Exception as e:
        print(f"生成结构文件失败: {e}")
        return False


def count_lines_of_code(repo_path):
    """统计代码行数（简单统计）"""
    extensions = {
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.py': 'Python',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
    }

    stats = {}

    try:
        for ext, lang in extensions.items():
            result = subprocess.run(
                ['find', '.', '-name', f'*{ext}', '-type', 'f'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                files = [f for f in result.stdout.strip().split('\n') if f]
                total_lines = 0

                for file in files:
                    try:
                        result = subprocess.run(
                            ['wc', '-l', file],
                            cwd=repo_path,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            lines = int(result.stdout.split()[0])
                            total_lines += lines
                    except:
                        pass

                if total_lines > 0:
                    stats[lang] = {
                        'files': len(files),
                        'lines': total_lines
                    }
    except Exception as e:
        print(f"统计代码行数失败: {e}")

    return stats


def main():
    import sys

    if len(sys.argv) < 3:
        print("用法: python bootstrap_github_analysis.py <github_url> <working_dir>")
        print("示例: python bootstrap_github_analysis.py https://github.com/user/repo ~/Documents/working")
        sys.exit(1)

    github_url = sys.argv[1]
    working_dir = sys.argv[2]

    try:
        # 解析 GitHub URL
        owner, repo = parse_github_url(github_url)
        print(f"✓ 解析 GitHub 仓库: {owner}/{repo}")

        # GitHub 目录
        github_dir = os.path.expanduser('~/Documents/coding/github')

        # 检查仓库是否存在
        exists, repo_path = check_repo_exists(github_dir, owner, repo)

        if exists:
            print(f"✓ 仓库已在本地: {repo_path}")
        else:
            print(f"✗ 仓库不在本地")
            print(f"  请先克隆: git clone https://github.com/{owner}/{repo}.git")
            print(f"  目标目录: {github_dir}/{repo}")
            sys.exit(1)

        # 获取仓库信息
        repo_info = get_repo_info(repo_path)
        print(f"✓ 当前分支: {repo_info.get('branch', 'unknown')}")

        # 创建分析目录
        analysis_dir = Path(working_dir) / 'github-analysis' / repo
        analysis_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建分析目录: {analysis_dir}")

        # 生成结构文件
        structure_file = analysis_dir / 'structure.txt'
        if generate_structure_file(repo_path, structure_file):
            print(f"✓ 生成结构文件: {structure_file}")

        # 统计代码行数
        loc_stats = count_lines_of_code(repo_path)

        # 生成 metadata.json
        metadata = {
            'github_url': github_url,
            'owner': owner,
            'repo': repo,
            'repo_path': repo_path,
            'analysis_dir': str(analysis_dir),
            'branch': repo_info.get('branch'),
            'last_commit': repo_info.get('last_commit'),
            'analysis_date': datetime.now().isoformat(),
            'loc_stats': loc_stats
        }

        metadata_file = analysis_dir / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"✓ 生成元数据文件: {metadata_file}")
        print(f"\n分析目录已创建: {analysis_dir}")
        print(f"开始解读吧！")

        # 输出关键路径（供 AI 读取）
        print(f"\n# OUTPUT_START")
        print(f"repo_dir={repo_path}")
        print(f"analysis_dir={analysis_dir}")
        print(f"metadata_path={metadata_file}")
        print(f"structure_path={structure_file}")
        print(f"report_outline={Path(__file__).parent.parent / 'references' / 'report-outline.md'}")
        print(f"# OUTPUT_END")

    except ValueError as e:
        print(f"✗ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
