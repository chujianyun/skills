# 嵌入 Web 应用

> 通过 iframe、聊天气泡组件或自定义集成，将已发布的 Web 应用部署到任何网站

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/publish/webapp/embedding-in-websites.md)。

已发布的 Web 应用可直接嵌入任何网站。这不是另一种发布方式：嵌入的仍是你已创建的同一个 Web 应用，只是呈现在你现有的网站中，而不是作为独立页面。

## Web 应用嵌入的工作方式

在 Dify 中发布应用后，你会获得一个 Web 应用 URL。你可直接分享该 URL，也可通过以下方式将同一个应用嵌入你的网站：

> [card] 聊天气泡组件
>
> Web 应用以浮动按钮呈现，访客点击即可打开完整界面

> [card] Iframe 嵌入
>
> Web 应用直接嵌入页面内容，始终可见、随时可用

> [card] JavaScript 控制
>
> 高级嵌入方式，可自定义样式和控制行为

> [card] 响应式设计
>
> 同一个 Web 应用自动适配任何展示形式

> [!NOTE]
>
> 所有嵌入方式使用的都是你已发布的 Web 应用。应用配置的变更会自动应用到所有嵌入位置。

## 聊天气泡组件

聊天气泡将 Web 应用显示为一个浮动按钮。访客点击后，应用以浮层形式打开，无需离开当前页面即可使用 AI 功能。

### 配置选项

聊天气泡可以通过 `difyChatbotConfig` 对象进行自定义：

```javascript theme={null}
window.difyChatbotConfig = {
    // 必需：来自 Dify 的应用令牌
    token: 'YOUR_TOKEN',

    // 可选：环境设置
    isDev: false,
    baseUrl: 'https://udify.app', // 基于 isDev 自动设置

    // 可选：视觉自定义
    containerProps: {
        style: {
            right: '20px',
            bottom: '20px'
        },
        className: 'custom-chat-button'
    },

    // 可选：交互行为
    draggable: false,              // 允许用户拖动按钮
    dragAxis: 'both',             // 'x'、'y' 或 'both'

    // 可选：预填充用户上下文
    inputs: {
        name: "John Doe",          // 来自你的 Dify 应用的变量名
        department: "Support"
    },

    // 可选：用于追踪的系统变量
    systemVariables: {
        user_id: 'USER_123',
        conversation_id: 'CONV_456'
    },

    // 可选：用户个人资料信息
    userVariables: {
        avatar_url: 'https://example.com/avatar.jpg',
        name: 'John Doe'
    }
}
```

**1. 获取你的嵌入令牌**

在你的 Dify 应用中，打开 **访问入口** 标签页，在 **Web 应用** 卡片上点击 **嵌入网站**，找到唯一令牌。

**2. 添加脚本**

在你网站的 HTML 中包含配置和 Dify 的嵌入脚本。

**3. 自定义外观**

调整 `containerProps` 以匹配你网站的设计。

**4. 测试功能**

打开你的网站并尝试聊天按钮，确保一切正常工作。

## Iframe 嵌入

将 Web 应用直接嵌入页面内容，让它成为网站的组成部分：

```html theme={null}
<iframe
  src="https://udify.app/chatbot/YOUR_APP_TOKEN"
  width="100%"
  height="600"
  frameborder="0">
</iframe>
```

### 为什么使用 Iframe 嵌入

* **始终可见**：Web 应用直接可用，不必先点击按钮唤出
* **功能完整**：Web 应用的所有功能在 iframe 中表现一致
* **融入页面**：以页面原生内容呈现，而非浮层
* **配置简单**：只需 HTML，无需 JavaScript 配置

### 自定义选项

**尺寸和位置**：

```html theme={null}
<iframe
  src="https://udify.app/chatbot/YOUR_APP_TOKEN"
  width="400px"
  height="500px"
  style="border: 1px solid #ccc; border-radius: 8px;">
</iframe>
```

**响应式设计**：

```html theme={null}
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
  <iframe
    src="https://udify.app/chatbot/YOUR_APP_TOKEN"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0">
  </iframe>
</div>
```

## 选择嵌入方式

> [accordion] 客户支持应用
>
> **聊天气泡** 最合适：平时不打扰浏览，需要时随时可用。浮动按钮让访客边浏览边快速获取帮助。

> [accordion] 表单和 Workflow 应用
>
> 应用是页面主要内容时，选 **Iframe 嵌入**。访客无需额外点击，直接看到并使用应用。

> [accordion] 产品演示
>
> 在着陆页使用 **Iframe 嵌入**，让访客即刻体验你的 AI 能力，从感兴趣到上手没有任何门槛。

> [accordion] 多页面集成
>
> 希望全站每个页面都能访问同一个应用时，选 **聊天气泡**。一段嵌入代码即可覆盖所有页面。

## 高级配置

你可以使用 CSS 变量或 `containerProps` 选项覆盖默认按钮样式。根据 CSS 特异性应用这些方法以实现你想要的自定义。

### 1. 修改 CSS 变量

支持以下 CSS 变量进行自定义：

```css theme={null}
/* 按钮到底部的距离，默认为 `1rem` */
--dify-chatbot-bubble-button-bottom

/* 按钮到右侧的距离，默认为 `1rem` */
--dify-chatbot-bubble-button-right

/* 按钮到左侧的距离，默认为 `unset` */
--dify-chatbot-bubble-button-left

/* 按钮到顶部的距离，默认为 `unset` */
--dify-chatbot-bubble-button-top

/* 按钮背景颜色，默认为 `#155EEF` */
--dify-chatbot-bubble-button-bg-color

/* 按钮宽度，默认为 `50px` */
--dify-chatbot-bubble-button-width

/* 按钮高度，默认为 `50px` */
--dify-chatbot-bubble-button-height

/* 按钮边框半径，默认为 `25px` */
--dify-chatbot-bubble-button-border-radius

/* 按钮盒阴影，默认为 `rgba(0, 0, 0, 0.2) 0px 4px 8px 0px)` */
--dify-chatbot-bubble-button-box-shadow

/* 按钮悬停变换，默认为 `scale(1.1)` */
--dify-chatbot-bubble-button-hover-transform
```

要将背景颜色更改为 #ABCDEF，添加此 CSS：

```css theme={null}
#dify-chatbot-bubble-button {
    --dify-chatbot-bubble-button-bg-color: #ABCDEF;
}
```

### 2. 使用 `containerProps`

使用 `style` 属性设置内联样式：

```javascript theme={null}
window.difyChatbotConfig = {
    // ... 其他配置
    containerProps: {
        style: {
            backgroundColor: '#ABCDEF',
            width: '60px',
            height: '60px',
            borderRadius: '30px',
        },
        // 对于小的样式覆盖，你也可以为 `style` 属性使用字符串值：
        // style: 'background-color: #ABCDEF; width: 60px;',
    },
}
```

使用 `className` 属性应用 CSS 类：

```javascript theme={null}
window.difyChatbotConfig = {
    // ... 其他配置
    containerProps: {
        className: 'dify-chatbot-bubble-button-custom my-custom-class',
    },
}
```

### 3. 传递 `inputs`

支持四种类型的输入：

1. **`text-input`**：接受任何值。如果输入字符串的长度超过最大允许长度，将被截断。
2. **`paragraph`**：与 `text-input` 类似，接受任何值，如果字符串长度超过最大长度则截断。
3. **`number`**：接受数字或数值字符串。如果提供字符串，将使用 `Number` 函数转换为数字。
4. **`options`**：接受任何值，但需匹配预先配置的选项之一。

示例配置：

```javascript theme={null}
window.difyChatbotConfig = {
    // 其他配置设置...
    inputs: {
        name: 'apple',
    },
}
```

注意：当使用 embed.js 脚本创建 iframe 时，每个输入值都会被处理（使用 GZIP 压缩并进行 base64 编码），然后附加到 URL。

例如，带有处理过的输入值的 URL 将如下所示：
`http://localhost/chatbot/{token}?name=H4sIAKUlmWYA%2FwWAIQ0AAACDsl7gLuiv2PQEUNAuqQUAAAA%3D`

## 故障排除

**组件未显示**：

* 确认应用令牌与应用 **访问入口** 标签页 **嵌入网站** 中显示的一致
* 检查配置是否在嵌入脚本之前加载
* 查看浏览器控制台是否有 JavaScript 错误

**Iframe 无法加载**：

* 确认 Web 应用 URL 中包含正确的令牌
* 确保你的网站允许 iframe 内容（检查 Content Security Policy）
* 你的网站和 Dify 应用都应使用 HTTPS

> [!WARNING]
>
> Web 应用必须先发布才能嵌入。更新应用配置后，需重新发布，变更才会应用到嵌入版本。
