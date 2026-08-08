---
type: clipping
title: "🔥迈向长程智能体：Long-Horizon Agent综述"
source: "https://www.xiaohongshu.com/explore/6a5a0270000000001101bf4b?xsec_token=ABsyW_TufMeYuYUN9kE27a_2egTDunbHyLZvnStWmsoX0=&xsec_source=pc_user"
author:
  - "[[卡卡卡卡比(RUC读博版)]]"
published: 2026-07-22
created: 2026-07-22
description: "3 亿人的生活经验，都在小红书"
tags:
  - "clippings"
status: active
---
![](https://sns-webpic-qc.xhscdn.com/202607220424/debca00f0051b9bf425e247af68c09f2/1040g2sg322niq3mtn43g4b9qfdm3mt0jpr19odo!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/f928f795e1716b8470415d8b3cab5fd5/1040g2sg322niq3mtn4004b9qfdm3mt0jvoproio!nd_dft_wlteh_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/2858e97995359df597b270e6e2ff8578/1040g2sg322niq3mtn40g4b9qfdm3mt0jg05rjpg!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/bf70ba23de91df9c6d3f1d6f96921b1a/1040g2sg322niq3mtn4104b9qfdm3mt0jednjhm0!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/202ef3b38ca86cf2ff316d2d8559b3e3/1040g2sg322niq3mtn41g4b9qfdm3mt0jt68l11g!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/b0ccaf55787ea2030289bd6ec080242c/1040g2sg322niq3mtn4204b9qfdm3mt0j0045u6o!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/bbeaaeff518cdad0fa3852c2154cc644/1040g2sg322niq3mtn42g4b9qfdm3mt0jjfn0ci0!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/196f715a527338fe376189c5e3a2ddd4/1040g2sg322niq3mtn4304b9qfdm3mt0j7uprjro!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/debca00f0051b9bf425e247af68c09f2/1040g2sg322niq3mtn43g4b9qfdm3mt0jpr19odo!nd_dft_wgth_webp_3) ![](https://sns-webpic-qc.xhscdn.com/202607220424/f928f795e1716b8470415d8b3cab5fd5/1040g2sg322niq3mtn4004b9qfdm3mt0jvoproio!nd_dft_wlteh_webp_3)

1/8

🔥迈向长程智能体：Long-Horizon Agent综述

📖 欢迎关注我们在长程智能体「Long-Horizon Agent」领域的最新综述！ 百页长文，把"智能体如何完成超长时间跨度的任务"从 0 到 1 讲透！ 📌 核心干货速览 📈 智能体能自主完成任务的时间跨度正在指数级增长（每 7 个月翻一倍），从单个长窗口任务，一路卷到跨窗口、跨会话，乃至永不停机的开放式任务流。本文系统性地梳理了长程智能体方向，并将"长程能力"刻画为 Harness Engineering 与 Model Optimization 协同演化的产物：显式的 Harness 能力会逐步内化进模型策略，而更强的策略又反过来支撑更强的 Harness。 🔍 全文围绕六大视角展开： Foundations：长程能力的定义与难度分级 Evolution：提示工程 → 上下文工程 → Harness 工程 Harnesses：循环与工作流、上下文与记忆、工具/MCP 与技能、编排、Hooks、校验 Optimization：架构、数据/环境合成、预/中训练、微调，强化学习、策略蒸馏、自我演化 Applications：软件工程、信息检索、Computer Use、多模态、通用智能体 Frontiers：展望演进性、有效性、效率、可信性四大方向 欢迎长程智能体方向的朋友们关注与交流，希望大家点点 star 与 follow 🌟🌟🌟，我们会持续迭代更新！ 代码仓库：RUC-NLPIR/Awesome-Long-Horizon-Agents [#人工智能](https://www.xiaohongshu.com/search_result?keyword=%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD&type=54&source=web_note_detail_r10) [#大模型](https://www.xiaohongshu.com/search_result?keyword=%25E5%25A4%25A7%25E6%25A8%25A1%25E5%259E%258B&type=54&source=web_note_detail_r10) [#Agent](https://www.xiaohongshu.com/search_result?keyword=Agent&type=54&source=web_note_detail_r10) [#智能体](https://www.xiaohongshu.com/search_result?keyword=%25E6%2599%25BA%25E8%2583%25BD%25E4%25BD%2593&type=54&source=web_note_detail_r10) [#LLM](https://www.xiaohongshu.com/search_result?keyword=LLM&type=54&source=web_note_detail_r10) [#强化学习](https://www.xiaohongshu.com/search_result?keyword=%25E5%25BC%25BA%25E5%258C%2596%25E5%25AD%25A6%25E4%25B9%25A0&type=54&source=web_note_detail_r10) [#iclr](https://www.xiaohongshu.com/search_result?keyword=iclr&type=54&source=web_note_detail_r10) [#多模态大模型](https://www.xiaohongshu.com/search_result?keyword=%25E5%25A4%259A%25E6%25A8%25A1%25E6%2580%2581%25E5%25A4%25A7%25E6%25A8%25A1%25E5%259E%258B&type=54&source=web_note_detail_r10) [#agent](https://www.xiaohongshu.com/search_result?keyword=agent&type=54&source=web_note_detail_r10) [#waic](https://www.xiaohongshu.com/search_result?keyword=waic&type=54&source=web_note_detail_r10)

说点什么...

56450357

<iframe src=""></iframe>