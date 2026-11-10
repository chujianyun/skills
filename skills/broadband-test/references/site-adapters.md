# 站点操作与字段适配

以下为已核实的网页界面，站点可能更新。使用前先读当前页面，选择器失效时按标签重新定位；不要猜测私有 API，也不要直接调用垃圾数据下载/上传接口代替完整测速。浏览器工具只允许只读 DOM 求值时，仅用下列 DOM 读取方式，不读应用内部变量或通过求值启动测试。

## 中科大：test.ustc.edu.cn

- 页面标题：中国科学技术大学测速网站。
- 页面会在正常 PoW 计算后**自动开始**。只等待页面自身完成计算，不自行重写验证逻辑。先检查 `#startStopBtn` 是否有 `running` 类；在运行中点击它会中止测速。
- 手动开始/停止控件为 `#startStopBtn`，文字可能来自 CSS 伪元素，不能只找 `textContent === '开始测速'`。
- 观察到本轮进入 `running` 后，再观察 `running` 消失及四项最终字段更新。页面下方含历史记录/结果对象，不应读取其他人的历史结果作为本轮数据。
- 该站可能根据来源网络调整时长，使用页面默认设置。站点说明会保存测试时间、IP 和测速结果，短时间多测/大量下载可能临时封禁；不连续重试或调长测速时长。
- `#pingText`：网络延迟 ms；`#jitText`：延迟抖动 ms；`#dlText`：下载 Mbps；`#ulText`：上传 Mbps。页面可能对显示值舍入，保留其显示精度，不伪造更多位数。

可传入浏览器只读求值工具的函数：

```javascript
() => {
  const text = id => document.getElementById(id)?.textContent?.trim() || null;
  const button = document.getElementById('startStopBtn');
  return {
    running: button ? button.classList.contains('running') : null,
    latency_ms: text('pingText'),
    jitter_ms: text('jitText'),
    download_mbps: text('dlText'),
    upload_mbps: text('ulText')
  };
}
```

此函数提供一次快照；`running: false` 不等于本轮已完成。加载前/中止后也可能返回 false，仍须结合主流程的开始、结束和结果更新证据。

## 南京大学：test.nju.edu.cn

- 页面标题：南大测速 NJU Test；页头：南京大学测速站。
- 可能出现正常浏览器验证/自动跳转。无头访问或普通抓取可能返回 403，而已连接的正常本机浏览器可以访问；这不是测速结果。按主流程报告失败或使用已授权的正常浏览器，不伪装客户端身份或绕过验证。
- 先观察是否在测；空闲时点击 `#startStopBtn` 一次。界面从“开始测速”变为“中止测速”，完成后回到“开始测速”，出现本轮分享结果区域。加载时的四个 `0.00` 是占位值。
- 四项字段与中科大相同：`#pingText`、`#jitText`、`#dlText`、`#ulText`；下载/上传标签为 `Mbit/s`，与 Mbps 相同。可复用上节的只读函数。
- 完成后 `#resultsImg` 的 `alt` 可能提供比仪表盘更高精度的本轮结果，格式为 `Download: … Mbps, Upload: … Mbps, Ping: … ms, Jitter: … ms`。只有确认本轮结束、分享区域更新后才使用；同站优先采用这一个来源的四项数据，避免混合旧值和新值。不存在时退回四个文本字段。

```javascript
() => ({
  result_alt: document.getElementById('resultsImg')?.getAttribute('alt') || null,
  share_present: Boolean(document.getElementById('shareArea'))
})
```

`share_present` 只说明节点存在，不说明它可见或属于本轮；先核对页面状态。不要输出 `#resultsURL` 的值、测试 ID 或 IP。

校内用户到该节点的结果可能是校内路径带宽，不能当成访问所有校外网站的速度。

## 测速网：www.speedtest.cn

- 使用“测网速”首页的免费基础测速；它与 Ookla 的 `speedtest.net` 是不同服务，不替换网址。
- 等待“正在查找测速节点”完成，记录自动选定的节点名称。主页圆形“测速”控件用于开始；根据当前快照定位，例如精确匹配文本“测速”，不要误点“提网速”“企业专线测速”、广告、安装或会员入口。
- 点击一次后观察启动/运行过程；本轮结束后主测速控件恢复，页面出现已更新的下载、上传结果曲线和时延/抖动结果。大仪表盘回到 `0.0` 不表示下载或上传为零；应读最终结果卡片。
- 页面可能同时存在隐藏的验证码容器、隐藏的弹窗或历史值。用可见性检查或截图确认真实阻塞，不仅因 DOM 中有“拖动拼图”文字就要求用户验证。若确实弹出人工验证码，按主流程交给用户，不解题、不绕过。
- 结果后可能弹出客户端安装推荐：只关闭可见弹窗，不安装。已核实推荐弹窗的关闭控件为 `.download img.close`；仍需在当前 DOM 中确认后使用。广告和诊断结论不作为实测数据或硬件故障证据。

已核实的最终结果区域：

| 指标 | DOM 位置 | 读取说明 |
| --- | --- | --- |
| 下载 | `.transfer-item-down dd` | `textContent` 合并整数与小数子节点；单位看同区 `dt` |
| 上传 | `.transfer-item-up dd` | 同上；不要读取正在测速的大仪表盘 |
| 时延 | `.record-info-delay p > span` | 每项含图标 `img[alt]` 与 `.record-info-delay-value` |
| 抖动 | `.record-info-jitter p` | 单位看同区标签，不用游戏/视频延迟代替 |

时延区图标 `alt="delay"` 是基本时延，`alt="down"` 是下载负载时延，`alt="up"` 是上传负载时延。先结合当前标签/提示核对，主表用基本时延，后两项可附在表后；无法确认口径时保留原标签并说明，不把三个数平均。

```javascript
() => {
  const text = selector => document.querySelector(selector)?.textContent?.trim() || null;
  return {
    download: text('.transfer-item-down dd'),
    download_label: text('.transfer-item-down dt'),
    upload: text('.transfer-item-up dd'),
    upload_label: text('.transfer-item-up dt'),
    delays: [...document.querySelectorAll('.record-info-delay p > span')].map(item => ({
      kind: item.querySelector('img')?.getAttribute('alt') || null,
      value: item.querySelector('.record-info-delay-value')?.textContent?.trim() || null
    })),
    delay_label: text('.record-info-delay > span'),
    jitter: text('.record-info-jitter p'),
    jitter_label: text('.record-info-jitter > span')
  };
}
```

只有本轮完成且结果卡片可见时读取；如有多个匹配，先限定到可见的本轮结果容器，不默认取隐藏历史数据。用户可切换显示单位，因此必须读取 `dt` 标签后再换算，不能写死网页永远显示 Mbps。

节点名称从本轮测速区域“更换测速点”旁的可见文字取得，不从网页排名、广告或 IP 属地推断。

## 场景验收

维护本技能时检查以下行为；不用为了验证技能重复发起真实测速流量：

- “测一下宽带”：本机浏览器，默认三站顺序单轮，输出四项指标、节点、时间和状态。
- “只测南大”：只运行该站；“解释抖动”：只解释，不启动测速。
- 页面一打开全为 `0.00`：未观察到本轮开始和结束，不输出四个零作为成功。
- 旧结果仍在，点击后出现“中止测速”：旧值不算最终结果；用户中止/超时则标未完成。
- 一站 403，另一站缺抖动：前者失败指标写“—”，后者部分结果且抖动写“未提供”，其余站照常测。
- 下载单位 `MB/s`：乘 8 转 Mbps；`Mbit/s` 原值即可；MiB/s 使用二进制换算。
- 测速网显示三个延迟：区分基本与上下行负载延迟；隐藏验证码容器不视为可见人工验证。
- 人工验证确实可见：交给用户；缺浏览器或仅有云端工具：不冒充用户本机测速。
- “测得慢就给我自动提速”：仅交付实测结果，购买/配置修改先核实具体授权。
