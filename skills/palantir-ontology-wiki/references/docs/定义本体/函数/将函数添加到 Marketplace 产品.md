:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将函数添加到 Marketplace 产品 \[Beta]

使用 [Foundry DevOps](https://www.palantir.com/docs/foundry/devops/overview/) 将您的函数包含在 [Marketplace 产品](https://www.palantir.com/docs/foundry/devops/core-concepts/#product) 中，以便其他用户安装和重用。[了解如何创建您的第一个产品。](https://www.palantir.com/docs/foundry/foundry-devops/create-products/)

## 支持的功能

DevOps 打包函数供安装和重用，但不提供用户可查看的函数源代码。这意味着安装后，您将能够使用函数，但无法查看函数的源逻辑；随函数附带的存储库将是空的。具有[模型部署](%E6%A8%A1%E5%9E%8B%E4%B8%8A%E7%9A%84%E5%87%BD%E6%95%B0.md)输入的函数即将推出。

## 将函数添加到产品中

要将函数添加到产品中，首先[创建一个产品](https://www.palantir.com/docs/foundry/foundry-devops/create-products/)，然后选择如下所示的 **函数** 内容类型。

[官方图片已失效：添加函数](https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function.png)

然后系统会提示您选择一个函数和一个版本。在大多数情况下，您应选择函数的最新版本。

[官方图片已失效：添加函数](https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function-dialog.png)

虽然您可以直接选择函数，但我们建议先添加像[Workshop 应用程序](https://www.palantir.com/docs/foundry/workshop/marketplace-workshop/)这样的内容，然后通过[依赖面板](https://www.palantir.com/docs/foundry/foundry-devops/create-products/#content)选择相关函数，如下所示。

[官方图片已失效：通过面板添加函数](https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function-panel.png)

## 安装时的函数覆盖

可以通过提供本地定义的函数在安装时修改函数行为的一部分，该函数覆盖随您的 Marketplace 产品一起发布的“静态”函数输入。为此，您可以使用 `@Static` 装饰器指定某个函数可以被覆盖。

例如，考虑一个取反给定数字的函数：

```
// 普通函数

import { Function, Double } from "@foundry/functions-api";

export class MyFunctions {

    @Function() // 标记这是一个函数
    public async modifyNumber(d: Double): Promise<Double> {
        return -d; // 返回负值
    }

}
```

要使此函数可重写，请按如下方式重写：

```typescript
// 可重写的函数

import { Function, Static, Double } from "@foundry/functions-api";

export class MyFunctions {

    @Function()
    public async modifyNumberByStaticFoo(
        n: Double,
        @Static() staticFunctionInput: (num: Double) => Promise<Double> = this.defaultFoo
        ): Promise<Double> {
        // 调用传入的静态函数，默认为 defaultFoo
        return await staticFunctionInput(n);
    }

    private async defaultFoo(n: number) {
        // 默认实现为返回数字的相反数
        return -n;
    }

}
```

以上代码定义了一个可重写的函数 `modifyNumberByStaticFoo`，其中使用了 `@Static` 修饰符允许传入一个静态函数，默认为 `defaultFoo` 函数，作用是返回给定数字的相反数。
在打包一个静态函数时，输入将在安装过程中显示为`staticFunctionInputs`，如下所示。安装者可以提供自己的函数逻辑来覆盖默认行为。从概念上讲，`staticFunctionInputs`作为可覆盖函数的输入参数。

例如，您可能有一个供应链优化函数，其逻辑在另一种情况下需要稍作调整。为此，请在打包之前指定函数是可覆盖的，然后在安装过程中覆盖它。


> 配图缺失说明：本页有 3 个官方图片地址在抓取及重试时失效（返回 HTML 错误页）。下列地址保留用于溯源，未替换成其他版本的图片。

- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function-dialog.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function-panel.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/functions/marketplace-add-function.png>
