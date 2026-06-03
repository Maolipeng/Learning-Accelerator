# 示例：代码错误诊断 + 难度调整

## 用户输入

```text
调用 Learning Accelerator Skill，帮我分析这个 FastAPI 报错，并更新我的薄弱点：

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "upper": item_id.upper()}

报错：AttributeError: 'int' object has no attribute 'upper'
```

## 期望输出风格

## 学习状态

- 当前目标：理解 FastAPI 路径参数和 Python 类型
- 薄弱点：类型标注不等于任意对象都拥有字符串方法
- 本轮模式：代码错误诊断

## 失败路径

FastAPI 会根据 `item_id: int` 把路径参数转换成整数。进入函数后，`item_id` 是 `int`，而 `.upper()` 是字符串方法，所以运行时报错。

## 根因

你把“HTTP 路径里收到的是字符串”和“FastAPI 传给函数的是类型转换后的值”混在一起了。

## 最小修复

如果你想保留整数 ID：

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "double": item_id * 2}
```

如果你真的需要字符串方法：

```python
@app.get("/items/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id, "upper": item_id.upper()}
```

## 针对性练习

写两个接口：

1. `/square/{n}`：`n` 是 `int`，返回平方。
2. `/shout/{word}`：`word` 是 `str`，返回大写。

## 状态更新

- 新增薄弱点：FastAPI 路径参数类型转换
- 待复习：解释 `item_id: int` 对请求处理的影响
- 难度调整：保持同级，先巩固类型转换证据
