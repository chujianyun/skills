> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 涂鸦作画

> 根据手绘图加上任意文字描述，使用万相-涂鸦作画模型，即可轻松完成涂鸦作画。

## 基本介绍

万相-涂鸦作画通过手绘任意内容加文字描述，即可生成精美的涂鸦绘画作品，作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。涂鸦作画支持扁平插画、油画、二次元、3D卡通和水彩5种风格，可用于创意娱乐、辅助设计、儿童教学等场景。

### 使用场景

- **创意贺卡设计**：用户可以利用涂鸦作画功能，结合节日主题和个人创意，手稿创作一幅圣诞老人与驯鹿在雪地中的温馨场景，增加贺卡的个性化与情感表达，使收卡人感受到更加真挚与特别的祝福。
- **儿童绘本制作**：教育工作者或家长可以根据孩子的兴趣和故事内容，涂鸦作画制作富有教育意义和趣味性的插图绘本，提升儿童阅读兴趣，促进想象力和创造力的发展。
- **个性化商品设计**：电商平台或设计师可以利用该功能快速生成具有独特艺术风格的产品设计，如T恤、手机壳、马克杯上的涂鸦创作图案，满足消费者对个性化和定制化商品的需求。
- **社交媒体内容创作**：博主和内容创作者可利用涂鸦作画创作与主题内容相符的原创涂鸦插图，提高内容的视觉吸引力，帮助建立独特的个人品牌形象，吸引并保持粉丝的关注。
- **室内装饰设计**：室内设计师可以为客户定制个性化的墙面艺术画或装饰图案，如根据房间风格创作相应风格的涂鸦画作，实现空间的个性化定制，提升居住或办公环境的艺术氛围。

### 特色优势

- **知识重组&可变维扩散模型**：基于自研的Composer组合生成框架的AI局部绘画创作大模型，通过知识重组与可变维度扩散模型，生成符合语义描述的多样化风格的图像。
- **效果业界领先**：生成图像语义一致性更精准，AI绘画创作布局自然、细节丰富、画面细腻、结果逼真。作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。
- **涂鸦风格多样化**：支持扁平插画、油画、二次元、3D卡通和水彩五种风格。
- **稳定、易用平台服务**：提供在高并发、大流量下的稳定图片生成响应和99.99%的可靠性保障，可直接调用的简单训练和推理API接口，服务简单易用，易于集成，兼容性强。

### 模型概览

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 模型名                       | 模型简介                                                           | 免费额度[（查看）](/resources/free-quota) | 计费单价    | 任务下发接口QPS限制 | 同时处理中任务数量 |
| ------------------------- | -------------------------------------------------------------- | --------------------------------- | ------- | ----------- | --------- |
| wanx-sketch-to-image-lite | 万相-涂鸦作画通过手绘任意内容加文字描述，即可生成精美的涂鸦绘画作品。作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。 | 500张                              | 0.06元/张 | 2           | 1         |

## 快速开始

输入图像关键参数：

- **手绘草图**：输入草图的比例需要与输出分辨率的比例一致，否则会导致图片拉伸变形。建议使用白色背景+黑色线条。
- **图像格式**：格式为JPG、PNG、TIFF、WEBP等常见位图格式。
- **图像大小**：不超过10MB。
- **图像分辨率**：分辨率长边不大于2048像素。

<img alt="涂鸦作画示例" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5649386271/p848471.png" width="900" />

由于模型计算耗时较长，示例代码均展示异步处理的调用方式，以避免请求超时。

<Note>
  您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。如果通过SDK调用，还需要[安装DashScope SDK](/api-reference/preparation/install-sdk)。
</Note>

<CodeGroup>
  ```bash curl
  # 1、创建涂鸦作画任务
  # 接口返回任务ID，可根据任务ID查询图像生成的结果。
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
  --header 'X-DashScope-Async: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wanx-sketch-to-image-lite",
    "input": {
      "sketch_image_url": "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg",
      "prompt": "一棵参天大树"
    },
    "parameters": {
      "size": "768*768",
      "n": 2,
      "sketch_weight": 3,
      "style": "<watercolor>"
    }
  }'

  # 2、根据任务ID查询结果
  curl -X GET \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
  ```

  ```python Python
  from http import HTTPStatus
  from urllib.parse import urlparse, unquote
  from pathlib import PurePosixPath
  import requests
  from dashscope import ImageSynthesis

  prompt = "一棵参天大树"
  sketch_image_url = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg"
  model = "wanx-sketch-to-image-lite"
  task = "image2image"

  # 异步调用
  def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task done then save image----')
    wait_async_task(task_info)

  # 创建异步任务
  def create_async_task():
    rsp = ImageSynthesis.async_call(model=model,
      prompt=prompt,
      n=1,
      style='<watercolor>',
      size='768*768',
      sketch_image_url=sketch_image_url,
      task=task)
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

  ```java Java
  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;

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
      String prompt = "一棵参天大树";
      String sketchImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg";
      String model = "wanx-sketch-to-image-lite";
      ImageSynthesisParam param = ImageSynthesisParam.builder()
        .model(model)
        .prompt(prompt)
        .n(1)
        .size("768*768")
        .sketchImageUrl(sketchImageUrl)
        .style("<watercolor>")
        .build();

      String task = "image2image";
      ImageSynthesis imageSynthesis = new ImageSynthesis(task);
      ImageSynthesisResult result = null;
      try {
        result = imageSynthesis.asyncCall(param);
      } catch (Exception e) {
        throw new RuntimeException(e.getMessage());
      }
      String taskId = result.getOutput().getTaskId();
      System.out.println("taskId=" + taskId);
      return taskId;
    }

    /**
     * 等待异步任务结束
     * @param taskId 任务id
     */
    public void waitAsyncTask(String taskId) {
      ImageSynthesis imageSynthesis = new ImageSynthesis();
      ImageSynthesisResult result = null;
      try {
        // If you have set the DASHSCOPE_API_KEY in the system environment variable, the apiKey can be null.
        result = imageSynthesis.wait(taskId, null);
      } catch (ApiException | NoApiKeyException e) {
        throw new RuntimeException(e.getMessage());
      }

      System.out.println(JsonUtils.toJson(result.getOutput()));
      System.out.println(JsonUtils.toJson(result.getUsage()));
    }

    public static void main(String[] args) {
      Main text2Image = new Main();
      text2Image.asyncCall();
    }
  }
  ```
</CodeGroup>

## API参考

API的输入输出参数，请参见[万相-涂鸦作画API参考](/api-reference/image-generation/wanx-sketch-to-image/create-task)。
