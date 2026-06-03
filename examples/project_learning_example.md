# 示例：项目驱动学习 RAG API

## 用户输入

```text
调用 Learning Accelerator Skill，用一个小项目带我学 RAG API 后端。我熟悉 React 和 Node.js，不熟 FastAPI。
```

## 期望输出风格

## 先定位

RAG API 后端可以理解成“React 前端和向量检索/LLM 之间的稳定服务层”。它负责接收问题、检索相关文档、拼接上下文、调用模型，并把结果返回给前端。

## 用 Node/Express 类比

- FastAPI route ≈ Express route handler。
- Pydantic schema ≈ TypeScript interface + 运行时校验。
- service 层 ≈ Express 项目里的业务模块。

类比边界：TypeScript 类型主要在编译期保护你；Pydantic 会在请求进入服务时做运行时校验。

## 本轮项目任务

先实现一个不接真实模型的 `/ask` mock API，目标是把目录结构、schema、route、service 分层跑通。

```text
app/
  main.py
  api/routes.py
  models/schemas.py
  services/rag_service.py
```

## 验收标准

- `POST /ask` 接收 `{ "question": "..." }`。
- 返回 `{ "answer": "mock: ...", "sources": [] }`。
- route 不直接拼业务答案，而是调用 service。
- schema 文件只放请求/响应结构。

## 回顾问题

1. 为什么 route 不应该塞满业务逻辑？
2. Pydantic schema 和 TypeScript interface 最大区别是什么？
3. 如果下一步接真实 LLM，错误处理应该放在哪一层？

## 下一步

把 mock service 替换成“检索函数 + 生成函数”两个小函数，但先不要接真实数据库，避免一次引入太多概念。
