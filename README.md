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
├── references/
│   └── learning_os_protocol.md # 学习状态、复习、练习、错误诊断协议
├── examples/
│   ├── python_function_example.md
│   └── fastapi_example.md
└── tests/
    └── test_skill_structure.py
```

## 如何使用

### 方式一：作为 Skill 安装

把整个目录复制到目标 Agent 的 skills 目录，确保平台能读取 `SKILL.md`。

示例：

```bash
cp -R learning-agent-skill-prompt ~/.codex/skills/learning-accelerator
```

### 方式二：作为通用提示词

如果目标 Agent 没有 Skill 机制，把 `SYSTEM_PROMPT.md` 内容放到 Agent/System Prompt 中。

### 方式三：作为学习模板

每次学习新主题时，输入：

```text
调用 Learning Accelerator Skill，作为 AI Learning OS 带我学习 Python async/await：记录状态、安排复习、生成练习，并根据我的代码错误调整难度。
```

## 本地测试

```bash
cd learning-agent-skill-prompt
python3 tests/test_skill_structure.py
```

测试会检查核心文件、Skill frontmatter、Agent 元数据和关键教学模块。
