:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从Python函数进行API调用

可以从Python函数进行API调用到外部来源，但这样做需要额外的配置。下面详细介绍了此配置和外部来源的使用。

## 配置对外部API的访问

默认情况下，Python函数不允许调用外部API。要启用从Python函数调用外部系统，必须在[数据连接](https://www.palantir.com/docs/foundry/data-connection/overview/)中[配置一个来源](https://www.palantir.com/docs/foundry/data-connection/set-up-source/)，以允许Foundry连接到外部系统。

为使Python函数安全地连接到来源的外部系统，必须配置来源以[启用导出](https://www.palantir.com/docs/foundry/data-connection/export-overview/#enable-exports-for-source)并允许[将来源导入代码库](https://www.palantir.com/docs/foundry/data-integration/external-transforms-source-based/#prerequisite-import-a-source-into-code)。这两项都可以通过导航到数据连接中的来源并打开**连接设置**部分进行配置。在这里，您会找到**代码导入配置**选项卡，如果来源尚未拥有API名称，也可以在此配置API名称。此API名称将在代码中用于引用您的来源。

## 在函数中使用外部来源

:::callout{theme="neutral"}
目前无法从Python函数访问存储在来源中的密钥和凭证。
:::

要从Python函数进行API调用，首先必须在Python函数库中使用[资源导入侧边栏](../%E5%B0%86%E8%B5%84%E6%BA%90%E5%AF%BC%E5%85%A5%E4%BB%A3%E7%A0%81%E5%BA%93.md)导入您的来源。导入后，通过将来源的API名称添加到`@function`装饰器的`sources`参数中，授予函数对来源的访问权限。
在函数装饰器中导入并声明来源后，您可以对该来源所代表的系统进行外部API调用。
下面显示了一个示例：

```python
@function(sources=["<SOURCE API NAME>"])
def my_external_function(name: str) -> str:
    # 发送GET请求到指定的API URL，并获取响应文本
    response_string = requests.get('https://<API URL>').text
    return response_string  # 返回响应的文本内容
```

在[发布您的函数](%E8%B5%B7%E5%A7%8B%E6%AD%A5%E9%AA%A4.md#commit-and-publish-your-function)后，您可以在[Pipeline Builder](%E5%9C%A8Pipeline%20Builder%E4%B8%AD%E4%BD%BF%E7%94%A8Python%E5%87%BD%E6%95%B0.md)和[Workshop](%E5%9C%A8Workshop%E4%B8%AD%E4%BD%BF%E7%94%A8Python%E5%87%BD%E6%95%B0.md)中使用它进行外部调用。

:::callout{theme="warning"}
目前无法在函数实时预览中进行API调用，您需要发布函数以进行测试。
:::
