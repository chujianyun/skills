> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# wanx-v1 — 创建文生图任务

> wanx-v1 异步图像生成

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<Note>
  **wanx-v1 已停止迭代更新**，推荐升级至 [Wan 文生图 V2](/api-reference/image-generation/wan-text-to-image-v2/create-task) 以获取更好的效果。
</Note>

## OpenAPI

````yaml post /services/aigc/text2image/image-synthesis
openapi: 3.1.0
info:
  title: Wan 文生图 V1 API
  description: 使用 wanx-v1 模型根据文本描述生成图像。本 API 采用异步任务模式：先通过 POST 请求提交任务，再通过 GET 请求轮询结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 阿里云 DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/text2image/image-synthesis:
    post:
      operationId: createWanxV1TextToImageTask
      summary: 创建文生图任务
      description: 提交 wanx-v1 文生图异步任务。提交后通过 GET /tasks/{task_id} 轮询获取结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable` 以创建异步任务。如未设置，将返回错误："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
        - name: X-DashScope-WorkSpace
          in: header
          required: false
          description: 指定工作空间，格式为 `ws_{workspaceId}`。
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WanxV1TextToImageRequest"
      responses:
        "200":
          description: 任务创建成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/WanxV1CreateTaskResponse"
              examples:
                success:
                  summary: 任务创建成功
                  value:
                    output:
                      task_status: PENDING
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                    request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        4XX:
          description: 请求失败。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                error:
                  summary: 请求失败示例
                  value:
                    code: InvalidApiKey
                    message: No API-key provided.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL - 文字作画（正向提示词）
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wanx-v1",
                "input": {
                    "prompt": "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"
                },
                "parameters": {
                    "style": "<auto>",
                    "size": "1024*1024",
                    "n": 1
                }
            }'
        - lang: curl
          label: cURL - 文字作画（正向+反向提示词）
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wanx-v1",
                "input": {
                    "prompt": "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。",
                    "negative_prompt": "不要使用红色元素"
                },
                "parameters": {
                    "style": "<auto>",
                    "size": "1024*1024",
                    "n": 1
                }
            }'
        - lang: curl
          label: cURL - 参考图生成（基于参考图内容）
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wanx-v1",
                "input": {
                    "prompt": "一个英气的黑发女人，飞舞着金色的蝴蝶，背景中有若隐若现的水墨竹林，高细节，高质量。",
                    "ref_img": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png"
                },
                "parameters": {
                    "style": "<auto>",
                    "size": "1024*1024",
                    "n": 1,
                    "ref_strength": 1.0,
                    "ref_mode": "repaint"
                }
            }'
        - lang: curl
          label: cURL - 参考图生成（基于参考图风格）
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wanx-v1",
                "input": {
                    "prompt": "有一只黑色的小猫",
                    "ref_img": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/gpqnqy/house.png"
                },
                "parameters": {
                    "style": "<auto>",
                    "size": "1024*1024",
                    "n": 1,
                    "ref_strength": 0.7,
                    "ref_mode": "refonly"
                }
            }'
        - lang: python
          label: Python - 同步调用 - 文字作画
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

            print('----sync call, please wait a moment----')
            rsp = ImageSynthesis.call(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              model=ImageSynthesis.Models.wanx_v1,
              prompt=prompt,
              n=1,
              style='<watercolor>',
              size='1024*1024'
            )
            print('response: %s' % rsp)
            if rsp.status_code == HTTPStatus.OK:
              # 在当前目录下保存图片
              for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                  f.write(requests.get(result.url).content)
            else:
              print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                    (rsp.status_code, rsp.code, rsp.message))
        - lang: python
          label: Python - 同步调用 - 参考图生成
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

            # 上传参考图方式：url链接和本地路径二选一
            # 若两者存在，ref_img参数优先级更高
            # 使用公网url链接
            ref_img = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png"
            # 使用本地文件路径
            sketch_image_url = './girl.png'

            print('----sync call, please wait a moment----')
            rsp = ImageSynthesis.call(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              model=ImageSynthesis.Models.wanx_v1,
              prompt=prompt,
              n=1,
              style='<auto>',
              size='1024*1024',
              ref_mode='repaint',
              ref_strength=1.0,
              # sketch_image_url=sketch_image_url,
              ref_img=ref_img
            )
            print(rsp)
            if rsp.status_code == HTTPStatus.OK:
              print(rsp.output)
              # 保留图片到当前目录
              for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                  f.write(requests.get(result.url).content)
            else:
              print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                    (rsp.status_code, rsp.code, rsp.message))
        - lang: python
          label: Python - 异步调用 - 文字作画
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

            def async_call():
              print('----create task----')
              task_info = create_async_task()
              print('----wait task done then save image----')
              wait_async_task(task_info)

            # 创建异步任务
            def create_async_task():
              rsp = ImageSynthesis.async_call(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model=ImageSynthesis.Models.wanx_v1,
                prompt=prompt,
                n=1,
                style='<watercolor>',
                size='1024*1024'
              )
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
              return rsp

            # 等待异步任务结束
            def wait_async_task(task):
              rsp = ImageSynthesis.wait(task, api_key=os.getenv("DASHSCOPE_API_KEY"))
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
                for result in rsp.output.results:
                  file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                  with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            # 获取异步任务信息
            def fetch_task_status(task):
              status = ImageSynthesis.fetch(task, api_key=os.getenv("DASHSCOPE_API_KEY"))
              print(status)
              if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (status.status_code, status.code, status.message))

            # 取消异步任务，只有处于PENDING状态的任务才可以取消
            def cancel_task(task):
              rsp = ImageSynthesis.cancel(task, api_key=os.getenv("DASHSCOPE_API_KEY"))
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.task_status)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              async_call()
        - lang: python
          label: Python - 异步调用 - 参考图生成
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

            # 上传参考图方式：url链接和本地路径二选一
            # 若两者存在，ref_img参数优先级更高
            # 使用公网url链接
            ref_img = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png"
            # 使用本地文件路径
            sketch_image_url = './girl.png'

            def async_call():
              print('----create task----')
              task_info = create_async_task()
              print('----wait task done then save image----')
              wait_async_task(task_info)

            # 创建异步任务
            def create_async_task():
              rsp = ImageSynthesis.async_call(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model=ImageSynthesis.Models.wanx_v1,
                prompt=prompt,
                n=1,
                style='<auto>',
                size='1024*1024',
                ref_mode='repaint',
                ref_strength=1.0,
                # sketch_image_url=sketch_image_url,
                ref_img=ref_img
              )
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
              else:
                print('create_async_task Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
              return rsp

            # 等待异步任务结束
            def wait_async_task(task):
              rsp = ImageSynthesis.wait(task, api_key=os.getenv("DASHSCOPE_API_KEY"))
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                for result in rsp.output.results:
                  file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                  with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              async_call()
        - lang: java
          label: Java - 同步调用 - 文字作画
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;

            public class Main {
                public static void basicCall() throws ApiException, NoApiKeyException {
                    String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
                    ImageSynthesisParam param =
                            ImageSynthesisParam.builder()
                                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                    .model(ImageSynthesis.Models.WANX_V1)
                                    .prompt(prompt)
                                    .style("<watercolor>")
                                    .n(1)
                                    .size("1024*1024")
                                    .build();

                    ImageSynthesis imageSynthesis = new ImageSynthesis();
                    ImageSynthesisResult result = null;
                    try {
                        System.out.println("---sync call, please wait a moment----");
                        result = imageSynthesis.call(param);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                }

                public static void listTask() throws ApiException, NoApiKeyException {
                    ImageSynthesis is = new ImageSynthesis();
                    AsyncTaskListParam param = AsyncTaskListParam.builder().build();
                    ImageSynthesisListResult result = is.list(param);
                    System.out.println(result);
                }

                public void fetchTask() throws ApiException, NoApiKeyException {
                    String taskId = "your task id";
                    ImageSynthesis is = new ImageSynthesis();
                    // If set DASHSCOPE_API_KEY environment variable, apiKey can null.
                    ImageSynthesisResult result = is.fetch(taskId, null);
                    System.out.println(result.getOutput());
                    System.out.println(result.getUsage());
                }

                public static void main(String[] args){
                    try{
                        basicCall();
                        //listTask();
                    }catch(ApiException|NoApiKeyException e){
                        System.out.println(e.getMessage());
                    }
                }
            }
        - lang: java
          label: Java - 同步调用 - 相似图生成
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.HashMap;

            public class Main {

                public void syncCall() {
                    String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
                    //使用公网url链接
                    String refImage = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png";
                    HashMap<String,Object> parameters = new HashMap<>();
                    parameters.put("ref_strength", 0.5);
                    parameters.put("ref_mode", "repaint");

                    ImageSynthesisParam param =
                            ImageSynthesisParam.builder()
                                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                    .model(ImageSynthesis.Models.WANX_V1)
                                    .prompt(prompt)
                                    .style("<auto>")
                                    .n(1)
                                    .size("1024*1024")
                                    .refImage(refImage)
                                    .parameters(parameters)
                                    .build();

                    ImageSynthesis imageSynthesis = new ImageSynthesis();
                    ImageSynthesisResult result = null;
                    try {
                        System.out.println("---sync call, please wait a moment----");
                        result = imageSynthesis.call(param);
                    } catch (ApiException|NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                }

                public static void main(String[] args){
                    Main text2Image = new Main();
                    text2Image.syncCall();
                }

            }
        - lang: java
          label: Java - 异步调用 - 文字作画
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

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
                    String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
                    ImageSynthesisParam param =
                            ImageSynthesisParam.builder()
                                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                    .model(ImageSynthesis.Models.WANX_V1)
                                    .prompt(prompt)
                                    .style("<watercolor>")
                                    .n(1)
                                    .size("1024*1024")
                                    .build();

                    ImageSynthesis imageSynthesis = new ImageSynthesis();
                    ImageSynthesisResult result = null;
                    try {
                        result = imageSynthesis.asyncCall(param);
                    } catch (Exception e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                    String taskId = result.getOutput().getTaskId();
                    System.out.println("taskId=" + taskId);
                    return taskId;
                }

                /**
                 * 等待异步任务结束
                 * @param taskId 任务id
                 * */
                public void waitAsyncTask(String taskId) {
                    ImageSynthesis imageSynthesis = new ImageSynthesis();
                    ImageSynthesisResult result = null;
                    try {
                        //环境变量配置后，可在这里将apiKey设置为null
                        result = imageSynthesis.wait(taskId, null);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                    System.out.println(JsonUtils.toJson(result.getOutput()));
                }

                public static void main(String[] args){
                    Main main = new Main();
                    main.asyncCall();
                }
            }
        - lang: java
          label: Java - 异步调用 - 相似图生成
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

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
                    String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
                    String refImage = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png";
                    ImageSynthesisParam param =
                            ImageSynthesisParam.builder()
                                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                    .model(ImageSynthesis.Models.WANX_V1)
                                    .prompt(prompt)
                                    .style("<auto>")
                                    .n(1)
                                    .size("1024*1024")
                                    .refImage(refImage)
                                    .build();

                    ImageSynthesis imageSynthesis = new ImageSynthesis();
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
                    } catch (ApiException|NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }

                    System.out.println(JsonUtils.toJson(result.getOutput()));
                }

                public static void main(String[] args){
                    Main text2Image = new Main();
                    text2Image.asyncCall();
                }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanxV1TextToImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          example: wanx-v1
        input:
          type: object
          required:
            - prompt
          description: 输入内容。
          properties:
            prompt:
              type: string
              description: 正向文本描述，即期望图像中出现的内容。最大 800 个字符。
              maxLength: 800
            negative_prompt:
              type: string
              description: 反向文本描述，即不希望图像中出现的内容。最大 500 个字符。
              maxLength: 500
            ref_img:
              type: string
              description: 参考图像 URL。支持 JPG、PNG、BMP、TIFF、WEBP 格式，大小不超过 10 MB，分辨率在 256×256 至 4096×4096 之间，URL 不能包含中文字符。
        parameters:
          type: object
          description: 生成参数（可选）。
          properties:
            style:
              type: string
              description: 图像风格。
              enum:
                - <auto>
                - <photography>
                - <portrait>
                - <3d cartoon>
                - <anime>
                - <oil painting>
                - <watercolor>
                - <sketch>
                - <chinese painting>
                - <flat illustration>
              default: <auto>
            size:
              type: string
              description: 图像分辨率，格式为 `宽*高`。
              enum:
                - 1024*1024
                - 720*1280
                - 768*1152
                - 1280*720
              default: 1024*1024
            n:
              type: integer
              description: 生成图像数量。
              minimum: 1
              maximum: 4
              default: 4
            seed:
              type: integer
              description: 随机种子，用于结果复现。范围 [0, 2147483647]。
              minimum: 0
              maximum: 2147483647
            ref_strength:
              type: number
              description: 参考图强度，控制生成图像与参考图的相似程度。范围 [0.0, 1.0]，值越大越相似。
              minimum: 0
              maximum: 1
            ref_mode:
              type: string
              description: 参考图模式。`repaint` 基于参考图内容生成，`refonly` 基于参考图风格生成。
              enum:
                - repaint
                - refonly
              default: repaint
    WanxV1CreateTaskResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于查询任务状态和结果。有效期 24 小时。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
        request_id:
          type: string
          description: 请求唯一标识。
    WanxV1TaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 任务状态：`PENDING`（等待）、`RUNNING`（运行中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（未知）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            results:
              type: array
              description: 生成的图像列表。任务成功后返回。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 图像 URL，有效期 24 小时，请及时下载。
                  code:
                    type: string
                    description: 当该图像生成失败时，返回错误码。
                  message:
                    type: string
                    description: 当该图像生成失败时，返回错误信息。
            task_metrics:
              type: object
              description: 任务统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 图像总数。
                SUCCEEDED:
                  type: integer
                  description: 成功生成的图像数量。
                FAILED:
                  type: integer
                  description: 生成失败的图像数量。
            code:
              type: string
              description: 任务失败时的错误码。
            message:
              type: string
              description: 任务失败时的错误信息。
        usage:
          type: object
          description: 资源用量统计。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误信息。
        request_id:
          type: string
          description: 请求唯一标识。
````
