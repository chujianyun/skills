# CoPaw 内置 Skills

## 概述

CoPaw 内置了多个 skills，提供常用功能的封装。这些 skills 位于工作区的 `active_skills/` 目录下，可以自动加载和使用。

## 内置 Skills 列表

### 1. cron - 定时任务管理

**用途**：通过 `copaw cron` 命令管理定时任务

**功能**：
- 创建、查询、暂停、恢复、删除任务
- 支持多 agent（`--agent-id` 参数）
- 支持 text 和 agent 两种任务类型

**常用命令**：
```bash
copaw cron list --agent-id <id>
copaw cron create --agent-id <id> ...
copaw cron state <job_id> --agent-id <id>
copaw cron resume <job_id> --agent-id <id>
copaw cron run <job_id> --agent-id <id>
```

**故障排查**：
1. 检查 jobs.json：`cat ~/.copaw/workspaces/<id>/jobs.json`
2. 检查任务状态：`copaw cron state <job_id> --agent-id <id>`
3. 手动执行测试：`copaw cron run <job_id> --agent-id <id>`

**依赖项**：无

### 2. dingtalk_channel - 钉钉自动连接

**用途**：通过可视化浏览器自动完成钉钉频道接入

**功能**：
- 自动创建钉钉应用
- 自动配置机器人
- 自动发布机器人
- 自动绑定到 CoPaw channel

**使用方式**：
```bash
# 需要可视化浏览器
copaw skills run dingtalk_channel --agent-id <id>
```

**前置条件**：
1. 可视化浏览器模式（`headed: true`）
2. 钉钉开发者后台账号
3. 图片资源（机器人图标、预览图）

**故障排查**：
1. 检查配置：`copaw channels config dingtalk --agent-id <id>`
2. 检查必填字段：`client_id`, `client_secret`, `robot_code`
3. 检查机器人是否发布
4. 检查 Stream 模式配置

**依赖项**：
- 可视化浏览器（Playwright/Puppeteer）
- 网络连接

### 3. docx - Word 文档操作

**用途**：编辑和操作 Word 文档

**功能**：
- 创建、编辑、读取 Word 文档
- 添加评论、修订
- 验证文档格式

**常用脚本**：
```bash
# 接受所有修订
python scripts/accept_changes.py <input.docx>

# 添加评论
python scripts/comment.py <input.docx>

# 验证文档
python scripts/office/validate.py <input.docx>
```

**故障排查**：
1. 检查 Python 依赖：`pip list | grep docx`
2. 检查文件格式：确保是 .docx 格式
3. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：
- python-docx
- lxml

### 4. pptx - PowerPoint 文档操作

**用途**：编辑和操作 PowerPoint 文档

**功能**：
- 创建、编辑、读取 PPT
- 添加幻灯片
- 生成缩略图
- 清理格式

**常用脚本**：
```bash
# 添加幻灯片
python scripts/add_slide.py <input.pptx>

# 清理格式
python scripts/clean.py <input.pptx>

# 生成缩略图
python scripts/thumbnail.py <input.pptx>

# 验证文档
python scripts/office/validate.py <input.pptx>
```

**故障排查**：
1. 检查 Python 依赖：`pip list | grep pptx`
2. 检查文件格式：确保是 .pptx 格式
3. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：
- python-pptx
- lxml
- Pillow（缩略图功能）

### 5. xlsx - Excel 文档操作

**用途**：编辑和操作 Excel 文档

**功能**：
- 创建、编辑、读取 Excel
- 重新计算公式
- 验证文档格式

**常用脚本**：
```bash
# 重新计算公式
python scripts/recalc.py <input.xlsx>

# 验证文档
python scripts/office/validate.py <input.xlsx>
```

**故障排查**：
1. 检查 Python 依赖：`pip list | grep openpyxl`
2. 检查文件格式：确保是 .xlsx 格式
3. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：
- openpyxl
- lxml

### 6. pdf - PDF 文档操作

**用途**：编辑和操作 PDF 文档

**功能**：
- 创建、编辑、读取 PDF
- 填写表单
- 提取表单字段
- 转换为图片

**常用脚本**：
```bash
# 检查表单字段
python scripts/check_fillable_fields.py <input.pdf>

# 提取表单信息
python scripts/extract_form_field_info.py <input.pdf>

# 填写表单
python scripts/fill_fillable_fields.py <input.pdf>

# 转换为图片
python scripts/convert_pdf_to_images.py <input.pdf>
```

**故障排查**：
1. 检查 Python 依赖：`pip list | grep pdf`
2. 检查 PDF 工具：`which pdftotext`
3. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：
- pdfplumber
- PyPDF2
- Pillow

### 7. himalaya - 邮件客户端

**用途**：管理邮件

**功能**：
- 发送、接收邮件
- 管理邮件文件夹
- 搜索邮件

**配置**：
参见 `references/configuration.md`

**故障排查**：
1. 检查邮件配置：`cat ~/.config/himalaya/config.toml`
2. 检查网络连接
3. 检查认证信息

**依赖项**：
- himalaya CLI

### 8. browser_visible - 浏览器可视化

**用途**：控制可视化浏览器

**功能**：
- 打开、关闭浏览器
- 导航网页
- 截图
- 执行脚本

**使用方式**：
```bash
# 启动可视化浏览器
copaw skills run browser_visible --agent-id <id>
```

**故障排查**：
1. 检查浏览器是否安装
2. 检查浏览器驱动（ChromeDriver/GeckoDriver）
3. 检查网络连接

**依赖项**：
- Playwright 或 Puppeteer
- 浏览器（Chrome/Firefox/Safari）

### 9. news - 新闻获取

**用途**：获取新闻信息

**功能**：
- 获取最新新闻
- 分类新闻
- 搜索新闻

**使用方式**：
```bash
# 获取最新新闻
copaw skills run news --agent-id <id>
```

**故障排查**：
1. 检查网络连接
2. 检查新闻源配置
3. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：
- 网络连接
- 新闻源 API（可选）

### 10. file_reader - 文件读取

**用途**：读取各种格式的文件

**功能**：
- 读取文本文件
- 读取二进制文件
- 读取压缩文件

**使用方式**：
```bash
# 读取文件
copaw skills run file_reader --agent-id <id>
```

**故障排查**：
1. 检查文件路径
2. 检查文件权限
3. 检查文件格式

**依赖项**：无

### 11. guidance - 指导

**用途**：提供使用指导和帮助

**功能**：
- 提供命令帮助
- 提供使用指南
- 提供故障排查建议

**使用方式**：
```bash
# 获取指导
copaw skills run guidance --agent-id <id>
```

**故障排查**：
1. 检查 skill 是否加载
2. 查看详细错误：`copaw daemon logs -n 200`

**依赖项**：无

## Skills 故障排查

### 通用排查流程

1. **检查 skill 是否存在**：
   ```bash
   ls ~/.copaw/workspaces/<id>/active_skills/
   ```

2. **检查 skill 配置**：
   ```bash
   cat ~/.copaw/workspaces/<id>/active_skills/<skill>/SKILL.md
   ```

3. **检查依赖项**：
   ```bash
   pip list | grep <dependency>
   ```

4. **查看详细错误**：
   ```bash
   copaw daemon logs -n 200 | grep <skill>
   ```

5. **重新加载 skills**：
   ```bash
   copaw daemon reload-config
   ```

### 常见错误

#### Skill 加载失败

**错误**：
```
Error: Failed to load skill 'xxx'
```

**解决**：
1. 检查 SKILL.md 格式
2. 检查依赖项是否安装
3. 查看详细错误日志

#### 依赖项缺失

**错误**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决**：
```bash
pip install <module>
```

#### 权限问题

**错误**：
```
PermissionError: [Errno 13] Permission denied
```

**解决**：
```bash
chmod +x ~/.copaw/workspaces/<id>/active_skills/<skill>/scripts/*.py
```

#### 网络问题

**错误**：
```
ConnectionError: Unable to connect
```

**解决**：
1. 检查网络连接
2. 检查代理设置
3. 检查防火墙规则

## Skills 管理

### 列出所有 Skills

```bash
# 列出所有内置 skills
copaw skills list --agent-id <id>

# 列出特定 skill 的详细信息
copaw skills config <skill> --agent-id <id>
```

### 禁用 Skill

```bash
# 移动到临时目录
mv ~/.copaw/workspaces/<id>/active_skills/<skill> ~/.copaw/workspaces/<id>/disabled_skills/

# 重新加载配置
copaw daemon reload-config
```

### 启用 Skill

```bash
# 移动回 active_skills 目录
mv ~/.copaw/workspaces/<id>/disabled_skills/<skill> ~/.copaw/workspaces/<id>/active_skills/

# 重新加载配置
copaw daemon reload-config
```

### 更新 Skill

```bash
# 备份旧版本
cp -r ~/.copaw/workspaces/<id>/active_skills/<skill> ~/.copaw/workspaces/<id>/active_skills/<skill>.bak

# 更新代码
cd ~/.copaw/workspaces/<id>/active_skills/<skill>
git pull

# 重新加载配置
copaw daemon reload-config
```

## 自定义 Skills

### 创建自定义 Skill

1. 创建目录：
   ```bash
   mkdir -p ~/.copaw/workspaces/<id>/active_skills/<skill>
   ```

2. 创建 SKILL.md：
   ```markdown
   ---
   name: <skill>
   description: <skill description>
   ---

   # <Skill Name>

   <skill content>
   ```

3. 创建脚本（可选）：
   ```bash
   mkdir -p ~/.copaw/workspaces/<id>/active_skills/<skill>/scripts
   touch ~/.copaw/workspaces/<id>/active_skills/<skill>/scripts/main.py
   ```

4. 重新加载配置：
   ```bash
   copaw daemon reload-config
   ```

### Skill 开发最佳实践

1. **清晰的描述**：在 SKILL.md 中提供清晰的描述
2. **完整的文档**：包含使用说明和故障排查指南
3. **错误处理**：脚本中包含完善的错误处理
4. **依赖管理**：明确列出所有依赖项
5. **版本控制**：使用 Git 管理代码

## 参考资料

- [CoPaw 命令速查](copaw_commands.md)
- [故障恢复策略](copaw_recovery.md)
- [多 Agent 架构](multi_agent.md)
