# developers.llamaindex.ai/python/framework/integrations/llm/pipeshift/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/pipeshift/index.md

--- title: Pipeshift [1] | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-pipeshift ```
``` %pip install llama-index ```
## Basic Usage
Head on to the models [2] section of pipeshift dashboard to see the list of available models.
#### Call `complete` with a prompt

# import os # os.environ["PIPESHIFT_API_KEY"] = "your_api_key"
llm = Pipeshift( model="meta-llama/Meta-Llama-3.1-8B-Instruct", # api_key="<API_KEY>" # alternative way to pass api_key if not specified in environment variable ) res = llm.complete("supercars are ") ```

``` Supercars! Here are some interesting facts and tidbits about these high-performance vehicles:
**What is a Supercar?**
A supercar is a high-performance sports car that is typically characterized by its exceptional speed, handling, and luxury features. Supercars are often designed to be exclusive, rare, and expensive, with prices ranging from hundreds of thousands to millions of dollars.
**Types of Supercars:**
1. **Exotic Supercars**: These are the most exclusive and expensive supercars, often with unique designs and limited production runs. Examples include the Bugatti Chiron, Koenigsegg Agera, and Pagani Huayra. 2. **Hypercars**: These are the fastest and most powerful supercars, often with advanced technology and innovative designs. Examples include the Bugatti Veyron, Hennessey Venom F5, and Rimac C_Two. 3. **Super GTs**: These are high-performance versions of grand tourers, often with a focus on comfort and luxury. Examples include the Ferrari 812 Superfast, Lamborghini Aventador, and Aston Martin DBS Superleggera.
**Notable Supercars:**
1. **Bugatti Chiron**: A hypercar with an 8.0L W16 engine producing 1,479 horsepower. 2. **Koenigsegg Agera RS**: A Swedish supercar with a 5.0L V8 engine producing 1,340 horsepower. 3. **Porsche 918 Spyder**: A hybrid supercar with a 4.6L V8 engine producing 887 horsepower. 4. **Lamborghini Aventador**: A supercar with a 6.5L V12 engine producing 759 horsepower. 5. **Ferrari 488 GTB**: A mid-engined supercar with a 3.9L V8 engine producing 661 horsepower.

**Supercar Features:**
1. **Advanced Materials**: Supercars often feature lightweight materials like carbon fiber, aluminum, and titanium to reduce weight and improve performance. 2. **High-Performance Engines**: Supercars are equipped with powerful engines, often with multiple turbochargers or superchargers, to produce exceptional power and torque. 3. **Advanced Aerodynamics**: Supercars often feature aerodynamic designs, such as spoilers and air intakes, to improve downforce and reduce drag. 4. **Luxury Interiors**: Supercars often come with premium materials ```
#### Call `chat` with a list of messages
``` from llama_index.core.llms import ChatMessage from llama_index.llms.pipeshift import Pipeshift
messages = [ ChatMessage( role="system", content="You are sales person at supercar showroom" ), ChatMessage(role="user", content="why should I pick porsche 911 gt3 rs"), ] res = Pipeshift( model="meta-llama/Meta-Llama-3.1-8B-Instruct", max_tokens=50 ).chat(messages) ```

``` print(res) ```
``` assistant: You're looking for a high-performance vehicle that's going to deliver an unparalleled driving experience, right? Well, let me tell you, the Porsche 911 GT3 RS is the ultimate choice for any driving enthusiast.
First of all, the 911 ```
## Streaming
Using `stream_complete` endpoint
``` from llama_index.llms.pipeshift import Pipeshift
llm = Pipeshift(model="meta-llama/Meta-Llama-3.1-8B-Instruct") resp = llm.stream_complete("porsche GT3 RS is ") ```

``` The Porsche 911 GT3 RS!
The Porsche 911 GT3 RS is a high-performance variant of the Porsche 911 sports car, designed for track driving and enthusiasts. Here are some key features and facts about the Porsche 911 GT3 RS:
**Key Features:**
1. **Engine:** The GT3 RS is powered by a naturally aspirated 4.0-liter flat-six engine, producing 520 horsepower (386 kW) at 8,250 rpm and 346 lb-ft (470 Nm) of torque at 6,250 rpm. 2. **Transmission:** A 7-speed dual-clutch transmission (PDK) is standard, with a manual transmission option available on some models. 3. **Suspension:** The GT3 RS features a rear-axle steering system, which provides improved handling and stability. 4. **Aerodynamics:** The car has a distinctive front splitter, side skirts, and a rear wing, which generate significant downforce and improve high-speed stability. 5. **Weight reduction:** The GT3 RS has a lightweight construction, with a dry weight of around 3,020 pounds (1,370 kg), thanks to the use of lightweight materials such as carbon fiber and aluminum.

**Performance:**
1. **0-60 mph (0-97 km/h):** 3.2 seconds 2. **Top speed:** 193 mph (311 km/h) 3. **Lap time:** The GT3 RS has a lap time of 6:56.4 minutes at the Nürburgring Nordschleife, making it one of the fastest production cars on the track.
**Design and Interior:**
1. **Exterior:** The GT3 RS has a distinctive design, with a more aggressive front bumper, side skirts, and a rear wing. 2. **Interior:** The interior features a sporty design, with a 7-inch touchscreen display, a sport steering wheel, and a range of trim options.
**History:**
1. **First generation (2019):** The first-generation GT3 RS was introduced in 2019, based on the 991.2 911 platform. 2. **Second generation (2022):** The second-generation GT3 RS was introduced in 2022, based on the 992 911 platform.
**Price:**
The price of the Porsche 911 GT3 RS varies depending on the market and trim level, but it typically starts around $175,000 in the United States ```
Using `stream_chat` endpoint
``` from llama_index.llms.pipeshift import Pipeshift from llama_index.core.llms import ChatMessage
llm = Pipeshift(model="meta-llama/Meta-Llama-3.1-8B-Instruct") messages = [ ChatMessage( role="system", content="You are sales person at supercar showroom" ), ChatMessage(role="user", content="how fast can porsche gt3 rs it go?"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` You're interested in the Porsche GT3 RS, eh? That's a beast of a car!
The Porsche 911 GT3 RS is a track-focused variant of the 911, and it's a real rocket ship. It's powered by a 4.0-liter naturally aspirated flat-six engine that produces a whopping 520 horsepower and 346 lb-ft of torque.
As for its top speed, the GT3 RS can reach an electronically limited top speed of 193 mph (311 km/h). But, if you were to remove the limiter, it's rumored to be capable of reaching speeds of up to 200 mph (322 km/h).
But what's even more impressive is its acceleration. The GT3 RS can go from 0-60 mph in just 3.2 seconds, and it can lap the Nürburgring Nordschleife in a blistering 6:40.3 minutes. That's some serious performance right there!
Now, I know what you're thinking: "Is it worth the price tag?" Well, let me tell you, this car is a true driver's car, and it's an investment piece for those who truly appreciate the art of driving. The GT3 RS starts at around $175,000, but trust me, it's worth every penny.
Would you like to take a look at our current inventory? We have a few GT3 RS models available, and I'd be happy to give you a tour. ```

[1] https://pipeshift.com
[2] https://dashboard.pipeshift.com/models