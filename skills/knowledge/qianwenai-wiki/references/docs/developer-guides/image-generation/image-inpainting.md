> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像局部重绘

> 使用wanx-x-painting模型，根据原始图片、涂抹图和文本描述进行图像局部重绘

<Warning>
  - wanx-x-painting 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[图像编辑-千问](/developer-guides/image-generation/image-editing)或[图像编辑-万相2.1](/developer-guides/image-generation/wan-image-editing)获取替代方案。
</Warning>

## 基本介绍

万相-图像局部重绘是基于自研的Composer组合生成框架的AI绘画创作大模型后置处理链路，能够根据用户输入的原始图片和局部涂抹图、prompt提示词文字内容，生成符合语义描述的多样化风格的局部重绘图像。通过知识重组与可变维度扩散模型，加速收敛并提升最终生成图片的效果，布局自然、细节丰富、画面细腻、结果逼真。

客户提供原始图片任意涂抹图中区域，结合输入修改初始提示文字，在涂抹区域内生成与新提示文字匹配的内容，涂抹区域外没有变化。

## 使用场景

- **艺术创作与设计**：艺术家和设计师可以利用图像局部重绘快速迭代作品，比如改变画作的背景、调整服装颜色或添加新的元素，而无需从头开始创作，极大地提升了创意工作的效率。
- **教育与培训**：在艺术教育中，学生可以利用图像局部重绘学习不同的绘画技巧和风格，通过修改大师作品的局部来理解色彩、构图和光影的应用。
- **广告与营销**：广告行业可以快速调整产品展示图，如改变产品颜色、背景环境、局部场景元素以适应不同市场和季节需求，提高广告创意的灵活性和针对性。
- **影视与游戏制作**：在后期制作中，图像局部重绘技术能帮助快速修改场景细节，如调整角色服饰、道具样式，或是优化视觉特效，减少图像海报等物料制作时间和成本。
- **个性化礼物定制**：图像局部重绘使得个性化定制变得简单快捷，比如在纪念品、T恤或杯子上添加个人照片时，可以轻松调整背景、融合风格或加入定制文字，确保最终产品既符合个人喜好又具有专业品质。

## 特色优势

- **知识重组与可变维扩散模型**：基于自研的Composer组合生成框架的AI局部绘画创作大模型，通过知识重组与可变维度扩散模型，生成符合语义描述的多样化风格的图像。
- **效果业界领先**：生成图像语义一致性更精准，AI绘画创作布局自然、细节丰富、画面细腻、结果逼真。
- **高语意精准可控**：用户能够精确指定修改区域，确保生成的内容仅限于所选范围，保持图像其余部分不变，实现高度的可控性和精确度。
- **易于集成使用**：用户无需具备高级图像编辑技能，只需简单提示词描述修改意图，即可通过万相系列生成大模型实现复杂图像处理，降低了技术门槛。

### 模型概览

<table>
  <thead>
    <tr>
      <th>模型名称</th>
      <th>计费单价</th>
      <th>任务下发接口QPS限制</th>
      <th>同时处理中任务数量</th>
      <th>免费额度[（查看）](/resources/free-quota)</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>wanx-x-painting</td>
      <td>目前仅供免费体验。免费额度用完后不可调用，推荐参考[图像编辑-千问](/developer-guides/image-generation/image-editing)或[图像编辑-万相2.1](/developer-guides/image-generation/wan-image-editing)获取替代方案。</td>
      <td style={{textAlign: "center"}}>2</td>
      <td style={{textAlign: "center"}}>1</td>
      <td style={{textAlign: "center"}}>500张</td>
    </tr>
  </tbody>
</table>

## 快速开始

输入图像关键参数：

- 图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。
- 图像大小：不超过10MB。
- 图像分辨率：大于256×256像素，小于4096×4096像素。
- URL地址中不能包含中文字符（请在此[获取临时公网URL](/api-reference/platform-api/file/upload-file)）。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "28%"}}>**输入图像（重绘前）**</th>
      <th style={{textAlign: "center", width: "28%"}}>**mask涂抹图**</th>
      <th style={{textAlign: "center", width: "16%"}}>**提示词示例**</th>
      <th style={{textAlign: "center", width: "28%"}}>**输出图像（重绘后）**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "top"}}>
        <img alt="输入图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8649386271/p848790.png" style={{width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "top"}}>
        <img alt="mask涂抹图" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8649386271/p848791.png" style={{width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>一只狗戴着红色眼镜</td>

      <td style={{textAlign: "center", verticalAlign: "top"}}>
        <img alt="输出图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8649386271/p848792.png" style={{width: "100%"}} />
      </td>
    </tr>
  </tbody>
</table>

由于模型计算耗时较长，示例代码均展示异步处理的调用方式，以避免请求超时。

您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。如果通过SDK调用，还需要[安装DashScope SDK](/api-reference/preparation/install-sdk)。

<Tabs>
  <Tab title="curl">
    **1、创建任务**

    由于模型计算耗时较长，HTTP使用异步调用。创建好的任务会进入任务池，等待调度执行。因此，这个接口会返回一个任务ID（task\_id），后续根据任务ID进行状态和结果的查询。

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wanx-x-painting",
      "input": {
        "prompt": "a dog wearing red glasses",
        "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
        "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
      },
      "parameters": {
        "size": "1024*1024",
        "n": 1
      }
    }'
    ```

    **2、根据任务ID查询结果**

    ```bash
    curl -X GET \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    https://dashscope.aliyuncs.com/api/v1/tasks/{your_task_id}
    ```
  </Tab>

  <Tab title="Python">
    <CodeGroup>
      ```python 同步调用
      from http import HTTPStatus
      from urllib.parse import urlparse, unquote
      from pathlib import PurePosixPath
      import requests
      from dashscope import ImageSynthesis

      prompt = "a dog wearing red glasses"
      model = "wanx-x-painting"
      task = "image2image"
      extra_input = {
        "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
        "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
      }

      print('----sync call, please wait a moment----')
      rsp = ImageSynthesis.call(model=model,
                                prompt=prompt,
                                n=1,
                                size='1024*1024',
                                task=task,
                                extra_input=extra_input)
      if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        # save file to current directory
        for result in rsp.output.results:
          file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
          with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)
      else:
        print('sync_call Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
      ```

      ```python 异步调用
      from http import HTTPStatus
      from urllib.parse import urlparse, unquote
      from pathlib import PurePosixPath
      import requests
      from dashscope import ImageSynthesis

      prompt = "a dog wearing red glasses"
      model = "wanx-x-painting"
      task = "image2image"
      extra_input = {
        "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
        "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
      }

      def async_call():
        print('----create task----')
        task_info = create_async_task()
        if task_info.status_code == HTTPStatus.OK:
          print('----wait task done then save image----')
          wait_async_task(task_info)
        else:
          print('Task creation failed, cannot proceed to wait')

      # 创建异步任务
      def create_async_task():
        rsp = ImageSynthesis.async_call(model=model,
                                        prompt=prompt,
                                        n=1,
                                        size='1024*1024',
                                        task=task,
                                        extra_input=extra_input)
        print(rsp)
        if rsp.status_code == HTTPStatus.OK:
          print(rsp.output)
        else:
          print('create_async_task Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))
        return rsp

      # 等待异步任务结束
      def wait_async_task(task):
        rsp = ImageSynthesis.wait(task)
        print(rsp)
        if rsp.status_code == HTTPStatus.OK:
          print(rsp.output.task_status)
          # save file to current directory
          for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
              f.write(requests.get(result.url).content)
        else:
          print('Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))

      if __name__ == '__main__':
        async_call()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Java">
    <CodeGroup>
      ```java 同步调用
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.JsonUtils;

      import java.util.HashMap;

      public class Main {

        public void syncCall() {
          String task = "image2image";
          ImageSynthesis imageSynthesis = new ImageSynthesis(task);
          ImageSynthesisParam param = genImageSynthesis();
          ImageSynthesisResult result = null;
          try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
          } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
          }
          System.out.println(JsonUtils.toJson(result));
        }

        private ImageSynthesisParam genImageSynthesis(){
          HashMap<String,Object> extraInputMap = new HashMap<>();
          extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
          extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");
          String prompt = "a dog wearing red glasses";
          String model = "wanx-x-painting";
          return ImageSynthesisParam.builder()
                  .model(model)
                  .prompt(prompt)
                  .n(1)
                  .size("1024*1024")
                  .extraInputs(extraInputMap)
                  .build();
        }

        public static void main(String[] args){
          Main text2Image = new Main();
          text2Image.syncCall();
        }

      }
      ```

      ```java 异步调用
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
      import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.JsonUtils;

      import java.util.HashMap;

      public class Main {

        public void asyncCall() {
          System.out.println("---create task----");
          String taskId = this.createAsyncTask();
          System.out.println("---wait task done then return image url----");
          this.waitAsyncTask(taskId);
        }

        /**
         * 创建异步任务
         * @return taskId
         */
        public String createAsyncTask() {
          String task = "image2image";
          ImageSynthesis imageSynthesis = new ImageSynthesis(task);
          ImageSynthesisParam param = genImageSynthesis();
          ImageSynthesisResult result = null;
          try {
            result = imageSynthesis.asyncCall(param);
          } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
          }
          String taskId = result.getOutput().getTaskId();
          System.out.println("taskId=" + taskId);
          return taskId;
        }

        private ImageSynthesisParam genImageSynthesis(){
          String prompt = "a dog wearing red glasses";
          String model = "wanx-x-painting";
          HashMap<String,Object> extraInputMap = new HashMap<>();
          extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
          extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");

          return ImageSynthesisParam.builder()
                  .model(model)
                  .prompt(prompt)
                  .n(1)
                  .size("1024*1024")
                  .extraInputs(extraInputMap)
                  .build();
        }

        /**
         * 等待异步任务结束
         * @param taskId 任务id
         * */
        public void waitAsyncTask(String taskId) {
          ImageSynthesis imageSynthesis = new ImageSynthesis();
          ImageSynthesisResult result = null;
          try {
            // If you have set the DASHSCOPE_API_KEY in the system environment variable, the apiKey can be null.
            result = imageSynthesis.wait(taskId, null);
          } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
          }

          System.out.println(JsonUtils.toJson(result.getOutput()));
          System.out.println(JsonUtils.toJson(result.getUsage()));
        }

        public static void main(String[] args){
          Main text2Image = new Main();
          text2Image.asyncCall();
        }

      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## API参考

API的输入输出参数，请参见[万相-图像局部重绘](/api-reference/image-generation/wanx-x-painting/create-task)。
