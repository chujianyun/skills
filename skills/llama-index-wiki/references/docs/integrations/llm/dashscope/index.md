# developers.llamaindex.ai/python/framework/integrations/llm/dashscope/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/dashscope/index.md

--- title: DashScope LLMS | Developer Documentation ---

In this notebook, we show how to use the DashScope LLM models in LlamaIndex. Check out the DashScope site [1] or the documents [2].
If you’re opening this Notebook on colab, you will need to install LlamaIndex 🦙 and the DashScope Python SDK.
``` !pip install llama-index-llms-dashscope ```
## Basic Usage
You will need to login DashScope [1] an create a API. Once you have one, you can either pass it explicitly to the API, or use the `DASHSCOPE_API_KEY` environment variable.
``` %env DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY ```
``` env: DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY ```
``` import os

os.environ["DASHSCOPE_API_KEY"] = "YOUR_DASHSCOPE_API_KEY" ```
#### Initialize `DashScope` Object
``` from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels

dashscope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_MAX) ```
#### Call `complete` with a prompt
``` resp = dashscope_llm.complete("How to make cake?") print(resp) ```

``` Making a basic vanilla cake from scratch is a simple and enjoyable process. Here's a step-by-step recipe for a classic vanilla sponge cake:

**Ingredients:** - 2 cups (240g) all-purpose flour - 1 ¾ cups (350g) granulated sugar - 3 teaspoons baking powder - ½ teaspoon salt - ⅓ cup (80g) unsalted butter, softened - 1 cup (240ml) whole milk, at room temperature - 2 teaspoons pure vanilla extract - 3 large eggs, at room temperature

1. **Preheat the Oven**: Preheat your oven to 350°F (175°C). Grease two 9-inch round cake pans with butter or cooking spray, then line the bottoms with parchment paper.

2. **Dry Ingredients**: In a large mixing bowl, sift together the flour, sugar, baking powder, and salt. Make sure everything is well combined.

3. **Cream the Butter and Sugar**: In another large bowl, beat the softened butter until creamy. Gradually add the sugar and continue beating until light and fluffy, about 3-4 minutes.

4. **Add Eggs and Vanilla**: Beat in the eggs one at a time, making sure each egg is fully incorporated before adding the next. Mix in the vanilla extract.

5. **Combine Wet and Dry**: With the mixer on low speed, alternately add the dry ingredients mixture and milk into the wet mixture in three parts, starting and ending with the flour mixture. Be careful not to overmix; stop as soon as the ingredients are just combined.

6. **Pour and Bake**: Divide the batter evenly between the prepared pans. Smooth the tops with a spatula. Bake for 25-30 minutes, or until a toothpick inserted into the center of each cake comes out clean.

7. **Cool the Cake**: Remove cakes from the oven and let them cool in their pans for about 10 minutes. Then, remove from the pans and transfer onto wire racks to cool completely.

8. **Frosting and Assembly**: Once cooled, you can frost and assemble the cake with your favorite frosting, such as buttercream. Place one cake layer on a plate or cake stand, spread frosting over the top, then place the second cake layer on top. Frost the top and sides of the cake as desired.

Remember, this is a basic vanilla cake recipe that can be customized with different flavors or toppings. Always read through the entire recipe before beginning and ensure all ingredients are at room temperature for best results. ```
#### Call \`stream\_complete“ with a prompt
``` responses = dashscope_llm.stream_complete("How to make cake?") for response in responses: print(response.delta, end="") ```

``` Baking a cake can be a fun and rewarding experience! Here's a simple recipe for a classic vanilla sponge cake:

**Ingredients:** - 2 cups (240g) all-purpose flour - 2 teaspoons baking powder - 1/2 teaspoon salt - 1 cup (2 sticks or 226g) unsalted butter, at room temperature - 1 3/4 cups (350g) granulated sugar - 4 large eggs, at room temperature - 2 teaspoons pure vanilla extract - 1 1/4 cups (300ml) whole milk, at room temperature

1. **Preheat the Oven**: Preheat your oven to 350°F (175°C). Grease two 9-inch (23cm) round cake pans with butter or cooking spray, then line the bottoms with parchment paper.

2. **Mix Dry Ingredients**: In a medium bowl, sift together the flour, baking powder, and salt. Set aside.

3. **Cream Butter and Sugar**: In a large mixing bowl or using a stand mixer, cream the butter until it is light and fluffy. Gradually add in the sugar and continue beating until the mixture is pale and well-combined, about 3-5 minutes.

4. **Add Eggs and Vanilla**: Beat in the eggs one at a time, making sure each egg is fully incorporated before adding the next. Add the vanilla extract and mix well.

5. **Combine Wet and Dry**: With the mixer on low speed, alternately add the dry ingredients mixture and the milk to the butter-sugar mixture, starting and ending with the dry ingredients. Mix just until combined; do not overmix.

6. **Pour and Bake**: Divide the batter evenly between the prepared pans. Smooth the tops with a spatula. Bake for 25-30 minutes or until a toothpick inserted into the center of the cakes comes out clean.

7. **Cool and Frost**: Remove the cakes from the oven and let them cool in their pans for about 10 minutes. Then, remove the cakes from the pans and transfer to a wire rack to cool completely. Once cooled, you can frost and decorate as desired.

For frosting, you could make a basic buttercream by beating softened butter with powdered sugar, vanilla, and a little milk until smooth and spreadable.

Remember that every oven behaves differently, so keep an eye on your cake while it bakes. Enjoy your homemade cake!

**Optional Steps:** - For extra flavor, you can add lemon zest, cocoa powder, or other flavorings to the batter. - Level the cakes with a serrated knife before stacking and frosting to ensure an even surface. - Chill the cakes before frosting to help prevent crumbs from getting mixed into the frosting. ```

#### Call `chat` with a list of messages
``` from llama_index.core.base.llms.types import MessageRole, ChatMessage

messages = [ ChatMessage( role=MessageRole.SYSTEM, content="You are a helpful assistant." ), ChatMessage(role=MessageRole.USER, content="How to make cake?"), ] resp = dashscope_llm.chat(messages) print(resp) ```
``` assistant: Baking a cake from scratch is a fun and rewarding experience! Here's a simple recipe for a classic vanilla cake:

**Ingredients:** - 2 and 1/4 cups (280g) all-purpose flour - 1 and 1/2 cups (300g) granulated sugar - 3 teaspoons baking powder - 1/2 teaspoon salt - 1 cup (2 sticks or 226g) unsalted butter, at room temperature - 1 cup (240ml) whole milk, at room temperature - 4 large eggs, at room temperature - 2 teaspoons pure vanilla extract

**For the frosting (optional):** - 1 cup (2 sticks or 226g) unsalted butter, softened - 4 cups (480g) powdered sugar - 2 teaspoons vanilla extract - 3-5 tablespoons milk

1. **Preheat Oven and Prepare Pan**: Preheat your oven to 350°F (175°C). Grease two 9-inch round cake pans with butter or cooking spray. Dust them lightly with flour and tap out any excess.

2. **Mix Dry Ingredients**: In a large mixing bowl, whisk together the flour, sugar, baking powder, and salt until well combined.

3. **Cream Butter and Sugar**: In another large bowl, using an electric mixer on medium speed, beat the butter until creamy. Gradually add in the sugar and continue beating until light and fluffy, about 3-5 minutes.

4. **Add Eggs and Vanilla**: Beat in the eggs one at a time, making sure each egg is fully incorporated before adding the next. Stir in the vanilla extract.

5. **Alternate Wet and Dry Ingredients**: With the mixer on low speed, alternately add the dry ingredients mixture and milk to the wet mixture, starting and ending with the dry ingredients. Mix until just combined; do not overmix.

6. **Pour Batter and Bake**: Divide the batter evenly between the prepared pans. Smooth the tops. Bake for 25-30 minutes or until a toothpick inserted into the center of the cakes comes out clean.

7. **Cool Cakes**: Remove cakes from the oven and let them cool in the pans for about 10 minutes. Then, carefully invert the cakes onto wire racks to cool completely.

8. **Make Frosting (Optional)**: In a separate bowl, beat butter until smooth. Gradually add powdered sugar, vanilla extract, and enough milk to reach your desired consistency. Beat until smooth and creamy.

9. **Assemble Cake**: Once the cakes are cooled, place one layer on a plate or cake stand. Spread a thick layer of frosting on top. Place the second cake layer on top and cover the entire cake with the remaining frosting.

Remember, this is just a basic recipe. You can customize it by adding food coloring, different extracts, or mix-ins like chocolate chips or fruit. Always be mindful of adjusting baking times if you're using different sized pans. ```
#### Using `stream_chat`
``` responses = dashscope_llm.stream_chat(messages) for response in responses: print(response.delta, end="") ```

``` Baking a cake from scratch is a fun and delicious activity! Here's a simple recipe for a classic vanilla cake:

**Ingredients:** - 2 cups (240g) all-purpose flour - 2 teaspoons baking powder - 1/2 teaspoon baking soda - 1/2 teaspoon salt - 1 cup (2 sticks or 226g) unsalted butter, at room temperature - 1 3/4 cups (350g) granulated sugar - 4 large eggs, at room temperature - 2 teaspoons pure vanilla extract - 1 cup (240ml) whole milk, at room temperature

**Instructions:**

1. **Preheat the Oven**: Preheat your oven to 350°F (175°C). Grease two 9-inch round cake pans with butter or cooking spray and line the bottoms with parchment paper.

2. **Dry Ingredients Mix**: In a medium bowl, sift together the flour, baking powder, baking soda, and salt. Set aside.

3. **Creaming Butter and Sugar**: In a large mixing bowl or using a stand mixer, beat the softened butter until creamy. Gradually add in the sugar and continue beating until light and fluffy, about 3-5 minutes.

4. **Egg Incorporation**: Add the eggs one at a time, beating well after each addition. Stir in the vanilla extract.

5. **Dry & Wet Ingredients Combine**: Add the dry ingredients mixture to the wet ingredients in three parts, alternating with the milk, beginning and ending with the dry ingredients. Mix on low speed just until combined. Do not overmix; a few lumps are okay.

6. **Bake**: Divide the batter evenly between the prepared pans. Smooth out the tops with a spatula. Bake for 25-30 minutes or until a toothpick inserted into the center of the cakes comes out clean.

7. **Cool**: Remove the cakes from the oven and let them cool in their pans for about 10 minutes. Then, invert onto wire racks to cool completely.

8. **Frosting and Assembly**: Once cooled, you can frost the cake with your choice of frosting - such as a classic buttercream. Place one cake layer on a plate or cake stand, spread frosting over it, then place the second layer on top. Frost the top and sides of the cake as desired.

Enjoy your homemade vanilla cake!

**Note:** You can customize this basic recipe by adding food coloring, different flavor extracts, or incorporating mix-ins like chocolate chips or fruit. Adjust baking times if you're making cupcakes or larger cakes. ```
#### Multiple rounds conversation.
``` messages = [ ChatMessage( role=MessageRole.SYSTEM, content="You are a helpful assistant." ), ChatMessage(role=MessageRole.USER, content="How to make cake?"), ] # first round resp = dashscope_llm.chat(messages) print(resp)

# add response to messages. messages.append( ChatMessage(role=MessageRole.ASSISTANT, content=resp.message.content) )

messages.append( ChatMessage(role=MessageRole.USER, content="How to make it without sugar") ) # second round resp = dashscope_llm.chat(messages) print(resp) ```
``` assistant: Baking a cake is a fun and creative process! Here's a simple recipe for a classic vanilla sponge cake. You will need:

Ingredients: - 1 and 1/2 cups (190g) all-purpose flour - 1 cup (200g) granulated sugar - 2 teaspoons baking powder - 1/2 teaspoon salt - 1/2 cup (1 stick or 113g) unsalted butter, softened - 2 large eggs, room temperature - 2 teaspoons pure vanilla extract - 3/4 cup (180ml) whole milk, at room temperature

For the frosting (optional): - 1 cup (226g) unsalted butter, softened - 4 cups (400g) powdered sugar - 2 tablespoons heavy cream or milk - 2 teaspoons vanilla extract

2. In a medium bowl, whisk together the flour, sugar, baking powder, and salt until well combined.

3. In a large mixing bowl, beat the softened butter until creamy. Gradually add in the sugar and continue beating until light and fluffy, about 3 minutes.

To make the frosting (if desired):

1. In a large mixing bowl, beat the softened butter until smooth. 2. Gradually add in the powdered sugar, mixing well after each addition. 3. Stir in the heavy cream or milk and vanilla extract. Beat on high speed until the frosting is smooth and creamy.

Assembling the Cake:

1. Once the cakes are cooled, place one layer on a plate or cake stand. Spread a generous amount of frosting over the top. 2. Place the second cake layer on top of the frosting, bottom-side up to create a flat surface. 3. Frost the top and sides of the cake with the remaining frosting as desired.

Enjoy your homemade vanilla sponge cake!

Remember, this is just a basic recipe and you can customize it by adding food coloring, different flavorings, or toppings to suit your taste. Always follow the specific instructions for more complex recipes or those that use different ingredients like chocolate or fruit. assistant: To make a cake without sugar, you can substitute sugar with alternative natural sweeteners. Here's a recipe for a simple sugar-free vanilla sponge cake using honey as a sweetener:

Ingredients: - 1 and 1/2 cups (190g) all-purpose flour - 3/4 cup (225g) honey (use mild-flavored honey like clover or acacia) - 2 teaspoons baking powder - 1/2 teaspoon salt - 1/2 cup (1 stick or 113g) unsalted butter, softened - 2 large eggs, room temperature - 2 teaspoons pure vanilla extract - 3/4 cup (180ml) whole milk, at room temperature

Instructions:

1. Preheat your oven to 350°F (175°C). Grease two 9-inch round cake pans with butter or cooking spray, then line the bottoms with parchment paper.

2. In a medium bowl, whisk together the flour, baking powder, and salt.

3. In a large mixing bowl, beat the softened butter and honey until light and fluffy, about 3-4 minutes. Honey is more liquid than sugar so it may take a little longer to incorporate.

4. Add in the eggs one at a time, beating well after each addition. Mix in the vanilla extract.

5. With the mixer on low speed, alternate adding the flour mixture and milk, starting and ending with the flour mixture. Beat until just combined, being careful not to overmix.

6. Divide the batter evenly between the prepared pans.

7. Bake for 25 to 30 minutes or until a toothpick inserted into the center of each cake comes out clean.

8. Let the cakes cool in their pans for 10 minutes, then remove them from the pans and place them onto wire racks to cool completely.

Note: Baking with honey can result in a moister cake that browns faster. You might need to adjust the baking time accordingly and monitor the color of the cake while it bakes.

Keep in mind that honey is still a form of carbohydrate and has calories. For a completely sugar-free option, you could use erythritol or stevia-based sweeteners, but be aware that these will affect the texture and taste differently compared to traditional sugar or honey. Adjust the amount according to the specific sweetener’s conversion ratio to sugar, and follow the instructions provided by the manufacturer.

For frosting, you can also create a sugar-free version using cream cheese or whipped cream sweetened with a sugar substitute, if desired. ```

[1] https://dashscope.aliyun.com/
[2] https://help.aliyun.com/zh/dashscope/developer-reference/api- details