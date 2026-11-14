# Upload files with traces

When you trace with the [`@traceable` decorator or `traceable` wrapper](Custom%20instrumentation.md#use-%40traceable-%2F-traceable), LangSmith supports uploading binary files (such as images, audio, videos, PDFs, and CSVs) alongside your traces. This is particularly useful when working with LLM pipelines using multimodal inputs or outputs.

In both the [Python](#python) and [TypeScript](#typescript) SDKs, you can add attachments to your traces by specifying the MIME type and binary content of each file. This page explains how to define and trace attachments using the `Attachment` type in Python and `Uint8Array` / `ArrayBuffer` in TypeScript.

## Python

In the [Python SDK](../../../Reference/langsmith%20%28smith-python-sdk%29.md), you can use the `Attachment` type to add files to your traces. Each `Attachment` requires:

* `mime_type` (str): The MIME type of the file (e.g., `"image/png"`).
* `data` (bytes | Path): The binary content of the file, or the file path.

You can also define an attachment with a tuple of the form `(mime_type, data)` for convenience.

There are two ways to provide file data:

* Load the bytes yourself and pass them directly (works in all environments), or
* Pass a `Path` object and let the SDK read the file by setting `dangerously_allow_filesystem=True` on your `@traceable` decorator.

  > [!NOTE]
  >
  > The `dangerously_allow_filesystem` flag exists as a safeguard for server and multi-tenant environments, where user-controlled input could influence a file path. In a trusted environment (a local script or a controlled pipeline where you own the file paths), it is safe to enable.

Decorate a function with `@traceable` and include your `Attachment` instances as arguments. The following example demonstrates both approaches: loading file bytes manually into an `Attachment`, and passing a `Path` object with `dangerously_allow_filesystem=True`:

```python Python
from langsmith import traceable
from langsmith.schemas import Attachment
from pathlib import Path
import os

# Must set dangerously_allow_filesystem to True if you want to use file paths
@traceable(dangerously_allow_filesystem=True)
def trace_with_attachments(
    val: int,
    text: str,
    image: Attachment,
    audio: Attachment,
    video: Attachment,
    pdf: Attachment,
    csv: Attachment,
):
    return f"Processed: {val}, {text}, {len(image.data)}, {len(audio.data)}, {len(video.data)}, {len(pdf.data), {len(csv.data)}}"

# Helper function to load files as bytes
def load_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()

# Load files and create attachments
image_data = load_file("my_image.png")
audio_data = load_file("my_mp3.mp3")
video_data = load_file("my_video.mp4")
pdf_data = load_file("my_document.pdf")

image_attachment = Attachment(mime_type="image/png", data=image_data)
audio_attachment = Attachment(mime_type="audio/mpeg", data=audio_data)
video_attachment = Attachment(mime_type="video/mp4", data=video_data)
pdf_attachment = ("application/pdf", pdf_data) # Can just define as tuple of (mime_type, data)
csv_attachment = Attachment(mime_type="text/csv", data=Path(os.getcwd()) / "my_csv.csv")

# Define other parameters
val = 42
text = "Hello, world!"

# Call the function with traced attachments
result = trace_with_attachments(
    val=val,
    text=text,
    image=image_attachment,
    audio=audio_attachment,
    video=video_attachment,
    pdf=pdf_attachment,
    csv=csv_attachment,
)
```

## TypeScript

In the [TypeScript SDK](../../../Reference/langsmith%20%28smith-js-ts-sdk%29.md), you can add attachments to traces by using `Uint8Array` or `ArrayBuffer` as data types. Each attachment's MIME type is specified within `extractAttachments`:

* `Uint8Array`: Useful for handling binary data directly.
* `ArrayBuffer`: Represents fixed-length binary data, which you can convert to `Uint8Array` as needed.

In the TypeScript SDK, the `extractAttachments` function is an optional parameter in the `traceable` configuration. When the traceable-wrapped function is invoked, it extracts binary data (e.g., images, audio files) from your inputs and logs them alongside other trace data, specifying their MIME types.

> [!NOTE]
>
> You cannot directly pass in a file path in the TypeScript SDK, because accessing local files is not supported in all runtime environments.

Wrap your function with `traceable` and include your attachments within the `extractAttachments` option. The signature is:

```typescript TypeScript
type AttachmentData = Uint8Array | ArrayBuffer;
type Attachments = Record<string, [string, AttachmentData]>;

extractAttachments?: (
    ...args: Parameters<Func>
) => [Attachments | undefined, KVMap];
```

The following example shows a full implementation:

```typescript TypeScript
import { traceable } from "langsmith/traceable";

const traceableWithAttachments = traceable(
    (
        val: number,
        text: string,
        attachment: Uint8Array,
        attachment2: ArrayBuffer,
        attachment3: Uint8Array,
        attachment4: ArrayBuffer,
        attachment5: Uint8Array,
    ) =>
        `Processed: ${val}, ${text}, ${attachment.length}, ${attachment2.byteLength}, ${attachment3.length}, ${attachment4.byteLength}, ${attachment5.byteLength}`,
    {
        name: "traceWithAttachments",
        extractAttachments: (
            val: number,
            text: string,
            attachment: Uint8Array,
            attachment2: ArrayBuffer,
            attachment3: Uint8Array,
            attachment4: ArrayBuffer,
            attachment5: Uint8Array,
        ) => [
            {
                "image inputs": ["image/png", attachment],
                "mp3 inputs": ["audio/mpeg", new Uint8Array(attachment2)],
                "video inputs": ["video/mp4", attachment3],
                "pdf inputs": ["application/pdf", new Uint8Array(attachment4)],
                "csv inputs": ["text/csv", new Uint8Array(attachment5)],
            },
            { val, text },
        ],
    }
);

const fs = Deno // or Node.js fs module
const image = await fs.readFile("my_image.png"); // Uint8Array
const mp3Buffer = await fs.readFile("my_mp3.mp3");
const mp3ArrayBuffer = mp3Buffer.buffer; // Convert to ArrayBuffer
const video = await fs.readFile("my_video.mp4"); // Uint8Array
const pdfBuffer = await fs.readFile("my_document.pdf");
const pdfArrayBuffer = pdfBuffer.buffer; // Convert to ArrayBuffer
const csv = await fs.readFile("test-vals.csv"); // Uint8Array

// Define example parameters
const val = 42;
const text = "Hello, world!";

// Call traceableWithAttachments with the files
const result = await traceableWithAttachments(
    val, text, image, mp3ArrayBuffer, video, pdfArrayBuffer, csv
);
```

## Related

* [Manage datasets](../../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md)
* [Set up LLM-as-a-judge online evaluators](../../../Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md)
