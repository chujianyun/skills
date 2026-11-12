:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 验证Ontology编辑

您可以使用 `verifyOntologyEditFunction()` API 来验证您的函数执行的编辑。您需要从 `"@foundry/functions-testing-lib"` 中导入它。这使您能够围绕以下列出的工作流创建单元测试。

#### 单数与复数验证方法

每种编辑都可以使用单数或复数方法进行验证。单数方法验证一项编辑，接受单个值；复数方法验证同一类型的多项编辑，接受这些值的数组。这两种形式不可互换，使用错误的形式会导致类型错误。

| 要验证的编辑    | 验证一项编辑                                 | 验证多项编辑                                    |
| --------------- | -------------------------------------------- | ----------------------------------------------- |
| Object创建      | `.createsObject({ objectType, properties })` | `.createsObjects([{ objectType, properties }])` |
| Object属性编辑  | `.modifiesObject({ object, properties })`    | `.modifiesObjects([{ object, properties }])`    |
| Object删除      | `.deletesObject(object)`                     | `.deletesObjects([object])`                     |
| 链接创建        | `.addsLink({ link, linkedObject })`          | `.addsLinks([{ link, linkedObject }])`          |
| 链接移除        | `.removesLink({ link, unlinkedObject })`     | `.removesLinks([{ link, unlinkedObject }])`     |

链接相关的四个方法还接受一个回调，该回调会收到目前已收集的编辑。当要链接的Object由被测函数创建时，这非常有用。在这种情况下，`.addsLink` 和 `.removesLink` 从回调中返回单个链接，而 `.addsLinks` 和 `.removesLinks` 返回一个数组。

`.hasNoMoreEdits()` 没有复数形式，并且由于它不返回结果，因此必须位于验证链的最后。

#### 验证Object创建

您可以使用 `.createsObject` 方法来验证Object的创建。如需在一次调用中验证多个Object的创建，请改用 `.createsObjects`。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataAirport } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

// 描述一个测试套件
describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    // 定义一个测试用例
    test("create airport", () => {
        // 使用 verifyOntologyEditFunction 验证 myFunctions.createAirport 方法的行为
        verifyOntologyEditFunction(() => myFunctions.createAirport("airportCode", "airportDisplayName"))
            .createsObject(
                {
                    objectType: ExampleDataAirport, // 期望创建的对象类型
                    properties: { // 期望创建对象的属性
                        airport: "airportCode",
                        displayAirportName: "airportDisplayName",
                    },
                });
    });
});
```

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataAirport } from "@foundry/ontology-api";

export class MyFunctions {

    // 使用 @Edits 和 @OntologyEditFunction 装饰器来修饰 createAirport 方法
    @Edits(ExampleDataAirport)
    @OntologyEditFunction()
    public createAirport(airport: string, displayName: string): void {
        // 创建一个新的机场对象
        const newAirport = Objects.create().exampleDataAirport(airport);
        // 设置机场的显示名称
        newAirport.displayAirportName = displayName;
    }
}
```

#### 验证新创建对象上的编辑

您可以验证涉及新创建对象的编辑。例如，您可能想创建一个新的`ExampleDataFlight`对象，并验证是否已创建到`new-flight-delay-0`的链接。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("single key with single created object", () => {
            // 创建一个 flight 对象，参数为 "flightTest"
            const flight = Objects.create().exampleDataFlight("flightTest");

            // 验证函数 createAndLinkDelays 是否按照预期创建对象和链接
            verifyOntologyEditFunction(() => myFunctions.createAndLinkDelays(flight, 1))
                // 检查是否创建了具有指定属性的新对象
                .createsObject({
                    objectType: ExampleFlightDelayEvent,
                    properties: {
                        eventId: "new-flight-delay-0", // 期望的事件 ID
                    },
                })
                // 检查是否添加了链接
                .addsLink(edits => ({
                    link: flight.flightDelayEvent, // 当前航班的延迟事件链接
                    linkedObject: edits.createdObjects.byObjectType(ExampleFlightDelayEvent)[0], // 新创建的延迟事件对象
                }))
        });
});
```

#### 验证Object属性编辑

您可以使用`.modifiesObject`验证对属性的编辑。如需在一次调用中验证多个Object的属性编辑，请向 `.modifiesObjects` 传入一个数组。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("modifies aircraft of the flight", () => {
        // 创建一个航班示例，从纽约飞往洛杉矶
        const flight = Objects.create().exampleDataFlight("NY -> LA");
        // 创建一个旧的飞机对象，航班原本使用的飞机
        const oldAircraft = Objects.create().exampleDataAircraft("N11111");
        flight.aircraft.set(oldAircraft); // 设置航班的初始飞机
        // 创建一个新的飞机对象，准备替换为该飞机
        const newAircraft = Objects.create().exampleDataAircraft("A00000");
        // 验证编辑函数是否正确修改了航班的飞机信息
        verifyOntologyEditFunction(() => myFunctions.assignAircraftToFlight(flight, newAircraft))
            .modifiesObject(
                {
                    object: flight,
                    properties: {
                        tailNumber: "A00000" // 期望的修改结果：飞机尾号被更新
                    }
                })
        });
});
```

这可以被用于在测试以下函数：

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";

export class MyFunctions {

    @Edits(ExampleDataFlight)
    @OntologyEditFunction()
    public assignAircraftToFlight(flight: ExampleDataFlight, aircraft: ExampleDataAircraft): void {
        // 清除当前航班的飞机信息
        flight.aircraft.clear();
        // 将飞机与航班关联
        aircraft.flight.set(flight);
        // 设置航班的尾号为飞机的尾号
        flight.tailNumber = aircraft.tailNumber;
    }
}
```

在这个代码片段中，我们定义了一个类 `MyFunctions`，其中包含一个方法 `assignAircraftToFlight`，用于将飞机分配给航班。通过使用 `@Edits` 和 `@OntologyEditFunction` 装饰器，我们可以指明这个方法会修改航班数据的本体。在方法内部，我们首先清除当前航班的飞机信息，然后将传入的飞机与航班关联，并将航班的尾号设置为飞机的尾号。

#### 验证对象没有其他编辑

您可以使用非必填的 `.hasNoMoreEdits()` 来确保没有其他编辑。这意味着只允许指定的编辑，如果检测到其他编辑，验证将失败。以下是一个例子：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

// 定义一个测试套件 "example test suite"
describe("example test suite", () => {
    const myFunctions = new MyFunctions(); // 创建 MyFunctions 的实例

    // 定义一个测试用例 "single key with linked object"
    test("single key with linked object", () => {
            const flight = Objects.create().exampleDataFlight("flightAnotherTest"); // 创建一个 ExampleDataFlight 对象
            const delay = Objects.create().exampleFlightDelayEvent("new-flight-delay"); // 创建一个 ExampleFlightDelayEvent 对象
            verifyOntologyEditFunction(() => myFunctions.linkDelays(flight, delay)) // 验证函数 linkDelays 的行为
                .addsLink({link: flight.flightDelayEvent, linkedObject: delay }) // 验证是否正确添加链接
                .hasNoMoreEdits(); // 验证没有其他编辑操作
        });
});
```

使用 `.hasNoMoreEdits()` 时，可以忽略发生的特定类型的编辑。通过传递一个包含以下某些或全部内容的对象来实现：

* `ignoreExtraCreatedObjects: true`
* `ignoreExtraModifiedObjects: true`
* `ignoreExtraDeletedObjects: true`
* `ignoreExtraLinkedObjects: true`
* `ignoreExtraUnlinkedObjects: true`

#### 验证到对象的链接创建

可以使用 `.addsLink` 验证对象上的链接创建。以下是一个示例：
此测试相当于测试同一链接在相反方向的情况：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("single key with linked object reverse", () => {
            // 创建一个航班对象
            const flight = Objects.create().exampleDataFlight("flightAnotherTest");
            // 创建一个航班延误事件对象
            const delay = Objects.create().exampleFlightDelayEvent("new-flight-delay")
            // 验证通过myFunctions.linkDelays函数进行的本体编辑
            verifyOntologyEditFunction(() => myFunctions.linkDelays(flight, delay))
                // 验证是否添加了正确的链接
                .addsLink({link: delay.flight, linkedObject: flight })
                // 确保没有其他编辑
                .hasNoMoreEdits();
        });
});
```

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";

export class MyFunctions {

    @Edits(ExampleDataFlight, ExampleFlightDelayEvent )
    @OntologyEditFunction()
    // 该方法用于将航班延误事件与航班数据关联起来
    public linkDelays(flight: ExampleDataFlight, delay: ExampleFlightDelayEvent): void {
        // 将延误事件添加到航班的延误事件列表中
        flight.flightDelayEvent.add(delay);
    }
}
```

#### 验证从对象中移除链接

您可以使用`.removesLink`验证从对象中移除链接。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

// 描述测试套件
describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    // 测试链接移除功能
    test("test link removal", () => {
            const flight = Objects.create().exampleDataFlight("flightAnotherTest"); // 创建一个示例航班对象
            const delay = Objects.create().exampleFlightDelayEvent("new-flight-delay") // 创建一个航班延误事件
            flight.flightDelayEvent.add(delay); // 将延误事件添加到航班的延误事件列表中
            verifyOntologyEditFunction(() => myFunctions.removeAllDelays(flight)) // 验证移除所有延误事件的功能
                .removesLink({link: flight.flightDelayEvent, unlinkedObject: delay }) // 确认链接被移除
                .hasNoMoreEdits(); // 确认没有其他的编辑操作
        });
});
```

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";

export class MyFunctions {

    // 使用 @Edits 装饰器，指定该方法会修改 ExampleDataFlight 和 ExampleFlightDelayEvent
    @Edits(ExampleDataFlight, ExampleFlightDelayEvent)
    // 使用 @OntologyEditFunction 装饰器标识这是一个本体编辑函数
    @OntologyEditFunction()
    // 定义一个方法，用于移除航班的所有延误事件
    public removeAllDelays(flight: ExampleDataFlight): void {
        flight.flightDelayEvent.clear(); // 清空 flightDelayEvent 集合，移除所有延误事件
    }
}
```

#### 验证删除Object

您可以使用 `.deletesObject` 验证删除Object。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("test object deletion", () => {
            const flight = Objects.create().exampleDataFlight("flightAnotherTest");
            verifyOntologyEditFunction(() => myFunctions.deleteFlight(flight))
                .deletesObject(flight) // 确认对象被删除
                .hasNoMoreEdits(); // 确认没有更多的编辑操作
        });
});
```

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight } from "@foundry/ontology-api";

// 定义一个类 MyFunctions，用于处理航班数据的相关操作
export class MyFunctions {

    // 使用 Edits 装饰器声明该方法会编辑 ExampleDataFlight 类型的对象
    // 使用 OntologyEditFunction 装饰器标记这是一个本体编辑函数
    @Edits(ExampleDataFlight)
    @OntologyEditFunction()
    public deleteFlight(flight: ExampleDataFlight): void {
        // 调用 flight 对象的 delete 方法来删除航班信息
        flight.delete();
    }
}
```

#### 验证多个对象已创建

您可以向 `.createsObjects` 方法传入一个Object规范数组，以验证多个Object已被创建。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

describe("example test suite", () => { // 描述测试套件
    const myFunctions = new MyFunctions(); // 创建 MyFunctions 实例

    test("single key with many created objects", () => { // 测试单个键与多个创建对象的关联
            const flight = Objects.create().exampleDataFlight("flightTest"); // 创建一个示例飞行数据对象
            verifyOntologyEditFunction(() => myFunctions.createAndLinkDelays(flight, 3))
                .createsObjects(
                    [0, 1, 2].map(i => ({ // 创建多个 ExampleFlightDelayEvent 对象
                        objectType: ExampleFlightDelayEvent,
                        properties: {
                            eventId: "new-flight-delay-" + i, // 为每个对象指定唯一的 eventId
                        },
                    })),
                )
                .addsLinks(edits =>
                    edits.createdObjects.byObjectType(ExampleFlightDelayEvent).map(event => ({ // 将创建的延迟事件与飞行对象链接
                        link: flight.flightDelayEvent,
                        linkedObject: event,
                    })),
                )
                .hasNoMoreEdits(); // 确保没有其他编辑
        });
});
```

```typescript
import { Function, Integer, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight, ExampleFlightDelayEvent } from "@foundry/ontology-api";

export class MyFunctions {

    @Edits(ExampleDataFlight, ExampleFlightDelayEvent )
    @OntologyEditFunction()
    public createAndLinkDelays(flight: ExampleDataFlight, numDelay: Integer): void {
        // 遍历指定的延迟次数
        for (let n = 0; n < numDelay; n++) {
            // 创建一个新的航班延迟事件对象
            const delay = Objects.create().exampleFlightDelayEvent(`new-flight-delay-${n}`);
            // 将新创建的延迟事件添加到航班的延迟事件集合中
            flight.flightDelayEvent.add(delay);
        }
    }
}
```

* 这个代码定义了一个名为 `MyFunctions` 的类，其中包含一个名为 `createAndLinkDelays` 的方法。
* `createAndLinkDelays` 方法接收两个参数：一个航班 `flight` 和一个表示延迟次数的整数 `numDelay`。
* 该方法通过循环创建指定数量的航班延迟事件，并将这些事件添加到航班的延迟事件集合中。

### 异步Ontology编辑

您可以通过以下方式验证异步Ontology编辑：

```typescript
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";

// 测试一个异步编辑函数
test("test async edit function", async () => {
        // 创建一个包含所有属性类型的对象
        const obj = Objects.create().objectWithAllPropertyTypes(1);
        // 验证编辑函数是否正确修改了对象
        (await verifyOntologyEditFunction(() => myFunctions.setDateAndTimestampToNow(obj))).modifiesObject({
            object: obj,
            properties: {
                // 期望timestampProperty属性被修改为当前时间戳
                timestampProperty: makeTimestamp(),
            },
        });
    });
```

### 多重验证

正如我们在上述示例中所看到的，我们可以串联验证。以下模式说明了这一点：

```typescript
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";
import { Objects, ExampleDataObject } from "@foundry/ontology-api";

test("multiple action edit", () => {
    // 验证多步骤编辑功能
    verifyOntologyEditFunction(() => myFunctions.multistageEdits("objectId", "objectName"))
        .createsObject({...}) // 创建对象
        .modifiesObjects([{...}]) // 修改对象
        .addsLinks([{...}]) // 添加链接
        .removesLinks([{...}]) // 移除链接
        .deletesObject(...) // 删除对象
        .hasNoMoreEdits(); // 确保没有更多的编辑操作
});
```
