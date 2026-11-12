:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 模拟日期、时间戳和UUID

您可以通过利用`jest.spyOn()`注入一个模拟来指定非确定性函数的输出以运行测试。

### UUID函数

您可以通过注入一个模拟来指定`Uuid`的输出。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects, ExampleDataFlight } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";
import { Uuid } from "@foundry/functions-utils";

// 描述一个测试套件
describe("example test suite", () => {
    const myFunctions = new MyFunctions(); // 实例化 MyFunctions 类

    // 定义一个测试用例
    test("creates new flight", () => {
        const makeUuid = () => "my-uuid"; // 定义一个返回固定 UUID 的函数
        jest.spyOn(Uuid, "random").mockImplementation(() => makeUuid()); // 使用 jest.spyOn 来模拟 Uuid.random 方法

        // 验证 createNewFlight 函数是否正确创建了一个新对象
        verifyOntologyEditFunction(() => myFunctions.createNewFlight())
            .createsObject({
                objectType: ExampleDataFlight, // 期望创建的对象类型
                properties: {
                    flightId: makeUuid() // 期望对象的属性和值
                }
            })
    })
});
```

这个 TypeScript 代码段是一个使用 Jest 测试框架编写的单元测试。它验证了 `createNewFlight` 方法是否正确创建了一个类型为 `ExampleDataFlight` 的对象，并且该对象的 `flightId` 属性值为 `"my-uuid"`。

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight } from "@foundry/ontology-api";
import { Uuid } from "@foundry/functions-utils";

export class MyFunctions {
    // 标记该方法会编辑 ExampleDataFlight 实例
    @Edits(ExampleDataFlight)
    // 标记该方法是一个本体编辑函数
    @OntologyEditFunction()
    public createNewFlight(): void {
        // 使用随机生成的 UUID 创建一个新的 ExampleDataFlight 实例
        Objects.create().exampleDataFlight(Uuid.random());
    }
}
```

#### 高级UUID函数

在某些情况下，您可能希望完全控制`Uuid`的输出。这需要您调整正在测试的函数的代码。例如，上面的`createNewFlight`函数被包装在一个类`MyFunctions`中，您可以向该类添加一个构造函数，该构造函数带有一个默认值的供应器。带有供应器的更新函数如下所示：

```typescript
import { Function, OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Objects, ExampleDataFlight } from "@foundry/ontology-api";
import { Uuid } from "@foundry/functions-utils";

export class MyFunctions {
    constructor (private UuidSupplier: () => string = Uuid.random){} // 这个构造函数接受一个供应函数，默认使用 Uuid.random

    @Edits(ExampleDataFlight) // 编辑 ExampleDataFlight 的注解
    @OntologyEditFunction() // 本体编辑函数的注解
    public createNewFlightWithConstructor(): void {
        Objects.create().exampleDataFlight(this.UuidSupplier()); // 创建一个新的 ExampleDataFlight 对象，使用 UuidSupplier 提供的 UUID
    }
}
```

此更新的函数可以在完全控制输出的情况下进行测试（在此情况下，我们将生成的`Uuid`设置为`my-other-uuid`）：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";
import { Uuid } from "@foundry/functions-utils";

// 描述测试套件
describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    // 测试用例：创建带供应商的新航班
    test("creates new flight with supplier", () => {
        // 创建 MyFunctions 实例，同时提供自定义 UUID 生成函数
        const myNewFunctions = new MyFunctions(() => "my-other-uuid");

        // 验证本体编辑功能，确保创建的对象符合预期
        verifyOntologyEditFunction(() => myNewFunctions.createNewFlightWithConstructor())
            .createsObject({
                objectType: ExampleDataFlight, // 对象类型
                properties: {
                    flightId: "my-other-uuid" // 设置航班ID为自定义的UUID
                }
            })

    })
});
```

此代码是一个 TypeScript 测试套件，主要功能是验证通过自定义的 UUID 创建航班对象的正确性。

### Timestamp.now() 函数

可以通过注入模拟来指定 `Timestamp.now()` 的输出。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects , ExampleDataFlight } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";
import { Timestamp } from "@foundry/functions-api";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("test timestamp now", () => {
        // 创建一个固定的时间戳
        const makeTimestamp = () => Timestamp.fromISOString("2018-06-13T12:11:13+05:00");
        // 使用 jest.spyOn 来监控 Timestamp 的 now 方法，并返回固定的时间戳
        jest.spyOn(Timestamp, "now").mockImplementation(() => makeTimestamp());

        // 创建一个航班对象
        const flight = Objects.create().exampleDataFlight("flightAnotherTest");
        // 验证 myFunctions.startTakeoff(flight) 方法是否正确修改了航班对象的 takeoff 属性
        verifyOntologyEditFunction(() => myFunctions.startTakeoff(flight))
            .modifiesObject({
                object: flight,
                properties: {
                    takeoff: makeTimestamp() // 确保 takeoff 属性被正确设置为固定的时间戳
                }
            })
    })
});
```

这可以被用于在测试以下函数：

```typescript
import { Function, OntologyEditFunction, Edits, Timestamp } from "@foundry/functions-api";
import { Objects, ExampleDataFlight } from "@foundry/ontology-api";

// 定义一个名为 MyFunctions 的类
export class MyFunctions {
    // 使用装饰器 @Edits 和 @OntologyEditFunction
    // @Edits(ExampleDataFlight) 表示这个方法会编辑 ExampleDataFlight 的实例
    @Edits(ExampleDataFlight)
    @OntologyEditFunction()
    public startTakeoff(flight: ExampleDataFlight): void {
        // 设置航班的起飞时间为当前时间
        flight.takeoff = Timestamp.now();
    }
}
```

### LocalDate.now() 函数

你可以通过注入一个模拟值来指定 `LocalDate.now()` 的输出。以下是一个示例：

```typescript
import { MyFunctions } from ".."

import { Objects, ExampleDataFlight } from "@foundry/ontology-api";
import { verifyOntologyEditFunction } from "@foundry/functions-testing-lib";
import { LocalDate } from "@foundry/functions-api";

describe("example test suite", () => {
    const myFunctions = new MyFunctions();

    test("test LocalDate now", () => {
        // 创建一个 LocalDate 实例，表示特定日期 "2018-06-13"
        const makeLocalDate = () => LocalDate.fromISOString("2018-06-13");

        // 使用 Jest 的 spyOn 和 mockImplementation 模拟 LocalDate.now 方法
        // 使其返回 makeLocalDate() 的结果
        jest.spyOn(LocalDate, "now").mockImplementation(() => makeLocalDate());

        // 创建一个 flight 对象，作为测试数据
        const flight = Objects.create().exampleDataFlight("flightTest");

        // 验证 myFunctions.dateTakeoff 方法对 flight 对象的修改
        verifyOntologyEditFunction(() => myFunctions.dateTakeoff(flight))
            .modifiesObject({
                object: flight,
                properties: {
                    date: makeLocalDate() // 检查 flight 对象的 date 属性是否被设置为 makeLocalDate() 返回的日期
                }
            })
    })
});
```

这可以被用于在测试以下函数：

```typescript
import { Function, OntologyEditFunction, Edits, LocalDate } from "@foundry/functions-api";
import { Objects, ExampleDataFlight } from "@foundry/ontology-api";

export class MyFunctions {
    // 使用 @Edits 装饰器来标记编辑的类
    @Edits(ExampleDataFlight)
    // 使用 @OntologyEditFunction 装饰器来标记本方法为本体编辑函数
    @OntologyEditFunction()
    public dateTakeoff(flight: ExampleDataFlight): void {
        // 将航班的起飞日期设为当前日期
        flight.date = LocalDate.now();
    }
}
```

本代码展示了一个 TypeScript 类 `MyFunctions`，其中包含一个方法 `dateTakeoff`，该方法用于更新航班对象 `ExampleDataFlight` 的起飞日期为当前日期。`@Edits` 和 `@OntologyEditFunction` 是用于标记和注释该方法的装饰器。
