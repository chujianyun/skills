> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 安装 SDK

> Python、Java、Node.js 和 Go 环境配置

千问AI平台提供 DashScope SDK（Python、Java），同时兼容 OpenAI SDK 调用。OpenAI 提供 Python、Node.js、Java 和 Go SDK。

## 环境准备

如果本地已安装 Python、Java、Node.js 或 Go，可跳过本节。

<Tabs>
  <Tab title="Python">
    ### 检查 Python 版本

    检查 Python 和 pip 是否已安装：

    ```bash
    python -V
    pip --version
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p914717.png" alt="image" />

    <Note>
      需要 Python 3.8 及以上版本。如未安装，请前往 [python.org](https://www.python.org/downloads/) 下载。
    </Note>

    #### `python -V` 或 `pip --version` 提示"command not found"？

    <Tabs>
      <Tab title="Windows">
        1. 安装 Python 并添加到 PATH。参见 [安装 Python](https://www.python.org/downloads/)。<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p917218.png" alt="image" />

        2. 安装 Python 并设置 PATH 后仍报错，请重启终端后重试。
      </Tab>

      <Tab title="Linux and macOS">
        1. 安装 Python。参见 [安装 Python](https://www.python.org/downloads/)。

        2. 如果仍报错，检查 `python` 和 `pip` 是否存在：

           - 输出显示 `/usr/bin/python` 和 `/usr/bin/pip`，重启终端即可。

           - 显示 "no python"，尝试 `which python3 pip3`：

        ```text
        /usr/bin/which: no python in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        /usr/bin/which: no pip in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        ```

        如果找到 `/usr/bin/python3` 和 `/usr/bin/pip3`，请使用 `python3 -V` 和 `pip3 --version`。

        ```text
        /usr/bin/python3
        /usr/bin/pip3
        ```
      </Tab>
    </Tabs>

    ### 配置虚拟环境（可选）

    建议创建虚拟环境来隔离 SDK 依赖。

    1. **创建虚拟环境**

    创建名为 **.venv** 的虚拟环境：

    ```bash
    # 如果命令执行失败，可将 python 替换为 python3 后重试。
    python -m venv .venv
    ```

    2. **激活虚拟环境**

    激活虚拟环境：

    - Windows:

    ```bash
    .venv\Scripts\activate
    ```

    - macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```
  </Tab>

  <Tab title="Java">
    ### 检查 Java 版本

    在终端运行以下命令：

    ```bash
    java -version
    # （可选）如果使用 Maven，检查是否已安装
    mvn --version
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p914723.png" alt="image" />

    <Note>
      需要 Java 8 及以上版本。如未安装，请前往 [Java Downloads](https://www.oracle.com/java/technologies/downloads/) 下载。
    </Note>
  </Tab>

  <Tab title="Node.js">
    ### 检查 Node.js 安装

    检查 Node.js 和 npm 是否已安装：

    ```bash
    node -v
    npm -v
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p914719.png" alt="image" />

    如未安装 Node.js，请前往 [Node.js 官网](https://nodejs.org/en/download/package-manager) 下载。
  </Tab>

  <Tab title="Go">
    ### 检查 Go 版本

    在终端运行以下命令：

    ```bash
    go version
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6146834571/p931008.png" alt="image" />

    如未安装 Go，请前往 [Go 官网](https://go.dev/doc/install) 下载。

    <Note>
      OpenAI Go SDK 需要 Go 1.22 及以上版本。
    </Note>

    ### 创建项目并初始化模块

    创建项目文件夹并初始化模块：

    ```bash
    # 创建项目文件夹（请根据操作系统调整路径和命令）
    mkdir D:\your_project_folder && cd /d D:\your_project_folder

    # 初始化模块。example.com 仅为示例，任意同格式名称均可，无需真实域名。
    go mod init example.com/your_project_folder
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7441934571/p931146.png" alt="image" />
  </Tab>
</Tabs>

## 安装 SDK

<Tabs>
  <Tab title="Python">
    可通过 OpenAI Python SDK 或 DashScope Python SDK 调用千问AI平台 API。

    ### 安装 OpenAI Python SDK

    安装 OpenAI Python SDK：

    ```bash
    # 如果命令执行失败，可将 pip 替换为 pip3 后重试。
    pip install -U openai
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p917092.png" alt="image" />

    安装成功提示：`Successfully installed ... openai-x.x.x`

    ### 安装 DashScope Python SDK

    安装 DashScope Python SDK：

    ```bash
    # 如果命令执行失败，可将 pip 替换为 pip3 后重试。
    pip install -U dashscope
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p917093.png" alt="image" />

    安装成功提示：`Successfully installed ... dashscope-x.x.x`

    <Note>
      pip 版本警告可忽略。
    </Note>
  </Tab>

  <Tab title="Java">
    ### 安装 DashScope Java SDK

    添加 [DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java) 依赖。将 `the-latest-version` 替换为最新版本号。

    #### XML

    1. 打开 Maven 项目的 `pom.xml` 文件。

    2. 在 `<dependencies>` 标签中添加以下依赖：

    ```xml
    <dependency>
      <groupId>com.alibaba</groupId>
      <artifactId>dashscope-sdk-java</artifactId>
      <!-- 将 'the-latest-version' 替换为最新版本号，参见：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
      <version>the-latest-version</version>
    </dependency>
    ```

    3. 保存 `pom.xml` 文件。

    4. 运行 Maven 命令（如 `mvn compile` 或 `mvn clean install`）更新依赖。Maven 会自动下载并添加 DashScope Java SDK 到项目中。

    IntelliJ IDEA 示例：

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p917125.png" alt="image" />

    #### Gradle

    1. 打开 Gradle 项目的 `build.gradle` 文件。

    2. 在 `dependencies` 代码块中添加以下依赖：

    ```groovy
    dependencies {
        // 将 'the-latest-version' 替换为最新版本号，参见：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    }
    ```

    3. 保存 `build.gradle` 文件。

    4. 在项目根目录运行以下命令更新依赖：

    ```bash
    ./gradlew build --refresh-dependencies
    ```

    IntelliJ IDEA 示例：

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9178692471/p917168.png" alt="image" />

    ### 安装 OpenAI Java SDK

    添加 OpenAI Java SDK 依赖。

    #### XML

    1. 打开 Maven 项目的 `pom.xml` 文件。

    2. 在 `<dependencies>` 标签中添加以下依赖（版本 4.30.0+）：

    ```xml
    <dependency>
      <groupId>com.openai</groupId>
      <artifactId>openai-java</artifactId>
      <version>4.30.0</version>
    </dependency>
    ```

    3. 保存 `pom.xml` 文件。

    4. 运行 Maven 命令（如 `mvn compile` 或 `mvn clean install`）更新项目依赖。Maven 会自动下载并添加 OpenAI Java SDK 到项目中。
  </Tab>

  <Tab title="Node.js">
    通过 npm 或 yarn 安装：

    ```bash
    npm install --save openai
    # or
    yarn add openai
    ```

    <Note>
      如果安装失败，配置镜像源：

      ```bash
      npm config set registry https://registry.npmmirror.com/
      ```

      然后重新安装。
    </Note>

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3859299371/p917106.png" alt="image" />

    安装成功提示：`added xx package in xxs`。查看版本：`npm list openai`
  </Tab>

  <Tab title="Go">
    安装 OpenAI Go SDK：

    ```bash
    go get github.com/openai/openai-go/v3@v3.30.0
    ```

    <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7441934571/p931147.png" alt="image" />

    安装成功提示：`go: added github.com/openai/openai-go/v3 v3.30.0`

    <Note>
      - 该 SDK 处于 beta 阶段，`v3.30.0` 版本已通过功能验证。

      - 如果服务器超时，请使用镜像：

      ```bash
      # 设置镜像
      go env -w GOPROXY=https://goproxy.cn,direct
      ```
    </Note>
  </Tab>
</Tabs>

## 后续步骤

运行 OpenAI SDK 或 DashScope SDK 的代码示例。
