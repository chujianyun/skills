#!/bin/bash
# GitHub 源码解读 - 复查脚本
# 用于 1 小时后复查和完善文档

set -e

# 从命令行参数获取分析目录
ANALYSIS_DIR="$1"

if [ -z "$ANALYSIS_DIR" ]; then
    echo "用法: $0 <analysis_dir>"
    echo "示例: $0 ~/Documents/working/github-analysis/some-repo"
    exit 1
fi

if [ ! -d "$ANALYSIS_DIR" ]; then
    echo "错误: 分析目录不存在: $ANALYSIS_DIR"
    exit 1
fi

echo "================================================"
echo "GitHub 源码解读 - 复查任务"
echo "================================================"
echo "分析目录: $ANALYSIS_DIR"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查 metadata.json
METADATA_FILE="$ANALYSIS_DIR/metadata.json"
if [ -f "$METADATA_FILE" ]; then
    echo "✓ 找到元数据文件: $METADATA_FILE"

    # 提取仓库路径
    REPO_PATH=$(grep -o '"repo_path":[[:space:]]*"[^"]*"' "$METADATA_FILE" | cut -d'"' -f4)
    if [ -n "$REPO_PATH" ] && [ -d "$REPO_PATH" ]; then
        echo "✓ 仓库路径: $REPO_PATH"

        # 检查是否有更新
        echo ""
        echo "检查仓库更新..."
        cd "$REPO_PATH"
        git fetch origin > /dev/null 2>&1

        LOCAL_COMMIT=$(git rev-parse HEAD)
        REMOTE_COMMIT=$(git rev-parse @{u} 2>/dev/null || echo "none")

        if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ] && [ "$REMOTE_COMMIT" != "none" ]; then
            echo "⚠ 仓库有更新，建议拉取最新代码"
            echo "  本地: $LOCAL_COMMIT"
            echo "  远程: $REMOTE_COMMIT"
        else
            echo "✓ 仓库已是最新"
        fi
    fi
fi

# 检查文档文件
echo ""
echo "检查文档文件..."

REPORT_FILE=$(find "$ANALYSIS_DIR" -maxdepth 1 -name "*_源码解读.md" | head -1)
QUICKSTART_FILE=$(find "$ANALYSIS_DIR" -maxdepth 1 -name "*_快速上手.md" | head -1)

if [ -n "$REPORT_FILE" ]; then
    echo "✓ 找到解读报告: $REPORT_FILE"
    LINES=$(wc -l < "$REPORT_FILE")
    echo "  当前行数: $LINES"
else
    echo "⚠ 未找到解读报告（*_源码解读.md）"
fi

if [ -n "$QUICKSTART_FILE" ]; then
    echo "✓ 找到快速上手文档: $QUICKSTART_FILE"
    LINES=$(wc -l < "$QUICKSTART_FILE")
    echo "  当前行数: $LINES"
else
    echo "⚠ 未找到快速上手文档（*_快速上手.md）"
fi

echo ""
echo "================================================"
echo "复查任务清单"
echo "================================================"
echo ""
echo "请按以下顺序进行复查："
echo ""
echo "1. 读取当前的解读报告和快速上手文档"
echo "2. 重新审视仓库结构（structure.txt）"
echo "3. 补充遗漏的内容："
echo "   - 调用 mermaid skill 生成架构图或流程图"
echo "   - 关键模块的详细说明"
echo "   - 使用场景的补充"
echo "   - 设计思想的深入分析"
echo "   - 对悟鸣的启发（结合岗位和研究）"
echo "4. 检查快速上手文档的准确性"
echo "5. 在文档末尾添加/更新复查记录"
echo ""
echo "复查记录格式："
echo '### YYYY-MM-DD 复查 N'
echo '- 补充了 xxx'
echo '- 修正了 xxx'
echo '- 优化了 xxx'
echo ""
echo "================================================"
echo "复查准备完成，可以开始完善文档了！"
echo "================================================"
