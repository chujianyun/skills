> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置 API Key

> 避免在代码中硬编码密钥

## 前提条件

先[创建 API Key](/api-reference/preparation/api-key)。

## 操作步骤

<Tabs>
  <Tab title="Linux">
    ### 永久环境变量

    为当前用户设置永久环境变量：

    <Steps>
      <Step title="添加环境变量">
        将变量写入 `~/.bashrc`：

        ```bash
        # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
        echo "export DASHSCOPE_API_KEY='REDACTED'" >> ~/.bashrc
        ```

        <Accordion title="手动编辑">
          打开 `~/.bashrc`：

          ```bash
          nano ~/.bashrc
          ```

          在文件中添加以下内容：

          ```bash
          # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
          export DASHSCOPE_API_KEY="REDACTED"
          ```

          在 nano 编辑器中，按 Ctrl+X，然后按 Y，再按 Enter 保存并关闭文件。
        </Accordion>
      </Step>

      <Step title="使变更生效">
        执行以下命令：

        ```bash
        source ~/.bashrc
        ```
      </Step>

      <Step title="验证">
        在新的终端会话中验证：

        ```bash
        echo $DASHSCOPE_API_KEY
        ```
      </Step>
    </Steps>

    ### 临时环境变量

    设置临时变量（仅当前会话有效）：

    <Steps>
      <Step title="设置变量">
        ```bash
        # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
        export DASHSCOPE_API_KEY="REDACTED"
        ```
      </Step>

      <Step title="验证">
        ```bash
        echo $DASHSCOPE_API_KEY
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="macOS">
    ### 永久环境变量

    为当前用户设置永久环境变量：

    <Steps>
      <Step title="查看默认 Shell 类型">
        ```bash
        echo $SHELL
        ```
      </Step>

      <Step title="添加环境变量">
        <Tabs>
          <Tab title="Zsh">
            将变量写入 `~/.zshrc`：

            ```zsh
            # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            echo "export DASHSCOPE_API_KEY='REDACTED'" >> ~/.zshrc
            ```

            <Accordion title="手动编辑">
              打开 `~/.zshrc`：

              ```zsh
              nano ~/.zshrc
              ```

              在文件中添加以下内容：

              ```zsh
              # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
              export DASHSCOPE_API_KEY="REDACTED"
              ```

              在 nano 编辑器中，按 Ctrl+X，然后按 Y，再按 Enter 保存并关闭文件。
            </Accordion>
          </Tab>

          <Tab title="Bash">
            将变量写入 `~/.bash_profile`：

            ```bash
            # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            echo "export DASHSCOPE_API_KEY='REDACTED'" >> ~/.bash_profile
            ```

            <Accordion title="手动编辑">
              打开 `~/.bash_profile`：

              ```bash
              nano ~/.bash_profile
              ```

              在文件中添加以下内容：

              ```bash
              # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
              export DASHSCOPE_API_KEY="REDACTED"
              ```

              在 nano 编辑器中，按 Ctrl+X，然后按 Y，再按 Enter 保存并关闭文件。
            </Accordion>
          </Tab>
        </Tabs>
      </Step>

      <Step title="使变更生效">
        <Tabs>
          <Tab title="Zsh">
            ```zsh
            source ~/.zshrc
            ```
          </Tab>

          <Tab title="Bash">
            ```bash
            source ~/.bash_profile
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="验证">
        在新的终端会话中验证：

        ```bash
        echo $DASHSCOPE_API_KEY
        ```
      </Step>
    </Steps>

    ### 临时环境变量

    设置临时变量（仅当前会话有效）：

    <Steps>
      <Step title="设置变量">
        ```bash
        # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
        export DASHSCOPE_API_KEY="REDACTED"
        ```
      </Step>

      <Step title="验证">
        ```bash
        echo $DASHSCOPE_API_KEY
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Windows">
    可以通过系统属性、CMD 或 PowerShell 设置环境变量。

    <Tabs>
      <Tab title="系统属性">
        <Note>
          - 永久环境变量（需要管理员权限）
          - 仅在新会话中生效——需重启终端、IDE 和应用程序
        </Note>

        <Steps>
          <Step title="打开系统属性">
            按 `Win+Q`，搜索"**编辑系统环境变量**"，打开**系统属性**。
          </Step>

          <Step title="添加环境变量">
            点击**环境变量** > **系统变量** > **新建**。将变量名设为 `DASHSCOPE_API_KEY`，变量值设为您的 API Key。

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/0439247371/p894015.png" alt="系统环境变量对话框" />
          </Step>

          <Step title="确认">
            在三个对话框中依次点击**确定**。
          </Step>

          <Step title="验证">
            在 CMD 或 PowerShell 中验证：

            - CMD：

            ```batch
            echo %DASHSCOPE_API_KEY%
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912522.png" alt="CMD 验证" />

            - Windows PowerShell：

            ```powershell
            echo $env:DASHSCOPE_API_KEY
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912525.png" alt="PowerShell 验证" />
          </Step>
        </Steps>
      </Tab>

      <Tab title="CMD">
        #### 永久环境变量

        <Steps>
          <Step title="设置变量">
            ```batch
            REM 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
            ```
          </Step>

          <Step title="打开新会话">
            打开一个新的 CMD 窗口。
          </Step>

          <Step title="验证">
            ```batch
            echo %DASHSCOPE_API_KEY%
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912522.png" alt="CMD 验证" />
          </Step>
        </Steps>

        #### 临时环境变量

        <Steps>
          <Step title="执行以下命令">
            ```batch
            REM 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
            ```
          </Step>

          <Step title="验证">
            ```batch
            echo %DASHSCOPE_API_KEY%
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912522.png" alt="CMD 验证" />
          </Step>
        </Steps>
      </Tab>

      <Tab title="PowerShell">
        #### 永久环境变量

        <Steps>
          <Step title="设置变量">
            ```powershell
            # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
            ```
          </Step>

          <Step title="打开新会话">
            打开一个新的 PowerShell 窗口。
          </Step>

          <Step title="验证">
            ```powershell
            echo $env:DASHSCOPE_API_KEY
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912525.png" alt="PowerShell 验证" />
          </Step>
        </Steps>

        #### 临时环境变量

        <Steps>
          <Step title="执行以下命令">
            ```powershell
            # 将 YOUR_DASHSCOPE_API_KEY 替换为您的 API Key
            $env:DASHSCOPE_API_KEY = "REDACTED"
            ```
          </Step>

          <Step title="验证">
            ```powershell
            echo $env:DASHSCOPE_API_KEY
            ```

            <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9623589371/p912525.png" alt="PowerShell 验证" />
          </Step>
        </Steps>
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 常见问题

### echo 能输出，但代码提示"未找到 API Key"

常见原因：

- **未设置永久变量**：临时变量仅在当前会话有效，请改用永久环境变量。

- **需要重启**：重启 IDE、终端或应用程序。通过服务管理器托管的应用可能需要重启服务。

- **服务管理器配置**：对于由服务管理器（systemd、supervisord）托管的应用，需要在服务配置文件中添加该环境变量。

- **使用了 sudo**：`sudo` 不会继承环境变量。使用 `sudo -E python xx.py`（`-E` 参数会传递环境变量），或在权限允许时不使用 `sudo`。

- **需要设置 Base URL**：设置千问AI平台的 Base URL：

  - 在代码中设置：

```python
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
```

- 通过环境变量设置：

```bash
export DASHSCOPE_HTTP_BASE_URL='https://dashscope.aliyuncs.com/api/v1'
```
