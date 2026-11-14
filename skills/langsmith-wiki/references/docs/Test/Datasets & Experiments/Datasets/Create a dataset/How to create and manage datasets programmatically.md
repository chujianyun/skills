# How to create and manage datasets programmatically

You can use the Python and TypeScript SDK to manage datasets programmatically. This includes creating, updating, and deleting datasets, as well as adding examples to them.

## Create a dataset

### Create a dataset from list of values

The most flexible way to make a dataset using the client is by creating examples from a list of inputs and optional outputs. Below is an example.

Note that you can add arbitrary metadata to each example, such as a note or a source. The metadata is stored as a dictionary.

> [!TIP]
>
> If you have many examples to create, consider using the `create_examples`/`createExamples` method to create multiple examples in a single request. If creating a single example, you can use the `create_example`/`createExample` method.

```python Python
from langsmith import Client

examples = [
  {
    "inputs": {"question": "What is the largest mammal?"},
    "outputs": {"answer": "The blue whale"},
    "metadata": {"source": "Wikipedia"},
  },
  {
    "inputs": {"question": "What do mammals and birds have in common?"},
    "outputs": {"answer": "They are both warm-blooded"},
    "metadata": {"source": "Wikipedia"},
  },
  {
    "inputs": {"question": "What are reptiles known for?"},
    "outputs": {"answer": "Having scales"},
    "metadata": {"source": "Wikipedia"},
  },
  {
    "inputs": {"question": "What's the main characteristic of amphibians?"},
    "outputs": {"answer": "They live both in water and on land"},
    "metadata": {"source": "Wikipedia"},
  },
]

client = Client()
dataset_name = "Elementary Animal Questions"

# Storing inputs in a dataset lets us
# run chains and LLMs over a shared set of examples.
dataset = client.create_dataset(
  dataset_name=dataset_name, description="Questions and answers about animal phylogenetics.",
)

# Prepare inputs, outputs, and metadata for bulk creation
client.create_examples(
  dataset_id=dataset.id,
  examples=examples
)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const exampleInputs: [string, string][] = [
  ["What is the largest mammal?", "The blue whale"],
  ["What do mammals and birds have in common?", "They are both warm-blooded"],
  ["What are reptiles known for?", "Having scales"],
  [
    "What's the main characteristic of amphibians?",
    "They live both in water and on land",
  ],
];

const datasetName = "Elementary Animal Questions";

// Storing inputs in a dataset lets us
// run chains and LLMs over a shared set of examples.
const dataset = await client.createDataset(datasetName, {
  description: "Questions and answers about animal phylogenetics",
});

// Prepare inputs, outputs, and metadata for bulk creation
const inputs = exampleInputs.map(([inputPrompt]) => ({ question: inputPrompt }));
const outputs = exampleInputs.map(([, outputAnswer]) => ({ answer: outputAnswer }));
const metadata = exampleInputs.map(() => ({ source: "Wikipedia" }));

// Use the bulk createExamples method
await client.createExamples({
  inputs,
  outputs,
  metadata,
  datasetId: dataset.id,
});
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.core.JsonValue;
import com.langchain.smith.errors.UnexpectedStatusCodeException;
import com.langchain.smith.models.datasets.Dataset;
import com.langchain.smith.models.datasets.DatasetCreateParams;
import com.langchain.smith.models.datasets.DatasetListParams;
import com.langchain.smith.models.examples.bulk.BulkCreateParams;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class CreateDatasetExample {
    public static void main(String[] args) {
        LangsmithClient client = LangsmithOkHttpClient.fromEnv();

        List<String[]> exampleInputs = List.of(
            new String[]{"What is the largest mammal?", "The blue whale"},
            new String[]{"What do mammals and birds have in common?", "They are both warm-blooded"},
            new String[]{"What are reptiles known for?", "Having scales"},
            new String[]{"What's the main characteristic of amphibians?", "They live both in water and on land"}
        );

        String datasetName = "Elementary Animal Questions";

        Dataset dataset;
        try {
            dataset = client.datasets().create(
                DatasetCreateParams.builder()
                    .name(datasetName)
                    .description("Questions and answers about animal phylogenetics")
                    .build()
            );
        } catch (UnexpectedStatusCodeException e) {
            // Dataset already exists, get it
            if (e.statusCode() == 409) {
                DatasetListParams listParams = DatasetListParams.builder()
                    .name(datasetName)
                    .build();
                dataset = client.datasets().list(listParams).items().get(0);
            } else {
                throw e;
            }
        }

        // Prepare inputs, outputs, and metadata for bulk creation
        List<Map<String, String>> inputs = exampleInputs.stream()
            .map(pair -> {
                return Maps.of("question", pair[0]);
            })
            .collect(Collectors.toList());

        List<Map<String, String>> outputs = exampleInputs.stream()
            .map(pair -> {
                return Maps.of("answer", pair[1]);
            })
            .collect(Collectors.toList());

        List<Map<String, String>> metadata = exampleInputs.stream()
            .map(pair -> {
                return Maps.of("source", "Wikipedia");
            })
            .collect(Collectors.toList());

        // Use the bulk createExamples method
        BulkCreateParams.Builder bulkParamsBuilder = BulkCreateParams.builder();
        for (int i = 0; i < inputs.size(); i++) {
            bulkParamsBuilder.addBody(
                BulkCreateParams.Body.builder()
                    .datasetId(dataset.id())
                    .inputs(JsonValue.from(inputs.get(i)))
                    .outputs(JsonValue.from(outputs.get(i)))
                    .metadata(JsonValue.from(metadata.get(i)))
                    .build()
            );
        }

        client.examples().bulk().create(bulkParamsBuilder.build());
    }
}


```

### Create a dataset from traces

To create datasets from the runs (spans) of your traces, you can use the same approach. For **many** more examples of how to fetch and filter runs, see the [export traces](../../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Query%20traces%20using%20the%20SDK.md) guide. Below is an example:

```python Python
import asyncio
from datetime import datetime, timedelta, timezone

from langsmith import Client


async def main():
    client = Client()
    dataset_name = "Example Dataset"
    project_id = str(client.read_project(project_name="my_project").id)

    # Filter runs to add to the dataset
    runs = [
        run
        async for run in client.runs.query(
            project_ids=[project_id],
            min_start_time=datetime.now(timezone.utc) - timedelta(days=7),
            is_root=True,
            has_error=False,
            selects=["INPUTS", "OUTPUTS"],
        )
    ]

    dataset = client.create_dataset(dataset_name, description="An example dataset")

    # Prepare inputs and outputs for bulk creation
    examples = [{"inputs": run.inputs, "outputs": run.outputs} for run in runs]

    # Use the bulk create_examples method
    client.create_examples(dataset_id=dataset.id, examples=examples)


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const datasetName = "Example Dataset";
const projectId = (await client.readProject({ projectName: "my_project" })).id;

// Filter runs to add to the dataset
const runs = [];
for await (const run of client.runs.query({
  project_ids: [projectId],
  min_start_time: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
  is_root: true,
  has_error: false,
  selects: ["INPUTS", "OUTPUTS"],
})) {
  runs.push(run);
}

const dataset = await client.createDataset(datasetName, {
  description: "An example dataset",
  dataType: "kv",
});

// Prepare inputs and outputs for bulk creation
const inputs = runs.map((run) => run.inputs ?? {});
const outputs = runs.map((run) => run.outputs ?? {});

// Use the bulk createExamples method
await client.createExamples({
  inputs,
  outputs,
  datasetId: dataset.id,
});
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.core.JsonValue;
import com.langchain.smith.models.datasets.Dataset;
import com.langchain.smith.models.datasets.DatasetCreateParams;
import com.langchain.smith.models.examples.bulk.BulkCreateParams;
import com.langchain.smith.models.runs.Run;
import com.langchain.smith.models.runs.RunQueryV2Params;
import com.langchain.smith.models.runs.RunSelectField;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

public class CreateDatasetExample {
    public static void main(String[] args) {
        LangsmithClient client = LangsmithOkHttpClient.fromEnv();
        String projectId = System.getenv("LANGSMITH_PROJECT_ID");
        String datasetName = "Example Dataset";

        // Filter runs to add to the dataset; autoPager() follows the cursor for you
        RunQueryV2Params params = RunQueryV2Params.builder()
            .addProjectId(projectId)
            .minStartTime(OffsetDateTime.now().minusDays(7))
            .isRoot(true)
            .hasError(false)
            .addSelect(RunSelectField.INPUTS)
            .addSelect(RunSelectField.OUTPUTS)
            .build();
        List<Run> allRuns = new ArrayList<>();
        client.runs().queryV2(params).autoPager().forEach(allRuns::add);

        System.out.println("Total runs found: " + allRuns.size());

        // Create dataset
        Dataset dataset = client.datasets().create(
            DatasetCreateParams.builder()
                .name(datasetName)
                .description("An example dataset")
                .build()
        );

        // Prepare inputs and outputs for bulk creation
        BulkCreateParams.Builder bulkParamsBuilder = BulkCreateParams.builder();
        int examplesWithData = 0;
        for (Run run : allRuns) {
            if (run.inputs().isPresent() && run.outputs().isPresent()) {
                bulkParamsBuilder.addBody(
                    BulkCreateParams.Body.builder()
                        .datasetId(dataset.id())
                        .inputs(JsonValue.from(run.inputs().get()._additionalProperties()))
                        .outputs(JsonValue.from(run.outputs().get()._additionalProperties()))
                        .build()
                );
                examplesWithData++;
            }
        }

        System.out.println("Prepared " + examplesWithData + " examples from " + allRuns.size() + " runs");

        if (examplesWithData == 0) {
            System.err.println("No runs have both inputs and outputs. Cannot create examples.");
            System.exit(1);
        }

        client.examples().bulk().create(bulkParamsBuilder.build());
        System.out.println("Created " + examplesWithData + " examples in dataset");
    }
}
```

### Create a dataset from a CSV file

In this section, we will demonstrate how you can create a dataset by uploading a CSV file.

First, ensure your CSV file is properly formatted with columns that represent your input and output keys. These keys will be utilized to map your data properly during the upload. You can specify an optional name and description for your dataset. Otherwise, the file name will be used as the dataset name and no description will be provided.

```python Python
from langsmith import Client
import os

client = Client()
csv_file = 'path/to/your/csvfile.csv'
input_keys = ['column1', 'column2'] # replace with your input column names
output_keys = ['output1', 'output2'] # replace with your output column names

dataset = client.upload_csv(
  csv_file=csv_file,
  input_keys=input_keys,
  output_keys=output_keys,
  name="My CSV Dataset",
  description="Dataset created from a CSV file",
  data_type="kv"
)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const csvFile = 'path/to/your/csvfile.csv';
const inputKeys = ['column1', 'column2']; // replace with your input column names
const outputKeys = ['output1', 'output2']; // replace with your output column names

const dataset = await client.uploadCsv({
  csvFile: csvFile,
  fileName: "My CSV Dataset",
  inputKeys: inputKeys,
  outputKeys: outputKeys,
  description: "Dataset created from a CSV file",
  dataType: "kv"
});
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.models.datasets.Dataset;
import com.langchain.smith.models.datasets.DatasetUploadParams;
import com.langchain.smith.models.datasets.DataType;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
Path csvFile = Paths.get("path/to/your/csvfile.csv");
List<String> inputKeys = List.of("column1", "column2");
List<String> outputKeys = List.of("output1", "output2");

Dataset dataset = client.datasets().upload(
    DatasetUploadParams.builder()
        .file(csvFile)
        .inputKeys(inputKeys)
        .outputKeys(outputKeys)
        .name("My CSV Dataset")
        .description("Dataset created from a CSV file")
        .dataType(DataType.KV)
        .build()
);
```

### Create a dataset from pandas DataFrame (Python only)

The python client offers an additional convenience method to upload a dataset from a pandas dataframe.

```python
from langsmith import Client
import os
import pandas as pd

client = Client()
df = pd.read_parquet('path/to/your/myfile.parquet')
input_keys = ['column1', 'column2'] # replace with your input column names
output_keys = ['output1', 'output2'] # replace with your output column names

dataset = client.upload_dataframe(
    df=df,
    input_keys=input_keys,
    output_keys=output_keys,
    name="My Parquet Dataset",
    description="Dataset created from a parquet file",
    data_type="kv" # The default
)
```

## Fetch datasets

You can programmatically fetch datasets from LangSmith using the `list_datasets`/`listDatasets` method in the Python and TypeScript SDKs. Below are some common calls.

> [!NOTE]
>
> Initialize the client before running the below code snippets.

```python Python
from langsmith import Client

client = Client()
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
```

### Query all datasets

```python Python
datasets = client.list_datasets()
```

```typescript TypeScript
const datasets = await client.listDatasets();
```

```java Java
import com.langchain.smith.models.datasets.DatasetListParams;

DatasetListParams listParams = DatasetListParams.builder().build();
var datasets = client.datasets().list(listParams);
```

### List datasets by name

If you want to search by the exact name, you can do the following:

```python Python
datasets = client.list_datasets(dataset_name="My Test Dataset 1")
```

```typescript TypeScript
const datasets = await client.listDatasets({
  datasetName: "My Test Dataset 1"
});
```

```java Java
import com.langchain.smith.models.datasets.DatasetListParams;

DatasetListParams listParams = DatasetListParams.builder()
    .name("My Test Dataset 1")
    .build();
var datasets = client.datasets().list(listParams);
```

If you want to do a case-invariant substring search, try the following:

```python Python
datasets = client.list_datasets(dataset_name_contains="some substring")
```

```typescript TypeScript
const datasets = await client.listDatasets({
  datasetNameContains: "some substring"
});
```

```java Java
import com.langchain.smith.models.datasets.DatasetListParams;

DatasetListParams listParams = DatasetListParams.builder()
    .nameContains("some substring")
    .build();
var datasets = client.datasets().list(listParams);
```

### List datasets by type

You can filter datasets by type:

```python Python
datasets = client.list_datasets(data_type="kv")
```

```typescript TypeScript
const datasets = await client.listDatasets({
  dataType: "kv"
});
```

```java Java
import com.langchain.smith.models.datasets.DatasetListParams;

DatasetListParams listParams = DatasetListParams.builder()
    .datatype(DataType.of("kv"))
    .build();
var datasets = client.datasets().list(listParams);
```

## Fetch examples

You can programmatically fetch examples from LangSmith using the `list_examples`/`listExamples` method in the Python and TypeScript SDKs. Below are some common calls.

> [!NOTE]
>
> Initialize the client before running the below code snippets.

```python Python
from langsmith import Client

client = Client()
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
```

### List all examples for a dataset

You can filter by dataset ID:

```python Python
examples = client.list_examples(dataset_id="c9ace0d8-a82c-4b6c-13d2-83401d68e9ab")
```

```typescript TypeScript
const examples = await client.listExamples({
  datasetId: "c9ace0d8-a82c-4b6c-13d2-83401d68e9ab"
});
```

```java Java
import com.langchain.smith.models.examples.ExampleListParams;

ExampleListParams listParams = ExampleListParams.builder()
    .dataset("c9ace0d8-a82c-4b6c-13d2-83401d68e9ab")
    .build();
var examples = client.examples().list(listParams);
```

Or you can filter by dataset name (this must exactly match the dataset name you want to query)

```python Python
examples = client.list_examples(dataset_name="My Test Dataset")
```

```typescript TypeScript
const examples = await client.listExamples({
  datasetName: "My test Dataset"
});
```

### List examples by id

You can also list multiple examples all by ID.

```python Python
example_ids = [
  '734fc6a0-c187-4266-9721-90b7a025751a',
  'd6b4c1b9-6160-4d63-9b61-b034c585074f',
  '4d31df4e-f9c3-4a6e-8b6c-65701c2fed13',
]

examples = client.list_examples(example_ids=example_ids)
```

```typescript TypeScript
const exampleIds = [
  "734fc6a0-c187-4266-9721-90b7a025751a",
  "d6b4c1b9-6160-4d63-9b61-b034c585074f",
  "4d31df4e-f9c3-4a6e-8b6c-65701c2fed13",
];

const examples = await client.listExamples({
  exampleIds: exampleIds
});
```

```java Java
import com.langchain.smith.models.examples.ExampleListParams;
import java.util.List;

List<String> exampleIds = List.of(
    "734fc6a0-c187-4266-9721-90b7a025751a",
    "d6b4c1b9-6160-4d63-9b61-b034c585074f",
    "4d31df4e-f9c3-4a6e-8b6c-65701c2fed13"
);

ExampleListParams listParams = ExampleListParams.builder()
    .id(exampleIds)
    .build();
var examples = client.examples().list(listParams);
```

### List examples by metadata

You can also filter examples by metadata. Below is an example querying for examples with a specific metadata key-value pair. Under the hood, we check to see if the example's metadata contains the key-value pair(s) you specify.

For example, if you have an example with metadata `{"foo": "bar", "baz": "qux"}`, both `{foo: bar}` and `{baz: qux}` would match, as would `{foo: bar, baz: qux}`.

```python Python
examples = client.list_examples(dataset_name=dataset_name, metadata={"foo": "bar"})
```

```typescript TypeScript
const examples = await client.listExamples({
  datasetName: datasetName,
  metadata: {foo: "bar"}
});
```

```java Java
import com.langchain.smith.models.examples.ExampleListParams;

ExampleListParams listParams = ExampleListParams.builder()
    .datasetId(datasetId)
    .metadata("{\"foo\":\"bar\"}")
    .build();
var examples = client.examples().list(listParams);
```

### List examples by structured filter

Similar to how you can use the structured filter query language to [fetch runs](../../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Query%20traces%20using%20the%20SDK.md#use-filter-query-language), you can use it to fetch examples.

> [!NOTE]
>
> This is currently only available in v0.1.83 and later of the Python SDK and v0.1.35 and later of the TypeScript SDK.
>
> Additionally, the structured filter query language is only supported for `metadata` fields.

You can use the `has` operator to fetch examples with metadata fields that contain specific key/value pairs and the `exists` operator to fetch examples with metadata fields that contain a specific key. Additionally, you can chain multiple filters together using the `and` operator and negate a filter using the `not` operator.

```python Python
examples = client.list_examples(
  dataset_name=dataset_name,
  filter='and(not(has(metadata, \'{"foo": "bar"}\')), exists(metadata, "tenant_id"))'
)
```

```typescript TypeScript
const examples = await client.listExamples({
  datasetName: datasetName,
  filter: 'and(not(has(metadata, \'{"foo": "bar"}\')), exists(metadata, "tenant_id"))'
});
```

```java Java
import com.langchain.smith.models.examples.ExampleListParams;

String filter = "and(not(has(metadata, '{\"foo\": \"bar\"}')), exists(metadata, \"tenant_id\"))";

ExampleListParams listParams = ExampleListParams.builder()
    .datasetId(datasetId)
    .filter(filter)
    .build();
var examples = client.examples().list(listParams);
```

## Update examples

### Update single example

You can programmatically update examples from LangSmith using the `update_example`/`updateExample` method in the Python and TypeScript SDKs. Below is an example.

```python Python
client.update_example(
  example_id=example.id,
  inputs={"input": "updated input"},
  outputs={"output": "updated output"},
  metadata={"foo": "bar"},
  split="train"
)
```

```typescript TypeScript
await client.updateExample(example.id, {
  inputs: { input: "updated input" },
  outputs: { output: "updated output" },
  metadata: { "foo": "bar" },
  split: "train",
});
```

```java Java
import com.langchain.smith.core.JsonValue;
import com.langchain.smith.models.examples.ExampleUpdateParams;

 // Create Inputs using the builder
ExampleUpdateParams.Inputs inputsObj = ExampleUpdateParams.Inputs.builder()
    .putAdditionalProperty("input", JsonValue.from("updated input"))
    .build();

// Create Outputs using the builder
ExampleUpdateParams.Outputs outputsObj = ExampleUpdateParams.Outputs.builder()
    .putAdditionalProperty("output", JsonValue.from("updated output"))
    .build();

// Create Metadata using the builder
ExampleUpdateParams.Metadata metadataObj = ExampleUpdateParams.Metadata.builder()
    .putAdditionalProperty("foo", JsonValue.from("bar"))
    .build();

ExampleUpdateParams updateParams = ExampleUpdateParams.builder()
    .inputs(inputsObj)
    .outputs(outputsObj)
    .metadata(metadataObj)
    .split("train")
    .build();

ExampleUpdateResponse updateResponse = client.examples().update(example.id(), updateParams);
```

### Bulk update examples

You can also programmatically update multiple examples in a single request with the `update_examples`/`updateExamples` method in the Python and TypeScript SDKs. Below is an example.

```python Python
client.update_examples(
  example_ids=[example.id, example_2.id],
  inputs=[{"input": "updated input 1"}, {"input": "updated input 2"}],
  outputs=[
      {"output": "updated output 1"},
      {"output": "updated output 2"},
  ],
  metadata=[{"foo": "baz"}, {"foo": "qux"}],
  splits=[["training", "foo"], "training"] # Splits can be arrays or standalone strings
)
```

```typescript TypeScript
await client.updateExamples([
  {
    id: example.id,
    inputs: { input: "updated input 1" },
    outputs: { output: "updated output 1" },
    metadata: { foo: "baz" },
    split: ["training", "foo"] // Splits can be arrays or standalone strings
  },
  {
    id: example2.id,
    inputs: { input: "updated input 2" },
    outputs: { output: "updated output 2" },
    metadata: { foo: "qux" },
    split: "training"
  },
]);
```

```java Java
Map<String, String> inputs1 = Map.of("question", "What is the capital of France?")
Map<String, String> outputs1 = Map.of("answer", "The capital of France is Paris.");
Map<String, String> metadata1 = Map.of(
    "source", "Wikipedia",
    "difficulty", "easy"
);

Map<String, String> inputs2 = Map.of("question", "What is 2 + 2?");
Map<String, String> outputs2 = Map.of("answer", "The answer is 4.");
Map<String, String> metadata2 = Map.of(
    "source", "Math textbook",
    "difficulty", "easy");

BulkPatchAllParams.Builder bulkParamsBuilder = BulkPatchAllParams.builder();

bulkParamsBuilder.addBody(
    BulkPatchAllParams.Body.builder()
        .id(example1.id())
        .inputs(buildInputs(inputs1))
        .outputs(buildOutputs(outputs1))
        .metadata(buildMetadata(metadata1))
        .splitOfStrings(Arrays.asList("training", "validation"))
        .build()
);

bulkParamsBuilder.addBody(
    BulkPatchAllParams.Body.builder()
        .id(example2.id())
        .inputs(buildInputs(inputs2))
        .outputs(buildOutputs(outputs2))
        .metadata(buildMetadata(metadata2))
        .split("test")
        .build()
);

client.examples().bulk().patchAll(bulkParamsBuilder.build());
```
