---
title: "AI出海最大的坑，不是模型。"
source: "https://mp.weixin.qq.com/s/gPHcTBCev7QFSjU4hfANiQ"
author:
  - "[[苍何]]"
published:
created: 2026-07-24
description:
tags:
  - "clippings"
---
苍何 苍何 *2026年7月23日 12:08*

这是苍何的第 567 篇原创！

大家好，我是苍何。

最近半年，我一直在尝试做出海业务和产品。比如 WeSight 和 GPT-Image 2-Gallery 就有不少的海外用户。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaBEeGAibPXQ1MvzNFaB6u4ENBaicyVzkzyXXc16ib4eelszS5Q6MhPscn8Y8AvdJkVV0rAricFOMINLaRtjibhLZSaj9gAZiaGMpmfs8/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

说实话，没真正跑起来之前，我以为最难的是产品本身。

跑起来之后才发现，技术基建才是真正的拦路虎。

我身边也有越来越多朋友在做出海，方向五花八门，有做 AI 社交的，有做跨境电商工具的，还有做短视频平台的。

但聊到最后，大家吐槽的问题出奇地一致。

## 出海业务，绕不开的几个坑

第一个坑，用户分散。

你的用户可能分布在东南亚、欧洲、北美，不同地区的网络质量天差地别。

同一个接口，新加坡用户 50ms 响应，巴西用户可能要 300ms。

用户才不管你服务器在哪，他只知道「这个 App 好卡，删了」。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaAHEZZf7dnD07nsYTBicIg9ECfJFWjFsVvkkqJfMYUgwk2D0E23Z0td0P1386wBBfT8hbEHqhYNriatZg7JkArrHymWhcSnh2t00/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

第二个坑，隐性成本。

很多人觉得云服务器不贵，一个月几百块钱。

但真正跑起来你会发现，服务器费用可能只占总成本的 30%。

流量费、跨区传输费、负载均衡费、监控费，各种杂七杂八的费用加起来，账单比你预期多出一倍都不止。

我一个做 AI 应用的朋友跟我说，他每个月算力花 1 万，流量费居然要花 5 千。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaARXibCwGp6iafK1cvdxOehHTgzgMsSTNE91PRUQRstpcKRVEoObRY0boF6XKD2zibGibnSO7uYRibvwjmos0iaicBwFHr2icLdLboqL5o/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

第三个坑，架构复杂。

业务增长后，你不得不在多个区域部署服务，然后分别接 CDN、WAF、容器编排、日志监控。

每个服务来自不同厂商，出了问题排查链路巨长。

说白了就是： **能跑，但运维成本越来越高，人越来越累。**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaDM6zkxxfzAA7LRZ8GzIltMibzTAib7jxTfL5Y6iaOzpiaXQqbl3pTgzlCazECeXSWl6gJIUwRPnOGLI7f0wbvchQ1o4RlRgeqVe60/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

## 大部分人怎么解决的

目前主流方案就是选 AWS、GCP 这些大厂，然后自己搭一套。

CDN 用 Cloudflare，容器用 EKS，监控用 Datadog，安全再接个第三方。

方案成熟是成熟，但问题也很明显：

贵。而且一旦深度绑定某家云，后面想迁移基本不可能，这就是所谓的「云锁定」。

我之前用过 AWS 的 GPU 实例跑推理，光是出站流量费每个月就让我肉疼。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zw8bZHsVSaCEPwWFKflMrxr8A7ykNcxnnYYa70E2Rqo46z5QethicqsW7G4MCsJxxSjChs0X2utWp6fWmb1xUFajcrF4Jbgbgcyh8Y381F7o/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

0.10 一个 GB，高并发场景下流量费比算力费还高。

麻了。

## 重新认识 Akamai Cloud

后来一个做出海的朋友推荐我看看 Akamai Cloud。

说实话，我第一反应跟大多数人一样：Akamai 不是做 CDN 的吗？

确实，它在 130 多个国家有超过 4400 个边缘节点，CDN 这块一直是行业头部。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zw8bZHsVSaBRvbhADjbuYtse7Fse5J39pMGuG1VdgROXOibVkMQHOfs95twXib2nUUMOgQBFDrnFuYgINgfWj3lxK8GIWkUUHP507RVXvGlVI/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

但我仔细了解之后发现，它现在已经是一个完整的云计算平台了。

CPU、GPU、视频专用处理器这些基础算力都有，也有托管 Kubernetes（LKE，控制平面免费）、边缘 Serverless（基于 WebAssembly）、可观测性平台 TrafficPeak，还有专门给 AI 场景做的 API 网关 Zuplo。

不能说多完美，但对出海场景来说，该有的基本都有了。

让我比较心动的是它的计费模式：

出站流量 $0.005/GB，部分服务还送 1 到 20TB 免费出站额度。

对比 AWS 动辄 0.10/GB 的出站价格，差距确实挺大的。

另外它基于开源技术构建，支持多云部署，不存在厂商锁定的问题。想搬随时能搬，这点我觉得挺重要的。

## Akamai 的 GPU 推理云，聊聊我的了解

除了基础的 IaaS，Akamai 今年还推出了基于 NVIDIA RTX PRO 6000 的 GPU 推理云服务，部署在全球 19 个数据中心节点，覆盖新加坡、东京、孟买、雅加达、法兰克福、洛杉矶等地。

对于做出海 AI 业务的团队来说，这个方案还是值得关注的。我把了解到的几个核心点整理一下。

### 性能和价格

RTX PRO 6000 支持最新的 FP4 精度量化。FP4 在几乎不损失精度的前提下，把显存需求缩小了一倍。而 H100 因为架构原因不支持 FP4，只能用 FP8。

官方 Benchmark 数据显示，RTX PRO 6000 的推理吞吐量最高可比 H100 提升 1.63 倍。

翻译成人话就是： **同样的模型，RTX PRO 6000 能用更少的显存跑出更高的吞吐。**

价格方面，大部分节点 5.40/hr。

跑 Llama 3.3 70B 模型推理，每百万 Token 成本约 $0.31，比 H100 便宜 14%。

另外大厂还有个「隐藏账单」的问题：GCP 按小时收 GPU 租金之外，还会对 CPU、本地存储单独收费。Akamai 是 CPU、存储、网络打包定价的，整体算下来差距还是比较明显的。

### 96GB 显存的优势

消费级 RTX 5090 只有 32GB 显存，跑企业级高并发，动不动就 OOM。

RTX PRO 6000 配备 96GB GDDR7 显存，30B 到 70B 的模型（比如 Llama 3.3 70B、Qwen3-72B）在 FP4 量化后只需约 35GB，单卡可以跑起来。

单卡评估速率达到 225.66 tokens/s，是 NVIDIA L20（84.74 tokens/s）的 2.6 倍。

另外消费级显卡在企业场景有两个硬伤：一是没有 ECC 内存，KV Cache 出错容易导致服务崩溃；二是不支持 GPU Direct 直通技术，多卡通信性能下降严重。

**消费卡适合自己折腾，但真要跑线上业务，还是得用专业卡。**

### 流量成本

这一点我前面提过，再说一下具体数据。

Akamai 出站流量 0.08 到 $0.10/GB，差了差不多 20 倍。

高并发下 Akamai 每一美元可处理 4,723,200 个 Token，GCP 同条件是 2,649,333 个。

对于 AI 推理这种出站流量大的业务，这部分成本差距确实会影响到你最终是赚钱还是亏钱。

### 全球节点分布

传统方案是把 GPU 集群放在美东或者美西，全球用户的请求都回传到中心机房。

对于实时音视频、AI 特效这些对延迟敏感的场景，这种架构体验比较差。

Akamai 把 RTX PRO 6000 部署在 19 个节点，AI 推理可以在离用户更近的位置运行。再加上 4400 个边缘节点的 CDN 网络，延迟方面会有比较明显的改善。

官方数据是全球 95% 的互联网用户可以在 10 毫秒内获得响应，实测从华盛顿节点发往南美的流量延迟比 AWS 低约 15%。

另外还有 AI 防火墙拦截提示词注入、数据窃取等安全威胁，对出海企业来说也是个加分项。

### 一些案例参考

我了解到的一个案例是，某亚太区做情感陪伴的出海企业，之前用大厂 A100，每百万 Token 综合成本在 5 左右。

换到 Akamai 的 RTX 6000 并结合 FP4 量化后，成本降到了 $1.8 左右，整体 AI 成本降了 60%。

还有一家韩国游戏公司，用 RTX 6000（96GB）跑 70B 模型支持游戏内 NPC 实时对话，同时用较老一代的 RTX 4000 Ada（20GB）跑文生图，高低搭配控制成本。

具体效果肯定因场景而异，但至少说明这个方案在某些场景下是可行的。

## 写在最后

做出海这段时间，我最大的感受是：

**选云不能只比服务器单价。**

全球覆盖、流量成本、扩展能力、迁移自由度，这些综合起来才能决定你的业务跑不跑得起来。

Akamai Cloud 对我来说，算是一个之前没太关注但确实值得了解的选项。尤其是流量费和全球节点这两点，对出海场景确实比较友好。

当然，每个团队的业务不一样，适合的方案也不同。我只是把自己了解到的信息分享出来，具体还是要结合自己的场景去评估。

如果你也在做出海业务，或者正在为 AI 推理的成本头疼，评论区聊聊你的方案？

苍何

邀请你前往腾讯公益一起捐

我为家乡上大分

231人捐赠

AI · 目录

作者提示: 个人观点，仅供参考