# 第七章学习断点

## 当前阶段

阶段 2：理解并按教学文档实现 `Config`，已完成最小测试与模块复盘。

## 已讨论

- 为什么框架内部需要 `Message`，而不是始终使用纯 `dict`
- `MessageRole` 为什么要限制允许的角色集合
- `timestamp` 为什么默认生成，但仍应保留显式传入能力
- 为什么内部消息字段不能全部发送给模型 API
- `Message` 的内部模型与外部 API 协议之间需要转换边界
- `BaseModel` 同时提供数据校验和统一数据模型机制
- 核心字段与附加字段的接口设计差异
- 将组件测试保存在独立的 `tests/test_message.py`，作为后续调试和 Agent 开发闭环的基础
- 配置集中管理可以统一默认值，并让模块不必重复读取环境变量
- 环境变量覆盖默认值，可以在不同部署环境切换配置而不修改源码
- 教学版对数值环境变量直接转换并 fail-fast，生产版再补充更友好的错误上下文
- `Config.to_dict()` 使用 Pydantic v2 的 `model_dump()` 导出完整配置

## 设计记录

- 架构讨论入口在 `ARCHITECTURE_QA.md`，各模块记录位于 `chapter7/qa/`
- 当前实现阶段以第七章教学文档源码为准
- 当前跟随文档的模块顺序和学习目标，不盲目复制源码
- 发现文档设计不严谨时可以直接 challenge，并记录教学写法与优化方向
- 学习阶段默认只记录问题，不立即修正；模块或阶段结束后统一复盘优化
- 只有阻塞运行、破坏当前概念或明显误导时才立即修正

## 阶段结果

- 当前 `Message` 阶段测试已通过：10 tests passed
- 文档源码中的 `timestamp`、`metadata` 和 `**kwargs` 问题已记录，暂不优化
- 当前 `Config` 阶段测试已通过：9 tests passed
- Config QA 已拆分到 `chapter7/qa/config.md`
- Config 阶段已完成；当前未处理的问题已记录，暂不提前生产化

## 下一次任务建议

开始前先阅读：

1. `AGENTS.md`
2. `chapter7/LEARNING_STATE.md`
3. `chapter7/ARCHITECTURE_QA.md`
4. 第七章中文版的 7.3.2 节

下一阶段：等待用户明确开始后，进入下一个教学模块。当前任务不提前进入 `Agent` 或 `LLM`。
