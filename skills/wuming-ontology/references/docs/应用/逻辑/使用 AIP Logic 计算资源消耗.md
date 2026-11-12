:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用 AIP Logic 计算资源消耗

AIP Logic 是 Palantir 的一种工具，允许您在通过 Ontology 和计算功能与组织的数据交互时，快速且可维护地搭建 LLM 驱动的流程。AIP Logic 围绕可以线性组合的 LLM 指令的“块”的概念构建，以创建链式思维工作流，可以查询数据、执行操作和函数，并生成新的信息以用于您的应用案例。在 AIP Logic 中，“块”是使用测量的基本单位，尽管每个块可以触发 Foundry 内的其他系统，这些系统也可能使用计算秒来将信息返回给 AIP Logic 块。

:::callout{theme="neutral"}
如果您与 Palantir 签订了企业合同，请在进行计算使用量计算之前联系您的 Palantir 代表。
:::

## 核心概念：资源、块和工具

AIP Logic *资源* 由一个或多个 AIP Logic *块* 组成。运行资源将运行实现所需输出所需的块。块可以使用 *工具*，如 Ontology 查询、函数和操作来生成输出。

## 使用 AIP Logic 测量 Foundry 计算

### AIP LLM 词元

AIP 中的 LLM 词元根据底层模型（如 [OpenAI ↗](https://platform.openai.com/tokenizer)）的方式进行测量，并且取决于提示和响应的大小以及所做提示的数量。有关详细信息，请参阅[各模型类型的使用表](https://www.palantir.com/docs/foundry/resource-management/usage-types/#measuring-compute-with-aip)。

### LLM 块执行

当 AIP Logic 块执行或选择使用工具时，会有一个最低计算秒使用量。

* 基本 LLM 块执行：`4` 计算秒
* LLM 块工具执行：`8` 计算秒

### 额外的 Foundry 计算使用

当 AIP Logic 块将计算委派给外部工具（如 Ontology 查询或函数）时，可能在这些应用执行期间使用额外的计算。

## 管理 AIP Logic 对 Foundry 计算的使用

AIP Logic 中的一些操作会显著影响计算使用量。下面，我们提供了通过仔细控制[词元使用](#token-usage)、[逻辑块执行总数](#total-number-of-logic-block-executions)和[Foundry 计算使用](#foundry-compute)来控制计算使用量的指导。

### 词元使用

* 处理大量文本会显著增加整体计算使用量。注意与 LLM 一起使用的输入提示的大小。这在从 Ontology 中提取大文本块时尤其相关。
* 为了适度使用词元，您应该努力减少注入提示的文本量，并确保提示中只包含相关文本。这在处理大文档时尤为重要。

### 逻辑块执行总数

* 运行许多逻辑块可能会使用大量计算，尤其是在块是通过函数程序触发的（即，不是由人类操作触发的）。
* 为了适度执行逻辑块，考虑将多个块合并为单个提示（在适当的情况下），并且仅在必要时使用额外的块。操作、函数和数据变换块本身不会产生计算使用量。

### Foundry 计算

* 运行许多对 Foundry 应用程序（如 Ontology 查询、函数或操作）的调用可能会使用大量计算。如果逻辑资源需要多次重试，或者每次执行时调用许多函数或操作，则可能会发生这种情况。
* 为了适度使用其他应用程序的计算，请确保您了解在您的逻辑块链中对其他工具的调用次数。可以调用 Foundry 其他部分的潜在工具包括：
  * Ontology 查询
  * 操作执行
  * 函数执行
  * 数据变换

## AIP Logic 计算使用示例

假设用户有一个包含两个 LLM 块的 AIP Logic 资源。其中一个 LLM 块配置了一个操作，并将在执行时调用它。逻辑资源从头到尾运行了两次。

```
Number of LLM blocks: 2
Number of LLM blocks that call actions: 1
Number of runs: 2

1 run compute-seconds = 2 LLM blocks * 4 compute-seconds + 1 action block * 8 compute-seconds
1 run compute-seconds = (2 * 4) + (1 * 8)
1 run compute-seconds = 16 compute-seconds

# 计算一个运行的总计算秒数
# 2 个 LLM 区块，每个占用 4 个计算秒数，加上 1 个 action 区块，占用 8 个计算秒数
# 因此，一个运行需要的计算时间为 (2 * 4) + (1 * 8) = 16 计算秒数

2 runs = 2 * 16 compute-seconds = 32 compute-seconds

# 总共运行 2 次，总计算秒数为 2 * 16 = 32 计算秒数

Total = 32 compute-seconds
```
