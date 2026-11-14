# Build a SQL agent

## Overview

In this tutorial, you will learn how to build an agent that can answer questions about a SQL database using LangChain [agents](../../../Core%20components/Agents.md).

At a high level, the agent will:

1. Fetch the available tables and schemas from the database
2. Decide which tables are relevant to the question
3. Fetch the schemas for the relevant tables
4. Generate a query based on the question and information from the schemas
5. Double-check the query for common mistakes using an LLM
6. Execute the query and return the results
7. Correct mistakes surfaced by the database engine until the query is successful
8. Formulate a response based on the results

> [!WARNING]
>
> Building Q\&A systems of SQL databases requires executing model-generated SQL queries. There are inherent risks in doing this. Make sure that your database connection permissions are always scoped as narrowly as possible for your agent's needs. This will mitigate, though not eliminate, the risks of building a model-driven system.

### Concepts

The following tutorial covers the following concepts:

* [Tools](../../../Core%20components/Tools.md) for reading from SQL databases
* LangChain [agents](../../../Core%20components/Agents.md)
* [Human-in-the-loop](../../../Advanced%20usage/Human-in-the-loop.md) processes

## Setup

**1. Install dependencies**

```bash pip
pip install langchain langgraph
```

**2. Set up LangSmith**

Set up [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-sql-agent) to inspect what is happening inside your chain or agent. Then set the following environment variables:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

## Build your SQL agent

**1. Select an LLM**

Select a model that supports [tool-calling](https://docs.langchain.com/oss/python/integrations/providers/overview.md):

> [tab] OpenAI
>
> 👉 Read the [OpenAI chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/openai/)
>
> ```bash pip
> pip install -U "langchain[openai]"
> ```
>
> ```bash uv
> uv add "langchain[openai]"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["OPENAI_API_KEY"] = "sk-..."
>
> model = init_chat_model("gpt-6.1-sol")
> ```
>
> ```python Model Class
> import os
> from langchain_openai import ChatOpenAI
>
> os.environ["OPENAI_API_KEY"] = "sk-..."
>
> model = ChatOpenAI(model="gpt-6.1-sol")
> ```

> [tab] Anthropic
>
> 👉 Read the [Anthropic chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/anthropic/)
>
> ```bash pip
> pip install -U "langchain[anthropic]"
> ```
>
> ```bash uv
> uv add "langchain[anthropic]"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["ANTHROPIC_API_KEY"] = "sk-..."
>
> model = init_chat_model("claude-sonnet-4-6")
> ```
>
> ```python Model Class
> import os
> from langchain_anthropic import ChatAnthropic
>
> os.environ["ANTHROPIC_API_KEY"] = "sk-..."
>
> model = ChatAnthropic(model="claude-sonnet-4-6")
> ```

> [tab] Azure
>
> 👉 Read the [Azure chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/azure_chat_openai/)
>
> ```bash pip
> pip install -U "langchain[openai]"
> ```
>
> ```bash uv
> uv add "langchain[openai]"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["AZURE_OPENAI_API_KEY"] = "..."
> os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
> os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
>
> model = init_chat_model(
>     "azure_openai:gpt-6.1-sol",
>     azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
> )
> ```
>
> ```python Model Class
> import os
> from langchain_openai import AzureChatOpenAI
>
> os.environ["AZURE_OPENAI_API_KEY"] = "..."
> os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
> os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
>
> model = AzureChatOpenAI(
>     model="gpt-6.1-sol",
>     azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
> )
> ```

> [tab] Google Gemini
>
> 👉 Read the [Google GenAI chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai/)
>
> ```bash pip
> pip install -U "langchain[google-genai]"
> ```
>
> ```bash uv
> uv add "langchain[google-genai]"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["GOOGLE_API_KEY"] = "..."
>
> model = init_chat_model("google_genai:gemini-4-hydrogen")
> ```
>
> ```python Model Class
> import os
> from langchain_google_genai import ChatGoogleGenerativeAI
>
> os.environ["GOOGLE_API_KEY"] = "..."
>
> model = ChatGoogleGenerativeAI(model="gemini-4-hydrogen")
> ```

> [tab] AWS Bedrock
>
> 👉 Read the [AWS Bedrock chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/bedrock/)
>
> ```bash pip
> pip install -U "langchain[aws]"
> ```
>
> ```bash uv
> uv add "langchain[aws]"
> ```
>
> ```python init_chat_model
> from langchain.chat_models import init_chat_model
>
> # Follow the steps here to configure your credentials:
> # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
>
> model = init_chat_model(
>     "us.anthropic.claude-sonnet-4-6",
>     model_provider="bedrock_converse",
> )
> ```
>
> ```python Model Class
> from langchain_aws import ChatBedrock
>
> model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
> ```

> [tab] HuggingFace
>
> 👉 Read the [HuggingFace chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/huggingface/)
>
> ```bash pip
> pip install -U "langchain[huggingface]"
> ```
>
> ```bash uv
> uv add "langchain[huggingface]"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."
>
> model = init_chat_model(
>     "microsoft/Phi-3-mini-4k-instruct",
>     model_provider="huggingface",
>     temperature=0.7,
>     max_tokens=1024,
> )
> ```
>
> ```python Model Class
> import os
> from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
>
> os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."
>
> llm = HuggingFaceEndpoint(
>     repo_id="microsoft/Phi-3-mini-4k-instruct",
>     temperature=0.7,
>     max_length=1024,
> )
> model = ChatHuggingFace(llm=llm)
> ```

> [tab] OpenRouter
>
> 👉 Read the [OpenRouter chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/openrouter/)
>
> ```bash pip
> pip install -U "langchain-openrouter"
> ```
>
> ```bash uv
> uv add "langchain-openrouter"
> ```
>
> ```python init_chat_model
> import os
> from langchain.chat_models import init_chat_model
>
> os.environ["OPENROUTER_API_KEY"] = "sk-..."
>
> model = init_chat_model(
>     "auto",
>     model_provider="openrouter",
> )
> ```
>
> ```python Model Class
> import os
> from langchain_openrouter import ChatOpenRouter
>
> os.environ["OPENROUTER_API_KEY"] = "sk-..."
>
> model = ChatOpenRouter(model="auto")
> ```

The output shown in the examples below used OpenAI.

**2. Configure the database**

You will be creating a [SQLite database](https://www.sqlitetutorial.net/sqlite-sample-database/) for this tutorial. SQLite is a lightweight database that is easy to set up and use. We will be loading the `chinook` database, which is a sample database that represents a digital media store.

For convenience, we have hosted the database (`Chinook.db`) on a public GCS bucket.

```python
import pathlib
import requests

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
```

We will use Python's built-in `sqlite3` module to interact with the database:

```python
import sqlite3

con = sqlite3.connect("Chinook.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

print("Dialect: sqlite")
print(f"Available tables: {tables}")

cursor.execute("SELECT * FROM Artist LIMIT 5;")
print(f"Sample output: {cursor.fetchall()}")
con.close()
```

```
Dialect: sqlite
Available tables: ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
Sample output: [(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains')]
```

**3. Add tools for database interactions**

> [!WARNING]
>
> The following database tools are minimal wrappers for demonstration purposes only. They are not intended to be secure or used in production. Use narrowly scoped database permissions and add application-specific validation before executing model-generated SQL.

We can implement database [tools](../../../Core%20components/Tools.md) as thin wrappers using the `@tool` decorator from `langchain.tools`:

```python
import sqlite3
from langchain.tools import tool

# Below are minimal tools for demonstration purposes.
# They are not intended to be secure or for production use.

@tool
def sql_db_list_tables() -> str:
    """Input is an empty string, output is a comma-separated list of tables in the database."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
        return ", ".join(tables)
    finally:
        con.close()

@tool
def sql_db_schema(table_names: str) -> str:
    """Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3"""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        valid_tables = {row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")}
        results = []
        for table in table_names.split(","):
            table = table.strip()
            if table not in valid_tables:
                results.append(f"Error: table_names {{{table!r}}} not found in database")
                continue
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            schema_row = cursor.fetchone()
            if schema_row:
                results.append(schema_row[0])
                try:
                    quoted_table = '"' + table.replace('"', '""') + '"'
                    cursor.execute(f"SELECT * FROM {quoted_table} LIMIT 3;")
                    rows = cursor.fetchall()
                    if rows:
                        col_names = [description[0] for description in cursor.description]
                        results.append(
                            f"/*\n3 rows from {table} table:\n"
                            + "\t".join(col_names)
                            + "\n"
                            + "\n".join("\t".join(str(x) for x in row) for row in rows)
                            + "\n*/"
                        )
                except Exception as e:
                    results.append(f"Error fetching sample rows: {e}")
        return "\n\n".join(results)
    finally:
        con.close()

@tool
def sql_db_query(query: str) -> str:
    """Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return str(res)
    except Exception as e:
        return f"Error: {e}"
    finally:
        con.close()

@tool
def sql_db_query_checker(query: str) -> str:
    """Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with sql_db_query!"""
    trigger_prompt = """{query}
Double check the sqlite query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only.

SQL Query: """.format(query=query)

    response = model.invoke(trigger_prompt)
    return response.text.strip()

tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_checker]

# Use a distinct loop variable so it does not shadow the `tool` decorator.
for t in tools:
    print(f"{t.name}: {t.description}\n")
```

```
sql_db_query: Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.

sql_db_schema: Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3

sql_db_list_tables: Input is an empty string, output is a comma-separated list of tables in the database.

sql_db_query_checker: Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with sql_db_query!
```

**4. Create the agent**

Use [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) to build a [ReAct agent](https://arxiv.org/pdf/2210.03629) with minimal code. The agent will interpret the request and generate a SQL command, which the tools will execute. If the command has an error, the error message is returned to the model. The model can then examine the original request and the new error message and generate a new command. This can continue until the LLM generates the command successfully or reaches an end count. This pattern of providing a model with feedback - error messages in this case - is very powerful.

Initialize the agent with a descriptive system prompt to customize its behavior:

```python
system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="sqlite",
    top_k=5,
)
```

Now, create an agent with the model, tools, and prompt:

```python
from langchain.agents import create_agent


agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
```

**5. Run the agent**

Run the agent on a sample query and observe its behavior:

```python
question = "Which genre on average has the longest tracks?"

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": question}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output
```

```
================================ Human Message =================================

Which genre on average has the longest tracks?
================================== Ai Message ==================================
Tool Calls:
  sql_db_list_tables (call_BQsWg8P65apHc8BTJ1NPDvnM)
 Call ID: call_BQsWg8P65apHc8BTJ1NPDvnM
  Args:
================================= Tool Message =================================
Name: sql_db_list_tables

Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track
================================== Ai Message ==================================
Tool Calls:
  sql_db_schema (call_i89tjKECFSeERbuACYm4w0cU)
 Call ID: call_i89tjKECFSeERbuACYm4w0cU
  Args:
    table_names: Track, Genre
================================= Tool Message =================================
Name: sql_db_schema


CREATE TABLE "Genre" (
	"GenreId" INTEGER NOT NULL,
	"Name" NVARCHAR(120),
	PRIMARY KEY ("GenreId")
)

/*
3 rows from Genre table:
GenreId	Name
1	Rock
2	Jazz
3	Metal
*/


CREATE TABLE "Track" (
	"TrackId" INTEGER NOT NULL,
	"Name" NVARCHAR(200) NOT NULL,
	"AlbumId" INTEGER,
	"MediaTypeId" INTEGER NOT NULL,
	"GenreId" INTEGER,
	"Composer" NVARCHAR(220),
	"Milliseconds" INTEGER NOT NULL,
	"Bytes" INTEGER,
	"UnitPrice" NUMERIC(10, 2) NOT NULL,
	PRIMARY KEY ("TrackId"),
	FOREIGN KEY("MediaTypeId") REFERENCES "MediaType" ("MediaTypeId"),
	FOREIGN KEY("GenreId") REFERENCES "Genre" ("GenreId"),
	FOREIGN KEY("AlbumId") REFERENCES "Album" ("AlbumId")
)

/*
3 rows from Track table:
TrackId	Name	AlbumId	MediaTypeId	GenreId	Composer	Milliseconds	Bytes	UnitPrice
1	For Those About To Rock (We Salute You)	1	1	1	Angus Young, Malcolm Young, Brian Johnson	343719	11170334	0.99
2	Balls to the Wall	2	2	1	U. Dirkschneider, W. Hoffmann, H. Frank, P. Baltes, S. Kaufmann, G. Hoffmann	342562	5510424	0.99
3	Fast As a Shark	3	2	1	F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman	230619	3990994	0.99
*/
================================== Ai Message ==================================
Tool Calls:
  sql_db_query_checker (call_G64yYm6R6UauiVPCXJZMA49b)
 Call ID: call_G64yYm6R6UauiVPCXJZMA49b
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query_checker

SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_AnO3SrhD0ODJBxh6dHMwvHwZ)
 Call ID: call_AnO3SrhD0ODJBxh6dHMwvHwZ
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

On average, the genre with the longest tracks is "Sci Fi & Fantasy" with an average track length of approximately 2,911,783 milliseconds. This is followed by "Science Fiction," "Drama," "TV Shows," and "Comedy."
```

The agent correctly wrote a query, checked the query, and ran it to inform its final response.

> [!NOTE]
>
> You can inspect all aspects of the above run, including steps taken, tools invoked, what prompts were seen by the LLM, and more in the [LangSmith trace](https://smith.langchain.com/public/cd2ce887-388a-4bb1-a29d-48208ce50d15/r).

**6. (Optional) Use Studio**

[Studio](https://docs.langchain.com/langsmith/studio.md) provides a "client side" loop as well as memory so you can run this as a chat interface and query the database. You can ask questions like "Tell me the scheme of the database" or "Show me the invoices for the 5 top customers". You will see the SQL command that is generated and the resulting output. The details of how to get that started are below.

> [accordion] Run your agent in Studio
>
> In addition to the previously mentioned packages, you will need to:
>
> ```shell
> pip install -U langgraph-cli[inmem]>=0.4.0
> ```
>
> In directory you will run in, you will need a `langgraph.json` file with the following contents:
>
> ```json
> {
>   "dependencies": ["."],
>   "graphs": {
>       "agent": "./sql_agent.py:agent",
>       "graph": "./sql_agent_langgraph.py:graph"
>   },
>   "env": ".env"
> }
> ```
>
> Create a file `sql_agent.py` and insert this:
>
> ```python
> # sql_agent.py for studio
> import pathlib
> import sqlite3
>
> import requests
> from langchain.agents import create_agent
> from langchain.chat_models import init_chat_model
> from langchain.tools import tool
>
> # Initialize an LLM
> model = init_chat_model("openai:gpt-6.1-sol")
>
> # Get the database, store it locally
> url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
> local_path = pathlib.Path("Chinook.db")
>
> if local_path.exists():
>     print(f"{local_path} already exists, skipping download.")
> else:
>     response = requests.get(url, timeout=60)
>     if response.status_code == 200:
>         local_path.write_bytes(response.content)
>         print(f"File downloaded and saved as {local_path}")
>     else:
>         print(f"Failed to download the file. Status code: {response.status_code}")
>
> # Below are minimal tools for demonstration purposes.
>
> @tool
> def sql_db_list_tables() -> str:
>     """Input is an empty string, output is a comma-separated list of tables in the database."""
>     con = sqlite3.connect("Chinook.db")
>     try:
>         cursor = con.cursor()
>         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
>         tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
>         return ", ".join(tables)
>     finally:
>         con.close()
>
> @tool
> def sql_db_schema(table_names: str) -> str:
>     """Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
>     Be sure that the tables actually exist by calling sql_db_list_tables first!
>     Example Input: table1, table2, table3"""
>     con = sqlite3.connect("Chinook.db")
>     try:
>         cursor = con.cursor()
>         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
>         valid_tables = {row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")}
>         results = []
>         for table in table_names.split(","):
>             table = table.strip()
>             if table not in valid_tables:
>                 results.append(f"Error: table_names {{{table!r}}} not found in database")
>                 continue
>             cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
>             schema_row = cursor.fetchone()
>             if schema_row:
>                 results.append(schema_row[0])
>                 try:
>                     quoted_table = '"' + table.replace('"', '""') + '"'
>                     cursor.execute(f"SELECT * FROM {quoted_table} LIMIT 3;")
>                     rows = cursor.fetchall()
>                     if rows:
>                         col_names = [description[0] for description in cursor.description]
>                         results.append(
>                             f"/*\n3 rows from {table} table:\n"
>                             + "\t".join(col_names)
>                             + "\n"
>                             + "\n".join("\t".join(str(x) for x in row) for row in rows)
>                             + "\n*/"
>                         )
>                 except Exception as e:
>                     results.append(f"Error fetching sample rows: {e}")
>         return "\n\n".join(results)
>     finally:
>         con.close()
>
> @tool
> def sql_db_query(query: str) -> str:
>     """Input to this tool is a detailed and correct SQL query, output is a result from the database.
>     If the query is not correct, an error message will be returned.
>     If an error is returned, rewrite the query, check the query, and try again.
>     If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields."""
>     con = sqlite3.connect("Chinook.db")
>     try:
>         cursor = con.cursor()
>         cursor.execute(query)
>         res = cursor.fetchall()
>         return str(res)
>     except Exception as e:
>         return f"Error: {e}"
>     finally:
>         con.close()
>
> @tool
> def sql_db_query_checker(query: str) -> str:
>     """Use this tool to double check if your query is correct before executing it.
>     Always use this tool before executing a query with sql_db_query!"""
>     trigger_prompt = """{query}
> Double check the sqlite query above for common mistakes, including:
> - Using NOT IN with NULL values
> - Using UNION when UNION ALL should have been used
> - Using BETWEEN for exclusive ranges
> - Data type mismatch in predicates
> - Properly quoting identifiers
> - Using the correct number of arguments for functions
> - Casting to the correct data type
> - Using the proper columns for joins
>
> If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.
>
> Output the final SQL query only.
>
> SQL Query: """.format(query=query)
>
>     response = model.invoke(trigger_prompt)
>     return response.text.strip()
>
> tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_checker]
>
> # Use a distinct loop variable so it does not shadow the `tool` decorator.
> for t in tools:
>     print(f"{t.name}: {t.description}\n")
>
> # Use create_agent
> system_prompt = """
> You are an agent designed to interact with a SQL database.
> Given an input question, create a syntactically correct {dialect} query to run,
> then look at the results of the query and return the answer. Unless the user
> specifies a specific number of examples they wish to obtain, always limit your
> query to at most {top_k} results.
>
> You can order the results by a relevant column to return the most interesting
> examples in the database. Never query for all the columns from a specific table,
> only ask for the relevant columns given the question.
>
> You MUST double check your query before executing it. If you get an error while
> executing a query, rewrite the query and try again.
>
> DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
> database.
>
> To start you should ALWAYS look at the tables in the database to see what you
> can query. Do NOT skip this step.
>
> Then you should query the schema of the most relevant tables.
> """.format(
>     dialect="sqlite",
>     top_k=5,
> )
>
> agent = create_agent(
>     model,
>     tools,
>     system_prompt=system_prompt,
> )
> ```

**7. Implement human-in-the-loop review**

It can be prudent to check the agent's SQL queries before they are executed for any unintended actions or inefficiencies.

LangChain agents feature support for built-in [human-in-the-loop middleware](../../../Advanced%20usage/Human-in-the-loop.md) to add oversight to agent tool calls. Let's configure the agent to pause for human review on calling the `sql_db_query` tool:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver # [!code highlight]


agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    middleware=[ # [!code highlight]
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={"sql_db_query": True}, # [!code highlight]
            description_prefix="Tool execution pending approval", # [!code highlight]
        ), # [!code highlight]
    ], # [!code highlight]
    checkpointer=InMemorySaver(), # [!code highlight]
)
```

> [!NOTE]
>
> We've added a [checkpointer](../../../Core%20components/Short-term%20memory.md) to our agent to allow execution to be paused and resumed. See the [human-in-the-loop guide](../../../Advanced%20usage/Human-in-the-loop.md) for detalis on this as well as available middleware configurations.

On running the agent, it will now pause for review before executing the `sql_db_query` tool:

```python
question = "Which genre on average has the longest tracks?"
config = {"configurable": {"thread_id": "1"}} # [!code highlight]

stream = agent.stream_events( # [!code highlight]
    {"messages": [{"role": "user", "content": question}]},
    config, # [!code highlight]
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted: # [!code highlight]
    print("INTERRUPTED:") # [!code highlight]
    interrupt = stream.interrupts[0] # [!code highlight]
    for request in interrupt.value["action_requests"]: # [!code highlight]
        print(request["description"]) # [!code highlight]
```

```
...

INTERRUPTED:
Tool execution pending approval

Tool: sql_db_query
Args: {'query': 'SELECT g.Name AS Genre, AVG(t.Milliseconds) AS AvgTrackLength FROM Track t JOIN Genre g ON t.GenreId = g.GenreId GROUP BY g.Name ORDER BY AvgTrackLength DESC LIMIT 1;'}
```

We can resume execution, in this case accepting the query, using [Command](https://docs.langchain.com/oss/python/langgraph/graph-api-send-command.md#combine-control-flow-and-state-updates-with-command):

```python
from langgraph.types import Command # [!code highlight]

stream = agent.stream_events( # [!code highlight]
    Command(resume={"decisions": [{"type": "approve"}]}), # [!code highlight]
    config,
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted:
    print("INTERRUPTED:")
    interrupt = stream.interrupts[0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])
```

```
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_7oz86Epg7lYRqi9rQHbZPS1U)
 Call ID: call_7oz86Epg7lYRqi9rQHbZPS1U
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AvgDuration FROM Track JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AvgDuration DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

The genre with the longest average track length is "Sci Fi & Fantasy" with an average duration of about 2,911,783 milliseconds, followed by "Science Fiction" and "Drama."
```

Refer to the [human-in-the-loop guide](../../../Advanced%20usage/Human-in-the-loop.md) for details.

## Next steps

For deeper customization, check out [this tutorial](https://docs.langchain.com/oss/python/langgraph/sql-agent.md) for implementing a SQL agent directly using LangGraph primitives.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/sql-agent.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
