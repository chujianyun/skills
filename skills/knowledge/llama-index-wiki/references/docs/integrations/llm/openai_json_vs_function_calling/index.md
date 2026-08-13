# developers.llamaindex.ai/python/framework/integrations/llm/openai_json_vs_function_calling/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/openai_json_vs_function_calling/index.md

--- title: OpenAI JSON Mode vs. Function Calling for Data Extraction | Developer Documentation ---

OpenAI just released JSON Mode [1]: This new config constrain the LLM to only generate strings that parse into valid JSON (but no guarantee on validation against any schema).
Before this, the best way to extract structured data from text is via function calling [2].
In this notebook, we explore the tradeoff between the latest JSON Mode [1] and function calling feature for structured output & extraction.
*Update*: OpenAI has clarified that JSON mode is always enabled for function calling, it’s opt-in for regular messages (<https://community.openai.com/t/json-mode-vs-function-calling/476994/4>)
### Generate synthetic data
We’ll start by generating some synthetic data for our data extraction task. Let’s ask our LLM for a hypothetical sales transcript.
``` %pip install llama-index-llms-openai %pip install llama-index-program-openai ```

``` from llama_index.llms.openai import OpenAI
llm = OpenAI(model="gpt-3.5-turbo-1106") response = llm.complete( "Generate a sales call transcript, use real names, talk about a product, discuss some action items" ) ```

``` transcript = response.text print(transcript) ```

``` [Phone rings]
John: Hello, this is John.
Sarah: Hi John, this is Sarah from XYZ Company. I'm calling to discuss our new product, the XYZ Widget, and see if it might be a good fit for your business.
John: Hi Sarah, thanks for reaching out. I'm definitely interested in learning more about the XYZ Widget. Can you give me a quick overview of what it does?
Sarah: Of course! The XYZ Widget is a cutting-edge tool that helps businesses streamline their workflow and improve productivity. It's designed to automate repetitive tasks and provide real-time data analytics to help you make informed decisions.
John: That sounds really interesting. I can see how that could benefit our team. Do you have any case studies or success stories from other companies who have used the XYZ Widget?
Sarah: Absolutely, we have several case studies that I can share with you. I'll send those over along with some additional information about the product. I'd also love to schedule a demo for you and your team to see the XYZ Widget in action.
John: That would be great. I'll make sure to review the case studies and then we can set up a time for the demo. In the meantime, are there any specific action items or next steps we should take?
Sarah: Yes, I'll send over the information and then follow up with you to schedule the demo. In the meantime, feel free to reach out if you have any questions or need further information.
John: Sounds good, I appreciate your help Sarah. I'm looking forward to learning more about the XYZ Widget and seeing how it can benefit our business.
Sarah: Thank you, John. I'll be in touch soon. Have a great day!
John: You too, bye. ```
### Setup our desired schema
Let’s specify our desired output “shape”, as a Pydantic Model.
``` from pydantic import BaseModel, Field from typing import List

class CallSummary(BaseModel): """Data model for a call summary."""
summary: str = Field( description="High-level summary of the call transcript. Should not exceed 3 sentences." ) products: List[str] = Field( description="List of products discussed in the call" ) rep_name: str = Field(description="Name of the sales rep") prospect_name: str = Field(description="Name of the prospect") action_items: List[str] = Field(description="List of action items") ```

### Data extraction with function calling
We can use the `OpenAIPydanticProgram` module in LlamaIndex to make things super easy, simply define a prompt template, and pass in the LLM and pydantic model we’ve definied.
``` from llama_index.program.openai import OpenAIPydanticProgram from llama_index.core import ChatPromptTemplate from llama_index.core.llms import ChatMessage ```

``` prompt = ChatPromptTemplate( message_templates=[ ChatMessage( role="system", content=( "You are an expert assitant for summarizing and extracting insights from sales call transcripts." ), ), ChatMessage( role="user", content=( "Here is the transcript: \n" "------\n" "{transcript}\n" "------" ), ), ] ) program = OpenAIPydanticProgram.from_defaults( output_cls=CallSummary, llm=llm, prompt=prompt, verbose=True, ) ```

``` output = program(transcript=transcript) ```
``` Function call: CallSummary with args: {"summary":"Sarah from XYZ Company called to discuss the new product, the XYZ Widget, which John expressed interest in. Sarah offered to share case studies and schedule a demo. They agreed to review the case studies and set up a time for the demo. The next steps include Sarah sending over information and following up to schedule the demo.","products":["XYZ Widget"],"rep_name":"Sarah","prospect_name":"John","action_items":["Review case studies","Schedule demo"]}
```
We now have the desired structured data, as a Pydantic Model. Quick inspection shows that the results are as we expected.
``` output.dict() ```
``` {'summary': 'Sarah from XYZ Company called to discuss the new product, the XYZ Widget, which John expressed interest in. Sarah offered to share case studies and schedule a demo. They agreed to review the case studies and set up a time for the demo. The next steps include Sarah sending over information and following up to schedule the demo.', 'products': ['XYZ Widget'], 'rep_name': 'Sarah', 'prospect_name': 'John', 'action_items': ['Review case studies', 'Schedule demo']} ```

### Data extraction with JSON mode
Let’s try to do the same with JSON mode, instead of function calling
``` prompt = ChatPromptTemplate( message_templates=[ ChatMessage( role="system", content=( "You are an expert assitant for summarizing and extracting insights from sales call transcripts.\n" "Generate a valid JSON following the given schema below:\n" "{json_schema}" ), ), ChatMessage( role="user", content=( "Here is the transcript: \n" "------\n" "{transcript}\n" "------" ), ), ] ) ```

``` messages = prompt.format_messages( json_schema=CallSummary.schema_json(), transcript=transcript ) ```

We get a vaid JSON, but it’s only regurgitating the schema we specified, and not actually doing the extraction.

``` { "title": "CallSummary", "description": "Data model for a call summary.", "type": "object", "properties": { "summary": { "title": "Summary", "description": "High-level summary of the call transcript. Should not exceed 3 sentences.", "type": "string" }, "products": { "title": "Products", "description": "List of products discussed in the call", "type": "array", "items": { "type": "string" } }, "rep_name": { "title": "Rep Name", "description": "Name of the sales rep", "type": "string" }, "prospect_name": { "title": "Prospect Name", "description": "Name of the prospect", "type": "string" }, "action_items": { "title": "Action Items", "description": "List of action items", "type": "array", "items": { "type": "string" } } }, "required": ["summary", "products", "rep_name", "prospect_name", "action_items"] } ```

Let’s try again by just showing the JSON format we want, instead of specifying the schema
``` import json
prompt = ChatPromptTemplate( message_templates=[ ChatMessage( role="system", content=( "You are an expert assitant for summarizing and extracting insights from sales call transcripts.\n" "Generate a valid JSON in the following format:\n" "{json_example}" ), ), ChatMessage( role="user", content=( "Here is the transcript: \n" "------\n" "{transcript}\n" "------" ), ), ] )

dict_example = { "summary": "High-level summary of the call transcript. Should not exceed 3 sentences.", "products": ["product 1", "product 2"], "rep_name": "Name of the sales rep", "prospect_name": "Name of the prospect", "action_items": ["action item 1", "action item 2"], }

json_example = json.dumps(dict_example) ```
``` messages = prompt.format_messages( json_example=json_example, transcript=transcript ) ```
``` output = llm.chat( messages, response_format={"type": "json_object"} ).message.content ```
Now we are able to get the extracted structured data as we expected.
``` print(output) ```
``` { "summary": "Sarah from XYZ Company called John to discuss the new product, the XYZ Widget, which is designed to streamline workflow and improve productivity. They discussed case studies and scheduling a demo for John and his team. The next steps include Sarah sending over information and following up to schedule the demo.", "products": ["XYZ Widget"], "rep_name": "Sarah", "prospect_name": "John", "action_items": ["Review case studies", "Schedule demo"] } ```

### Quick Takeaways
- Function calling remains easier to use for structured data extraction (especially if you have already specified your schema as e.g. a pydantic model) - While JSON mode enforces the format of the output, it does not help with validation against a specified schema. Directly passing in a schema may not generate expected JSON and may require additional careful formatting and prompting.

[1] https://platform.openai.com/docs/guides/text-generation/json-mode
[2] https://platform.openai.com/docs/guides/function-calling