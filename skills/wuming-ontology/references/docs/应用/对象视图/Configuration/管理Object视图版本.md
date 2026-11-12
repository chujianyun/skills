:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 管理Object视图版本

您对Object视图所做的更改将存储为**版本**，每个Object类型都有单独的历史记录。一个版本可以包含多个更改，例如添加、编辑和删除微件或标签页。以下是版本可以让您执行的一些操作：

* 通过将更改保存为增量版本，安全地迭代Object视图
* 控制哪个版本发布并对用户可见
* 在出现问题时重新发布旧版本
* 通过为版本添加描述，更高效地协作

## 使用说明

### 保存新版本

要保存Object视图的新版本，您必须先编辑Object视图（例如，更改/添加一个微件或标签页），然后保存这些更改。

默认情况下，当保存新版本时，它也会因为启用了自动发布而发布给用户。您将在标题中看到一个**保存并发布**按钮。

[官方图片已失效：保存新版本](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_save-and-publish.png)

如果自动发布被禁用，标题将有一个**保存**按钮，这将仅仅保存一个新版本而不发布它。[阅读更多关于自动发布行为或如何禁用它的信息。](#automatic-publishing)

您也可以**添加描述**到您的版本中，既可以从标题的左上方，也可以在版本历史面板中添加。

[官方图片已失效：添加描述](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_add-a-description.png)

### 浏览历史记录

要查看Object视图上所做的所有更改，您可以从右上方的编辑器标题导航到版本历史面板。在这里，您将看到所有版本的按时间顺序排列的列表，最新的在顶部，最旧的在底部。目前已发布的版本旁边有一个绿色勾选图标，而之前发布的版本有一个灰色勾选图标。

[官方图片已失效：浏览历史记录](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_navigating-to-history.png)

您可以看到某个版本保存的时间、作者是谁以及它基于哪个版本（即作者开始更改的版本）。此外，如果作者添加了描述，您还会看到版本的描述。

要查看完整描述和更多关于某个版本的细节，您可以将鼠标光标悬停在列表中的项目上。在悬停时出现的卡片中，您还可以编辑描述，或者如果没有描述的话，添加一个。

[官方图片已失效：查看完整详情](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_see-full-details.png)

版本历史面板还会在面板的最顶部突出显示当前发布给所有人的版本。

打开历史面板时，会显示您最近的20个版本。您可以通过导航到列表底部并点击**加载更多**按钮来查看较旧的版本。您最多只能查看200个过去的版本。

### 发布新版本

如果自动发布已关闭，您需要明确发布您的版本以使其对用户可用。

一旦您对所做的更改感到满意并已保存它们，您可以继续并通过点击编辑器标题中的**发布**按钮或版本历史面板中的版本悬停卡片，将您想要的版本发布给用户。

[官方图片已失效：发布新版本](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_publish-version.png)

### 预览

您可以通过点击版本历史面板中的任意一个版本来预览该版本。

但是，如果您有未保存的更改，您必须先保存或放弃这些更改才能预览版本。

### 重新发布旧版本

您可以重新发布Object视图的先前版本。例如，如果Object视图的较新版本出现问题，您可以重新发布您知道正常工作的旧版本。要重新发布先前发布的版本，您可以简单地从版本历史面板或编辑器标题中（如果您正在预览它）重新发布它。这样将该版本复制到版本历史列表的最顶部以保留操作的时间顺序。

[官方图片已失效：重新发布旧版本](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_republish-version.png)

### <a name="automatic-publishing"></a> 自动发布

默认情况下，所有Object类型都启用了自动发布，这意味着每个新版本在保存时也会被发布。要禁用此功能，请从标题中的保存并发布按钮旁的下拉菜单或历史面板中关闭它。

[官方图片已失效：更改自动发布设置](https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_change-automatic-publishing.png)

如果您的Object视图正在被许多用户积极使用和/或有多个编辑者在协作编辑视图，那么我们建议禁用自动发布。这降低了用户视图或工作流程中断的几率，并通过更清晰地显示每个人在做什么来提高协作效率。

只有拥有发布权限的编辑者可以更改自动发布设置。


> 配图缺失说明：本页有 7 个官方图片地址在抓取及重试时失效（返回 HTML 错误页）。下列地址保留用于溯源，未替换成其他版本的图片。

- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_add-a-description.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_change-automatic-publishing.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_navigating-to-history.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_publish-version.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_republish-version.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_save-and-publish.png>
- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/object-views/manage-object-view-versions_see-full-details.png>
