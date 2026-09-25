# FAQ 常见问题

本常见问题解答覆盖与 Qoder 相关的常见疑问，包括安装、登录、支持的平台、语言兼容性、数据安全、计费、网络问题与故障排查。

## 快速入门

### 如果 Qoder 一直停在"Qoder starting"，我该怎么办？

请尝试以下步骤：

1. **检查环境**
   - 确保 Qoder 已更新到最新版本
   - 确认操作系统和系统架构支持 Qoder

2. **测试网络连接**
   - 在终端运行以下命令检查连通性：
   ```
   curl https://api1.qoder.sh/algo/api/v1/ping
   ```
   - 如果收到 `pong`，表示网络已连接

3. **清理本地缓存**
   - 结束 Qoder 进程
   - 删除 `.Qoder` 目录
   - 重启 Qoder

## 登录和权限

### 如果登录失败或看到权限被拒绝错误怎么办？

- 过期的登录会话需要重新尝试
- 确保网络允许访问以下域名：
  - api1.qoder.sh
  - api2.qoder.sh
  - api3.qoder.sh

## 支持的平台

- macOS：11.0 及更高版本
- Windows：10/11

## 支持的编程语言

Qoder 支持所有主流语言，并在以下语言上提供增强体验：

- JavaScript、TypeScript、Python、Go、C/C++、C# 和 Java

## 数据安全

### Qoder 会存储我的代码吗？

不会。Qoder 不会存储或分享你的代码。在代码补全过程中会用到代码上下文，但这些内容不会被存储。

### 我可以直接使用 Qoder 生成的代码吗？

Qoder 生成的代码仅作参考，无法保证其可用性。开发者应自行审查并决定是否采用。

## 疑难排查

### 如果我在 Quest Mode 和 Repo Wiki 中遇到"System Error"

请更新至 Qoder v0.2.1 或更高版本。

### CPU 或内存占用过高

- 大型项目在进行代码索引时可能会占用大量资源
- 将不需要索引的文件模式或目录添加到 `.qoderignore`
- 编辑后请重启 Qoder

## 支持

如需更多帮助，请通过 support@qoder.com 与我们联系。
