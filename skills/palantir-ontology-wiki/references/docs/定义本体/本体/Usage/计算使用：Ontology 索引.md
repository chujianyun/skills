:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 计算使用：Ontology 索引

Foundry 的 Ontology 将对象存储在 Ontology 索引中，这是一种为快速访问而优化的存储格式。Foundry 数据集中的数据可以是任意大小或格式，这意味着需要进行数据变换以准备数据集数据以存储在 Ontology 索引中。这个过程称为*Ontology 索引*，可以应用于任意大小的数据集和对象。Ontology 索引的处理成本以计算秒来衡量。本文件描述了 Ontology 索引如何使用计算资源以及如何管理计算使用。

## 衡量 Ontology 索引的计算使用

Ontology 索引使用并行化的 Spark 后端读取任意大小的数据集并将其转变为 Ontology 格式。运行索引任务所使用的计算量基于计算资源（驱动程序和执行器）的数量以及索引任务本身的总墙钟时间。

有关 Spark 使用如何转换为计算秒的更多信息，请参阅主要[使用类型](https://www.palantir.com/docs/foundry/resource-management/usage-types/)文档。您可以在下面找到[Ontology 索引使用的计算秒计算示例](#example-indexing-compute-calculation)。

## 调查 Ontology 索引的使用情况

Ontology 索引任务在 Foundry 的搭建应用中展示，并附加到正在索引的对象上。Ontology 索引任务是 Spark 任务，因此被分类为并行化批处理计算；因此，Ontology 索引任务可以像同一后端上的其他任务一样进行测量，例如代码库变换和 Contour 查询。

索引任务可以根据其触发方式进行分类。

* *Ontology 索引任务* 将数据集索引到 Ontology 后端。此计算用于从数据集中生成已索引的对象。
* *Ontology 导出任务* 将在 Ontology 中直接进行的编辑保留到 Foundry 变换框架中的数据集。这些任务通常比完整索引任务要小，因为 Ontology 导出任务通常处理的是编辑，这些编辑是总对象集的严格子集。

## Ontology 索引使用的驱动因素

Ontology 索引任务必须读取所有需要索引的数据并将其转变为 Ontology 后端可以快速存储、搜索和编辑的格式。

读取和索引数据时的计算使用由以下因素驱动：

* **每个 Object 的记录数量**
  * 随着被索引数据集中的记录数量的增加，Object 的数量也会增加。每个 Object 需要一定数量的计算操作来进行索引，因此增加 Object 的数量会增加用于索引的计算量。
* **每个 Object 的属性数量**
  * 索引任务必须单独分析每个 Object 的每个属性，然后将其写入 Object 索引。如果有更多的属性需要分析和索引，则会使用更多的计算。
* **每个属性的大小**
  * 一些属性比其他属性大得多。例如，包含大量内容的文本属性将需要更多的空间和计算来分析，而不是简单的数字属性。具有更大、更复杂属性类型的 Object 将需要更多的计算来进行索引。

索引频率在 Ontology 更新所使用的计算量中也起着重要作用。上游数据集上设置的计划将触发对象的自动重索引。在检查保持对象最新的使用影响时，请考虑该对象及其上游数据集的更新计划。

## 管理 Ontology 索引计算

可以通过优化 Ontology 索引任务来减少计算使用。第一个也是最简单的优化方法是减少索引输入数据的大小，这会减少完成任务所需的工作量。这包括在可能的情况下执行以下操作：

* 管理输入记录的数量
* 管理每个 Object 的属性数量
* 管理每个 Object 每个属性的大小

另一种优化方法是配置 Ontology 索引任务以使用变更日志策略进行索引。通过在执行之前将任务与现有对象进行比较，变更日志索引显著减少了每个索引任务需要创建或更新的对象数量。变更日志索引需要更多的配置和更新策略的遵循，但可以带来数量级的性能和效率提升。

## 索引计算计算示例

索引任务以并行化 Spark 任务的形式出现，可以在搭建应用中看到。请参阅以下索引任务示例。请注意，Ontology 索引任务将根据任务的大小自动选择索引任务的驱动程序和执行器的大小。

```markdown
Driver:
    num_vcpu: 1
    GiB_RAM: 6
Executors:
    num_vcpu: 1
    GiB_RAM: 4
    num_executors: 2
Total Runtime: 10 seconds

Calculation:

driver_compute_seconds = max(num_vcpu, GiB_RAM / 7.5) * runtime_in_seconds
                       = max(1vcpu, 6GiB / 7.5) * 10sec
                       = 1 * 10 = 10 compute-seconds
                       # 驱动器计算秒数 = max(虚拟CPU数量, 内存大小/7.5) * 运行时间（秒）
                       #            = max(1虚拟CPU, 6GiB / 7.5) * 10秒
                       #            = 1 * 10 = 10 计算秒数

executor_compute_seconds = max(num_vcpu, GiB_RAM / 7.5) * num_executors * runtime_in_seconds
                         = max(1vcpu, 4GiB / 7.5) * 2executors * 10sec
                         = 1 * 2 * 10 = 20 compute-seconds
                         # 执行器计算秒数 = max(虚拟CPU数量, 内存大小/7.5) * 执行器数量 * 运行时间（秒）
                         #              = max(1虚拟CPU, 4GiB / 7.5) * 2执行器 * 10秒
                         #              = 1 * 2 * 10 = 20 计算秒数

total_compute_seconds = driver_compute_seconds + executor_compute_seconds
                      = 10 compute-seconds + 20 compute-seconds
                      = 30 compute-seconds
                      # 总计算秒数 = 驱动器计算秒数 + 执行器计算秒数
                      #           = 10 计算秒数 + 20 计算秒数
                      #           = 30 计算秒数
```
