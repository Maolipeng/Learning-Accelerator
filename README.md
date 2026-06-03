# Learning Accelerator: AI Learning OS

这是一个可复用的动态学习 Agent Skill。它不只是讲解模板，而是一个轻量 AI Learning OS：负责学习状态、复盘、间隔重复、项目驱动学习、练习生成、回顾问题生成、代码错误分析和难度自适应。

它适合用来学习新语言、新框架、新工具、新技术，比如：

- Python
- FastAPI
- asyncio
- MCP
- RAG
- WebGPU
- Rust
- Kubernetes
- LangChain
- Pydantic

核心思想：

> 不只是看懂语法，而是通过“状态记录 + 类比 + 实践 + 项目 + 复习 + 错误诊断 + 难度调整”建立可持续学习闭环。

## 文件说明

```text
.
├── SKILL.md                  # 标准 Skill 入口，包含 frontmatter 和使用流程
├── SYSTEM_PROMPT.md          # 不支持 Skill 的 Agent 可直接使用的系统提示词
├── agents/
│   └── openai.yaml           # OpenAI/Codex 侧 UI 元数据
├── manifest.json             # 通用安装/兼容性元数据
├── learning_accelerator/      # JSON 持久化实现和 CLI 工具
│   ├── __init__.py
│   ├── state.py
│   └── cli.py
├── references/
│   └── learning_os_protocol.md # 学习状态、复习、练习、错误诊断协议
├── examples/
│   ├── python_function_example.md
│   ├── fastapi_example.md
│   ├── persistence_cli_example.md
│   ├── code_error_diagnosis_example.md
│   └── project_learning_example.md
├── tests/
│   ├── test_skill_structure.py
│   ├── test_state_store.py
│   └── test_cli.py
├── pyproject.toml             # pytest/coverage/console script 配置
├── .gitignore                 # 忽略本地缓存、覆盖率和示例状态文件
└── .github/workflows/ci.yml   # 单元测试和覆盖率 CI
```

## 如何使用

### 方式一：作为 Skill 安装

把本仓库复制到目标 Agent 的 skills 目录，确保平台能读取 `SKILL.md`。

如果你在本仓库根目录执行，推荐只复制 Skill 运行需要的文件，避免把 `.git`、本地缓存和临时状态一起带过去：

```bash
rm -rf ~/.codex/skills/learning-accelerator
mkdir -p ~/.codex/skills/learning-accelerator
cp -R SKILL.md SYSTEM_PROMPT.md README.md manifest.json agents examples references learning_accelerator pyproject.toml \
  ~/.codex/skills/learning-accelerator/
```

如果你在本仓库的父目录执行，也可以复制当前项目目录名：

```bash
rm -rf ~/.codex/skills/learning-accelerator
cp -R Learning-Accelerator ~/.codex/skills/learning-accelerator
```

### 方式二：使用本地持久化和 CLI

本仓库内置一个零第三方运行时依赖的 JSON 状态存储，可用于真实记录学习画像、当前主题、掌握/薄弱概念和复习计划。

初始化状态文件：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
```

记录用户画像：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --known-stack JavaScript TypeScript React \
  --goal "学习 FastAPI 并构建 AI API" \
  --project "RAG notebook API"
```

设置主题、记录薄弱点并安排复习：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json review "dependency injection" "解释 Depends 解决的问题" --result incorrect
python -m learning_accelerator.cli --state-file .learning/state.json due
```

如果想使用 console script，先在仓库根目录安装为可编辑包：

```bash
python -m pip install -e .
learning-accelerator --state-file .learning/state.json show
```

更多命令见 `examples/persistence_cli_example.md`。

### 方式三：作为通用提示词

如果目标 Agent 没有 Skill 机制，把 `SYSTEM_PROMPT.md` 内容放到 Agent/System Prompt 中。

### 方式四：作为学习模板

每次学习新主题时，输入：

```text
调用 Learning Accelerator Skill，作为 AI Learning OS 带我学习 Python async/await：记录状态、安排复习、生成练习，并根据我的代码错误调整难度。
```

## 示例场景

当前示例覆盖：

- Python 函数学习：`examples/python_function_example.md`
- FastAPI 入门：`examples/fastapi_example.md`
- CLI 持久化：`examples/persistence_cli_example.md`
- 代码错误诊断：`examples/code_error_diagnosis_example.md`
- 项目驱动学习：`examples/project_learning_example.md`

## 本地测试和覆盖率

```bash
python -m pytest
```

如需在本地生成覆盖率报告，先安装 `pytest-cov`，再运行：

```bash
python -m pytest --cov=learning_accelerator --cov-report=term-missing --cov-report=xml
```

`pyproject.toml` 已配置 coverage 阈值和报告规则；CI 配置位于 `.github/workflows/ci.yml`，会在 push 和 pull request 时安装 `pytest-cov` 并运行单元测试与覆盖率检查，生成 `coverage.xml`。
