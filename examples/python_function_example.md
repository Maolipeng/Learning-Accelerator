# 示例：用 Learning Accelerator Skill 学 Python 函数

## 用户输入

```text
调用 Learning Accelerator Skill，带我学习 Python 函数，类比 JS 函数讲。
```

## 期望输出风格

# 先定位

Python 函数和 JS 函数一样，都是把一段可复用逻辑封装起来。但 Python 更强调可读性、显式参数和简单的调用方式。

# 用 JS 类比

JS:

```js
function add(a, b) {
  return a + b
}
```

Python:

```python
def add(a, b):
    return a + b
```

你可以把 `def` 理解成 JS 的 `function`，但 Python 用缩进表示函数体，不用 `{}`。

# 最小 Demo

```python
def greet(name: str) -> str:
    return f"hello, {name}"

print(greet("Mao"))
```

运行：

```bash
python3 demo.py
```

输出：

```text
hello, Mao
```

# 最佳实践

- 现代 Python 推荐写类型提示。
- 函数尽量只做一件事。
- 不要用可变对象作为默认参数。
- 复杂返回值可以用 dict、dataclass 或 Pydantic model 表达。

# 常见坑

```python
def add_item(items=[]):
    items.append("x")
    return items
```

这个 `[]` 只会在函数定义时创建一次，后续调用会复用同一个列表。

推荐写法：

```python
def add_item(items=None):
    if items is None:
        items = []
    items.append("x")
    return items
```

# 回顾

1. `def` 和 JS 的 `function` 有什么相似点？
2. Python 为什么靠缩进表示作用域？
3. 为什么默认参数不要随便写 `[]`？

小练习：写一个函数，接收一个字符串列表，返回每个字符串的长度。
