:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# API: 附件

:::callout{theme="warning"}
函数在具有严格内存限制的环境中执行。在处理文件数据时，超出这些内存限制可能会很快发生；我们建议仅与小于20MB的附件进行交互。
:::

附件是一个像对象属性一样的文件。附件作为临时文件上传，并通过操作附加到对象上。一旦附加到对象，附件即被持久化，并可以类似于其他属性访问。

## 函数中的附件

附件可以直接作为操作的输入传递到函数中，或作为对象上的属性访问。您也可以在函数中创建附件。

## 读取附件数据

要读取附件中的原始数据，请在附件上使用`readAsync`方法。`readAsync`方法的签名如下：

```typescript
readAsync(): Promise<Blob>; // 读取异步方法，返回一个Promise对象，包含Blob类型的数据
```

`Blob`是一个标准的[JavaScript类型↗](https://developer.mozilla.org/en-US/docs/Web/API/Blob)，表示一个类似文件的不可变原始数据对象。

您可能需要使用库或编写自定义代码来处理复杂的文件类型。例如，PDF文件必须使用适当的库进行解析。[了解更多关于向函数库添加NPM依赖项的信息。](../TypeScript%20basics/%E6%B7%BB%E5%8A%A0%20npm%20%E4%BE%9D%E8%B5%96%E9%A1%B9.md)

通常，与解析文件数据相关的依赖项将依赖于`fs`模块，而该模块在函数环境中不可用。这一限制可能会在编译和执行期间导致`fs`模块出错。为了解决这个限制，您可以引入对内存文件系统（例如`memfs`）的依赖。然后，将该依赖以`fs`的名称进行别名化。

例如，在您的`package.json`中使用NPM依赖`memfs`将如下所示：

```json
"fs": "npm:memfs@^x.x.x"
// 这是一个JSON格式的依赖项声明，用于在项目中使用memfs包。
// "fs" 代表文件系统模块，它在这里被替换为memfs库的一个特定版本。
// "npm:memfs@^x.x.x" 表示从npm获取memfs包，并且使用符合x.x.x版本号的所有版本。
// memfs 是一个内存文件系统库，常用于测试环境或需要模拟文件系统的场景。
```

以下示例演示如何从附件中读取数据：

```typescript
@OntologyEditFunction()
public async updateMaintenanceLog(aircraft: Aircraft, completedMaintenanceLog: Attachment): Promise<void> {
    const aircraftMaintenanceLogData: Blob = await aircraft.maintenanceLog.readAsync();
    const completedMaintenanceLogData: Blob = await completedMaintenanceLog.readAsync();

    // 比较当前的飞机维护日志和已完成的日志，并创建一个新的维护日志
    const updatedMaintenanceLogData: Blob;

    // 更新飞机的维护日志
    aircraft.maintenanceLog = await Attachments.uploadFile("maintenance-log.txt", updatedMaintenanceLogData);
}
```

## 创建附件

函数也可以用来创建附件并将它们附加到Objects。为了使在函数中创建的附件得以持久化，函数必须进行[Ontology编辑](../Ontology%20edits/API-%20Ontology%E7%BC%96%E8%BE%91.md)，以将附件链接到Object。

:::callout{theme="warning"}
未附加到Object的附件只能由上传者查看，并在一定时间后自动删除。
:::

要创建附件，请在从`@foundry/functions-api`导入的`Attachments`接口上使用`uploadFile`。`uploadFile`方法的签名如下：

```typescript
// 上传文件函数，接受文件名和Blob对象，返回一个Promise类型的Attachment
uploadFile(filename: string, blob: Blob): Promise<Attachment>;
```

以下示例展示了上传文件并将生成的附件指派给Object的过程。

```typescript
import { Attachments, Attachment, OntologyEditFunction } from "@foundry/functions-api"

@OntologyEditFunction()
public async setMaintenanceLog(aircraft: Aircraft): Promise<void> {
    const data: Blob;

    // 创建 Blob 对象并将其赋值给 data 变量的逻辑
    // Logic to create a Blob and assign it to the data variable

    const maintenanceLog = await Attachments.uploadFile("maintenance-log.txt", data);
    // 上传文件并返回维护日志的附件信息
    aircraft.maintenanceLog = maintenanceLog;
}
```

您可能需要依赖库或自定义代码来创建`Blob`对象，该对象作为参数传递给`uploadFile`方法。
