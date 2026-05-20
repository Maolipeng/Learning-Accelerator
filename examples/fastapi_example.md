# 示例：用 Learning Accelerator Skill 学 FastAPI

## 用户输入

```text
调用 Learning Accelerator Skill，类比 Express 带我快速上手 FastAPI。
```

## 期望输出风格

# 先定位

FastAPI 是 Python 生态里非常流行的 Web API 框架，特别适合 AI 服务、内部工具、RAG 服务、Agent 网关和后端接口。

# 用 Express 类比

Express:

```js
app.get("/hello", (req, res) => {
  res.json({ message: "hello" })
})
```

FastAPI:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

相似点：

- 都是声明路由。
- 都能返回 JSON。
- 都适合写 API 服务。

不同点：

- FastAPI 强依赖 Python 类型提示。
- FastAPI 常和 Pydantic 一起做请求/响应校验。
- FastAPI 天然支持 OpenAPI 文档。

# 最小 Demo

安装：

```bash
pip install fastapi uvicorn
```

创建 `main.py`：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return {"reply": f"你说的是：{req.message}"}
```

启动：

```bash
uvicorn main:app --reload
```

访问文档：

```text
http://127.0.0.1:8000/docs
```

# 实际项目里怎么用

常见结构：

```text
app/
  main.py
  api/
    routes.py
  services/
    chat_service.py
  models/
    schemas.py
  core/
    config.py
```

# 最佳实践

- 请求体用 Pydantic model。
- 业务逻辑不要全写在路由函数里。
- 配置放到 config/env。
- AI 请求建议封装到 service 层。
- 需要并发 IO 时再使用 async。

# 常见坑

- 把所有逻辑写进 `main.py`。
- 在 async 路由里调用阻塞请求。
- 不做异常处理。
- 不区分 schema 和业务模型。

# 回顾

1. FastAPI 和 Express 最大相似点是什么？
2. Pydantic 在 FastAPI 里承担什么作用？
3. 为什么业务逻辑不建议全写在路由函数里？

小练习：写一个 `/summarize` 接口，接收 `{ "text": "..." }`，返回文本长度和一句模拟摘要。
