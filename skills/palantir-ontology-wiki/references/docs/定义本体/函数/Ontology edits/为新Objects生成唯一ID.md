:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 为新Objects生成唯一ID

在编写创建Objects的[Ontology编辑函数](%E6%A6%82%E8%BF%B0.md)时，您可能需要为新创建的Object生成一个唯一ID。您可以通过使用`@foundry/functions-utils`包在函数中设置这一点，以生成全局唯一标识符。

## 导入包

默认情况下，`@foundry/functions-utils`包已安装，但如果`package.json`文件中不存在该包：

* 在`"dependencies"`部分添加`"@foundry/functions-utils": "0.1.0"`

如[添加依赖项的文档](../TypeScript%20basics/%E6%B7%BB%E5%8A%A0%20npm%20%E4%BE%9D%E8%B5%96%E9%A1%B9.md#adding-dependencies)中所述，请记得重启Code Assist以使新包可用于自动补全。

## 在代码中使用包

要生成唯一ID，您可以使用`@foundry/functions-utils`包中的`Uuid.random()`工具函数。下面的代码示例展示了如何在一个示例Ontology编辑函数中使用`random`函数。

```typescript
import { OntologyEditFunction, Timestamp } from "@foundry/functions-api";
import { Objects } from "@foundry/ontology-api";
import { Uuid } from "@foundry/functions-utils";

// 定义一个类 ExampleEditFunctions，用于处理与飞行场景相关的编辑功能
export class ExampleEditFunctions {
    // 使用装饰器声明该方法是一个编辑飞行场景的函数
    @Edits(FlightScenario)
    @OntologyEditFunction()
    public createFlightScenario(): void {
        // 创建一个新的飞行场景对象
        const scenario = Objects.create().flightScenarios(Uuid.random());
        // 设置飞行场景的名称
        scenario.scenarioName = "New scenario";
        // 设置飞行场景的创建时间为当前时间
        scenario.creationTime = Timestamp.now();
    }
}
```
