# developers.llamaindex.ai/python/framework/integrations/llm/friendli/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/friendli/index.md

--- title: Friendli | Developer Documentation ---

## Basic Usage
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-friendli ```
``` !pip install llama-index ```
``` %env FRIENDLI_TOKEN=... ```
``` env: FRIENDLI_TOKEN=... ```

# To customize your friendli token, do this # otherwise it will lookup FRIENDLI_TOKEN from your env variable # llm = Friendli(friendli_token="Your personal access token")
llm = Friendli() ```
### Call `chat` with a list of messages
``` from llama_index.core.llms import ChatMessage, MessageRole
message = ChatMessage(role=MessageRole.USER, content="Tell me a joke.") resp = llm.chat([message])

``` assistant: Of course, I'd be happy to share a joke with you! Here it is:

``` resp = llm.stream_chat([message]) for r in resp: print(r.delta, end="") ```
``` Of course, I'd be happy to share a joke with you! Here it is:

Because they make up everything!
I hope that brought a smile to your face. Would you like to hear another joke, or is there something else you'd like to talk about? ```

``` resp = await llm.achat([message])

``` assistant: Sure, here's one:

``` resp = await llm.astream_chat([message]) async for r in resp: print(r.delta, end="") ```
``` Sure, here's one:
Why don't scientists trust atoms?
Because they make up everything! ```
### Call `complete` with a prompt
``` prompt = "Draft a cover letter for a role in software engineering." resp = llm.complete(prompt)

I am writing to express my interest in the Software Engineer position at XYZ Company. As a highly skilled and motivated software engineer with over five years of experience in the field, I am confident that I have the skills and expertise necessary to make a valuable contribution to your team.
Throughout my career, I have gained extensive experience in designing, developing, and maintaining complex software systems. I have a strong background in programming languages such as Java, Python, and C++, and I am proficient in using various software development tools and frameworks. I am also experienced in working with agile methodologies and have a proven track record of delivering high-quality software on time and within budget.
In my current role at ABC Company, I have been responsible for leading a team of software engineers in the development of a mission-critical application used by over 10,000 users. I have successfully managed the entire software development lifecycle, from requirements gathering to deployment, and have implemented various performance optimization techniques to ensure the application runs smoothly even during peak usage times.
I am particularly drawn to XYZ Company because of its reputation as a leader in the software engineering industry. ```
#### Streaming
``` resp = llm.stream_complete(prompt) for r in resp: print(r.delta, end="") ```

Throughout my career, I have gained experience in various programming languages such as Java, Python, and C++. I have also worked on full-stack development projects, where I was responsible for both front-end and back-end development. My experience includes designing and implementing software solutions, collaborating with cross-functional teams, and conducting code reviews.
I am particularly interested in XYZ Company's focus on innovation and cutting-edge technology. I am excited about the opportunity to work with a team that values creativity and continuous learning. I am confident that my skills and experience make me a strong candidate for this role.
Thank you for considering my application. I look forward to the opportunity to discuss my qualifications further.
Sincerely,
[Your Name] ```
#### Async
``` resp = await llm.acomplete(prompt)

I am writing to express my interest in the Software Engineer position at XYZ Company. With a Bachelor's degree in Computer Science and over five years of experience in software development, I am confident in my ability to make a valuable contribution to your team.
Throughout my career, I have gained experience in various programming languages such as Java, Python, and C++. I have also worked on full-stack development projects, where I was responsible for both front-end and back-end development. My experience includes working on cloud-based applications, developing APIs, and integrating third-party services.
I am passionate about writing clean, efficient, and maintainable code. I am also a strong believer in Agile methodologies and have experience working in Agile teams. I am a team player and enjoy collaborating with others to find solutions to complex problems.
In my current role at ABC Company, I have been responsible for leading a team of software engineers in the development of a cloud-based application. I have also been involved in the design and implementation of the company's DevOps practices, which has helped to improve the team's productivity and efficiency. ```
#### Async Streaming
``` resp = await llm.astream_complete(prompt) async for r in resp: print(r.delta, end="") ```
``` Dear Hiring Manager,
I am writing to express my interest in the Software Engineer position at XYZ Corporation. With a Bachelor's degree in Computer Science and over five years of experience in software development, I am confident in my ability to make a valuable contribution to your team.
Throughout my career, I have gained extensive experience in various programming languages such as Java, Python, and C++. I have also worked on developing web applications using frameworks such as React and Angular. My experience includes working on both front-end and back-end development, as well as leading teams to deliver high-quality software products.
At my current role, I have been responsible for designing and implementing software solutions for clients in various industries. I have worked closely with cross-functional teams, including product managers, designers, and quality assurance engineers, to ensure that the final product meets the client's requirements. I have also been involved in the entire software development lifecycle, from requirements gathering to deployment.
I am particularly interested in the Software Engineer role at XYZ Corporation because of the company's reputation for innovation and excellence. I am excited about the opportunity to work with a talented team ```
## Configure Model
``` from llama_index.llms.friendli import Friendli
llm = Friendli(model="llama-2-70b-chat") ```
``` resp = llm.chat([message])
print(resp) ```
``` assistant: Sure, here's a joke for you:
Why couldn't the bicycle stand up by itself?
Because it was two-tired!
I hope that brought a smile to your face! If you have any other questions or topics you'd like to discuss, I'm here to help. ```