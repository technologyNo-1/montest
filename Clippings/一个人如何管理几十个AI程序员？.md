---
type: clipping
title: "一个人如何管理几十个AI程序员？"
source: "https://mp.weixin.qq.com/s/zxjYSGzgEoDyrcpdupEQ-w"
author:
  - "[[刘小排]]"
published:
created: 2026-07-21
description: "高手能每天有效烧几十亿Token的秘密。"
tags:
  - "clippings"
status: active
---
刘小排 刘小排r *2026年7月21日 00:06*

哈喽，大家好，我是刘小排。先给你们看张图。

OpenClaw 的作者 Peter Steinberger，前几天发了条推，就一句话：

「这大概就是我的 Mac Studio 能处理的最多会话数了。」

配图是他的 Codex 界面。

![图片](https://mmbiz.qpic.cn/mmbiz_png/q6aOmBZKAbN9vq2x1PIWLwprIibfibN7cmxKsdW8fwCcyWdggWqCeOmPeTIpiaYS65vYIqTXM4bicBVRv2UOomkLZ8dAiaM5kTbLPaKicBgibh6UBw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

我数了一下，三十多个任务，同时在跑。

删死代码的，修测试的，重构模块的，优化 Web UI 的……

底下他还补了一句：我通过 Jump Desktop 把工作分发到了大概五台机器上，这只是配置最强的那台。

好家伙。一个人，五台机器，几十个 AI 任务并行。这已经不是在写代码了，这是在开厂。

## 问题来了

我猜很多人第一反应是：他也开这么多？好猛。

第二反应是：等等，这些任务不会打架吗？

几十个 Agent 同时改一个项目的代码，你改我也改，最后不就乱套了？

问得好。

答案是：它们不在同一个目录里干活。每个任务，都有自己独立的一份代码。

靠的是 Git 的一个老功能，叫 **Worktree。**

要讲清楚它，得先把它和分支（Branch）掰开。

对了，提前说一下，Worktree其实是Git的一个很老的功能，早就有了，只不过以前的使用门槛比较高，用起来不方便，所以只有高级的程序员才会偶尔用到它。而今天我们已经有了Codex、Claude Code等先进的AI编程工具， **所以Worktree功能值得我们重新审视—— 它的使用门槛大大降低、好处又是无可替代的。**

上面我所谓的“使用门槛大大降低”，但还有一个唯一的门槛 —— 你需要明白这两个词到底是什么意思，以及什么时候该用谁。然后，你只需要用大白话告诉Codex、Claude Code启用即可。

## 分支和 Worktree，到底啥区别

打个比方。

**分支是「代码往哪个方向走」。**

主干是国道，分支是岔路。修 Bug 走一条岔路，做新功能走另一条岔路，最后汇合。

**Worktree 是「同时打开几个代码现场」。**

同一个项目，同一个仓库，但在硬盘上铺开成好几个独立目录。这个目录在改登录，那个目录在修支付，互不干扰。

一句话总结：

> 分支管「路线」，Worktree 管「现场」。

以前我们是一个人在几条路线之间来回切换——stash、切分支、改完、切回来，任务一多，脑子和代码一起乱。

现在是几条路线各自有自己的现场，同时开工。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/q6aOmBZKAbOWib5Tj4BdCEgXMbjZ3htER8Zc3JAqDNodiaKeaic4LXVPCVuH8voGxHZhLxtFZJqibEQf3BpzSRycEJwOQRbibYQFeG4qCoibcTXXU/640?wx_fmt=png&from=appmsg#imgIndex=1)

## 什么时候用分支，什么时候用 Worktree？五种情况

这是大家最容易迷糊的地方。我拿独立开发者做海外 AI 产品的场景，从简到繁讲五种：

**第一种：分支都不开，直接在 main 上改。**

改个 Landing Page 文案、调个定价、修个 typo、换个 OG 图。

这种五分钟的事，开分支都是浪费生命，直接在 main 上改完提交，推上去 Vercel 自动部署，收工。

**第二种：只开分支。**

要上大活儿了：重构整个鉴权系统、把数据库从 Supabase 迁到 Neon、给 AI 写作工具加订阅体系。

这种改动大、周期长、随时可能要推倒重来的活，必须开分支，给 main 留一条随时能回滚的退路。但你是一个人串行在做，一个目录就够了，不需要 Worktree。

**第三种：同一个分支，开多个 Worktree。**

这是很多人会漏掉、但 AI 时代特别好用的一种。

比如你在做一个超大的支付模块，路线只有一条（一个 payment 分支），但下面要同时接五个 provider：Stripe、Lemon Squeezy、Paddle、Creem、PayPal。

这五家都在同一个分支的势力范围内，没必要各开一条岔路。但它们可以同时做——一个 Worktree 接一个 provider，五个 Agent 并行，做完一起合回 payment 分支。

再比如你的 AI 图片站要接五个模型 provider：OpenAI、Gemini、Replicate、fal、Flux——同一个道理。

如果你不能熟练应用Worktree的话，那你可能只能串行接入。 **也不是不行，就是慢一点。**

**第四种：分支 + Worktree 一起上。**

多条路线，同时进行。

你的 AI 产品这周的排期是：重做落地页（feature-landing）、修订阅 Bug（fix-billing）、把最新发布的 Claude Sonnet 5 接进对话模块（feature-claude）。

路线不同，各开分支；每条分支派一个 Agent 驻场，各配一个 Worktree：

```
分支：feature-landing / fix-billing / feature-claude
现场：~/landing     / ~/billing   / ~/claude
```

三路并行，互不干扰，你负责 review 和合并。

**第五种：全矩阵拉满——Peter 模式。**

多条分支，每条分支再开多个 Worktree，甚至分发到多台机器。

产品做大了之后就是这样：支付模块下三个 provider 并行、增长模块下 SEO 页面和 Referral 系统并行、核心模块下模型升级和上下文优化并行……十几二十个现场同时开工。

这就是 Peter 那张截图里的世界。判断标准就一条： **你的任务是几件、几层？一件不用开，一件大的开分支，一件下面有并行子任务就一树枝多房间，几件大事就分支配 Worktree，几十件——欢迎来到全矩阵。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/q6aOmBZKAbMV7x74G4GovWhtQwXjWz1oVFjuoeNjBRJtGE0jic7FWHic5hUEaVRwh7lAiaRpdibiccuZuD81dibQDdd2EUvJyfKibPcx5aQ6BsUpU8/640?wx_fmt=png&from=appmsg#imgIndex=2)

## 这个时代的独立开发者，应该怎么做

Peter 是顶级开发者，但这件事对独立开发者的启发，比对大厂程序员的更大。

为什么？因为大厂的瓶颈从来不在写代码，在流程、在协调、在开会。而独立开发者没有这些包袱—— **AI 并行开发的红利，几乎是为一个人做产品的人量身定做的。**

我的看法，三条：

**第一，练的第一项能力不是写代码，是拆任务。**

以前是「这个需求我怎么实现」，现在是「这个需求怎么拆成五个互不干扰的任务，同时派给五个 Agent」。

拆得好，五个 Agent 各干各的，一晚上顶过去一周。拆得不好，五个 Agent 互相改对方的代码，你花一晚上收拾残局。

**任务拆解能力，就是这个时代开发者的第一道分水岭。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/q6aOmBZKAbNHDZ4Ren9zCpQrtzUja2ibeGQHrcHojCeLluyVk35FTmfUD0DVIqbms0LtF4yiaNfB9JMubMxusC2aLVHw4SgWhEMzbaUXtBtP8/640?wx_fmt=png&from=appmsg#imgIndex=3)

**第二，基础设施要先于功能投入。**

很多人一上来就让 AI 写功能，写到第五个项目就崩了——测试没有、CI 没有、代码规范没有，Agent 越多，产出越乱。

Peter 那张截图里一大半任务是什么？删死代码、修测试、修 CI、加固依赖。

看明白了吗？ **顶级开发者派给 AI 的活儿，大头是维护地基，不是盖楼。**

地基越稳，你敢同时派的 Agent 就越多。这才是真正的杠杆。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/q6aOmBZKAbOtDUaZicyWWZicCRxByqjmXRRD3lDTV9QfKTwnYcZ3YVMIw0q9p7D9hkYvRXyCVV6Fz5nMlTDqpRQX9gHKibgktaRAgLXAKAKNBo/640?wx_fmt=png&from=appmsg#imgIndex=4)

**第三，一个人就是一支队伍，但你要当产品经理，别当码农。**

当你的「手」变成几十个 Agent 之后，你最稀缺的资源就不再是时间，而是判断力：

- 做什么功能，不做什么功能；
- 哪个任务优先，哪个砍掉；
- Agent 交上来的代码，合还是不合。

写代码的人遍地都是了（虽然都是 AI）， **知道该写什么的人，值钱了。**

独立开发者最大的机会就在这：以前你输给团队，是因为你一双手干不过人家十双。现在人手不再稀缺，拼的是产品感觉和决策质量——这恰恰是独立开发者的主场。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/q6aOmBZKAbNFichVGPXq80hcujKHmyHQDCLgPTNXFUaRP70t5VumC2uCLb8Gliamk6giaO0ic7H8cUwE5lQdtJd88d2LH9vykYgNYjHTia8Fveos/640?wx_fmt=png&from=appmsg#imgIndex=5)

## 最后

Peter 那张截图，表面上是「大佬好卷」，实际上是一种新的工作形态：

**程序员的角色，从写代码的人，变成了管代码任务的人。**

你的产出不再取决于打字有多快，而 **取决于你能同时管理多少个并行的 AI 任务、同时协调多少个AI员工。**

下次有人问你 AI 编程跟以前有啥不一样，你可以告诉他：

> 以前一个程序员一个工位（碳基工位）。
> 
> 现在一个程序员带着几十个 AI，每个AI都得给它配一个工位（硅基工位）。

如果要一句话总结的话：

**分支是排班的、Worktree 是发工位的。**

**两者结合运用，你就是AI时代最靓的老板！**

**了解更多AI编程技巧↓**

**微信扫一扫赞赏作者**