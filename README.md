# Learning Accelerator: General Learning OS

这是一个可复用的通用动态学习 Agent Skill。它不只是讲解模板，而是一个轻量 General Learning OS：负责学习状态、复盘、间隔重复、任务驱动学习、练习生成、回顾问题生成、错误诊断和难度自适应。

它适合用来学习任何需要持续练习和复盘的主题。技术学习只是其中一个领域，比如：

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

也可以用于非技术学习，比如：

- 英语、日语、法语等语言学习
- 数学、物理、历史、心理学等学科
- 写作、演讲、沟通、设计、摄影
- 财务、法律常识、产品管理
- 健身、营养、考试备考

它不要求用户预先懂前端或编程。用户可以是零基础、小白、非程序员，也可以是前端、后端、数据、运维、产品技术或 AI 应用开发者；系统会先询问当前技能和背景，再选择合适的类比、练习和难度。

核心思想：

> 不只是看懂知识点，而是通过“状态记录 + 类比 + 实践 + 任务 + 复习 + 错误诊断 + 难度调整”建立可持续学习闭环。

## 文件说明

```text
.
├── AGENTS.md                 # 通用 coding agent 入口说明
├── CLAUDE.md                 # Claude Code 适配说明
├── GEMINI.md                 # Gemini CLI 项目级说明
├── SKILL.md                  # 标准 Skill 入口，包含 frontmatter 和使用流程
├── SYSTEM_PROMPT.md          # 不支持 Skill 的 Agent 可直接使用的系统提示词
├── .cursor/
│   └── rules/
│       └── learning-accelerator.mdc # Cursor rules 入口
├── agents/
│   └── openai.yaml           # OpenAI/Codex 侧 UI 元数据
├── docs/
│   └── platforms.md          # Codex/Claude/Cursor/Gemini/通用 Agent 适配矩阵
├── manifest.json             # 通用安装/兼容性元数据
├── learning_accelerator/      # JSON 持久化实现和 CLI 工具
│   ├── __init__.py
│   ├── state.py
│   └── cli.py
├── references/
│   └── learning_os_protocol.md # 学习状态、复习、练习、错误诊断协议
├── examples/
│   ├── no_prior_programming_example.md
│   ├── language_learning_example.md
│   ├── non_technical_learning_example.md
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

Codex:

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

安装后，在 Codex 里可以这样触发：

```text
调用 learning-accelerator，带我学习 FastAPI dependency injection。先问我目前熟悉哪些技能或工具，再根据我的背景讲清楚它解决什么问题，最后给我一个小练习并安排复习。
```

Claude Code:

```bash
rm -rf ~/.claude/skills/learning-accelerator
mkdir -p ~/.claude/skills/learning-accelerator
cp -R SKILL.md SYSTEM_PROMPT.md README.md manifest.json AGENTS.md CLAUDE.md agents examples references learning_accelerator pyproject.toml \
  ~/.claude/skills/learning-accelerator/
```

也可以把本仓库放在 Claude Code 项目中，使用 `CLAUDE.md` 作为项目记忆入口。

Claude Code 使用示例：

```text
Use the Learning Accelerator skill. First ask what skills and tools I already know, then review my weak FastAPI concepts and update the local learning state after I answer.
```

Gemini CLI:

把 `GEMINI.md` 保留在项目根目录；需要完整行为约束时，让 Agent 继续读取 `SYSTEM_PROMPT.md` 和 `references/learning_os_protocol.md`。

Gemini CLI 使用示例：

```text
根据 GEMINI.md 里的 Learning Accelerator 规则，先确认我的当前技能水平，再帮我复习今天到期的内容，并输出下一步项目任务。
```

Cursor:

把 `.cursor/rules/learning-accelerator.mdc` 保留在项目中，或复制到目标 Cursor 项目的 `.cursor/rules/` 目录。

Cursor 使用示例：

```text
按 Learning Accelerator 规则分析我这个 FastAPI 报错，指出缺失概念，给最小修复和一个针对性练习。
```

### 方式二：作为通用 coding agent 入口

如果目标工具支持项目级说明文件，可以优先使用：

- `AGENTS.md`：适合 Cursor、Windsurf、Aider 和其他能读取项目说明的 coding agent。
- `CLAUDE.md`：适合 Claude Code 项目记忆或 Claude Code skill 安装说明。
- `GEMINI.md`：适合 Gemini CLI 项目级说明。
- `.cursor/rules/learning-accelerator.mdc`：适合 Cursor rules。
- `SYSTEM_PROMPT.md`：适合只支持 system/developer prompt 的 Agent。

跨平台适配矩阵见 `docs/platforms.md`。

通用 coding agent 使用示例：

```text
请先读取 AGENTS.md，把这个仓库当成 Learning Accelerator。开始前先问我熟悉哪些技能、工具和概念；我要用任务驱动方式学习 asyncio，每轮都记录薄弱点、练习结果和下次复习项。
```

### 方式三：使用本地持久化和 CLI

本仓库内置一个零第三方运行时依赖的 JSON 状态存储，可用于真实记录学习画像、当前主题、掌握/薄弱概念和复习计划。

初始化状态文件：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
```

记录用户画像：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --domain technology \
  --known-stack JavaScript TypeScript React \
  --known-skill "React" \
  --known-skill "TypeScript" \
  --experience-level intermediate \
  --goal "学习 FastAPI 并构建 AI API" \
  --project "RAG notebook API"
```

开始一条新学习线前，可以先输出 onboarding 问题：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json onboarding --domain language
python -m learning_accelerator.cli --state-file .learning/state.json domain-template language
```

如果用户完全零基础，可以这样记录：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --domain general \
  --experience-level no_programming \
  --goal "从零开始学习 Python"
```

非技术学习也可以这样记录：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --domain language \
  --known-skill "中文拼音" \
  --experience-level beginner \
  --goal "通过日语 N5" \
  --outcome "能读写基础假名"
```

设置主题、记录薄弱点并安排复习：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json review "dependency injection" "解释 Depends 解决的问题" --result incorrect
python -m learning_accelerator.cli --state-file .learning/state.json task add "每天复习 5 个假名"
python -m learning_accelerator.cli --state-file .learning/state.json due
```

完成复习、记录练习结果，并输出给 Agent 用的上下文：

```bash
python -m learning_accelerator.cli --state-file .learning/state.json review-complete "<review-id-from-due>" --result correct
python -m learning_accelerator.cli --state-file .learning/state.json exercise complete "Build /ask mock API" --concept "FastAPI route"
python -m learning_accelerator.cli --state-file .learning/state.json summary
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
```

一轮真实学习落盘流程：

```bash
# 1. Agent 开始前读取上下文
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context

# 2. 查询今天要复习的内容
python -m learning_accelerator.cli --state-file .learning/state.json due

# 3. 用户完成复习后归档，并按结果安排下一次复习
python -m learning_accelerator.cli --state-file .learning/state.json review-complete "<review-id-from-due>" --result correct

# 4. 用户完成练习后记录结果，作为难度调整证据
python -m learning_accelerator.cli --state-file .learning/state.json exercise complete \
  "Implement FastAPI mock /ask endpoint" \
  --concept "FastAPI route" \
  --notes "独立完成 route/schema/service 分层"

# 5. Agent 结束前读取结构化摘要
python -m learning_accelerator.cli --state-file .learning/state.json summary
```

如果想使用 console script，先在仓库根目录安装为可编辑包：

```bash
python -m pip install -e .
learning-accelerator --state-file .learning/state.json show
```

更多命令见 `examples/persistence_cli_example.md`。

### 方式四：作为通用提示词

如果目标 Agent 没有 Skill 机制，把 `SYSTEM_PROMPT.md` 内容放到 Agent/System Prompt 中。

使用示例：

```text
系统提示词使用 SYSTEM_PROMPT.md。用户输入：我熟悉 TypeScript 和 React，请用 Learning Accelerator 的方式带我学 Pydantic，并把本轮状态更新输出在最后。
```

### 方式五：作为学习模板

每次学习新主题时，输入：

```text
调用 Learning Accelerator Skill，作为 General Learning OS 带我学习 Python async/await：记录状态、安排复习、生成练习，并根据我的错误调整难度。
```

## 示例场景

当前示例覆盖：

- 零编程基础入门：`examples/no_prior_programming_example.md`
  - 输入示例：`调用 Learning Accelerator Skill。我完全没有编程基础，带我学习 Python 函数。`
- 日语学习：`examples/language_learning_example.md`
  - 输入示例：`调用 Learning Accelerator Skill。我想学日语，目标是通过 N5。我会中文拼音。`
- 非技术学习：`examples/non_technical_learning_example.md`
  - 输入示例：`调用 Learning Accelerator Skill。我想提升公开演讲能力，平时不写代码，也没有技术背景。`
- Python 函数学习：`examples/python_function_example.md`
  - 输入示例：`调用 Learning Accelerator Skill，带我学习 Python 函数，类比 JS 函数讲。`
- FastAPI 入门：`examples/fastapi_example.md`
  - 输入示例：`调用 Learning Accelerator Skill，类比 Express 带我快速上手 FastAPI。`
- CLI 持久化：`examples/persistence_cli_example.md`
  - 使用示例：`python -m learning_accelerator.cli --state-file .learning/state.json prompt-context`
- 代码错误诊断：`examples/code_error_diagnosis_example.md`
  - 输入示例：`帮我分析这个 FastAPI 报错，并更新我的薄弱点。`
- 项目驱动学习：`examples/project_learning_example.md`
  - 输入示例：`用一个小项目带我学 RAG API 后端。我熟悉 React 和 Node.js，不熟 FastAPI。`

## 本地测试和覆盖率

```bash
python -m pytest
```

如果本地还没有测试依赖，先安装开发依赖：

```bash
python -m pip install -e ".[dev]"
```

如果你的 pip 版本较旧导致 editable install 失败，先升级 pip：

```bash
python -m pip install --upgrade pip
```

如需在本地生成覆盖率报告，先安装 `pytest-cov`，再运行：

```bash
python -m pytest --cov=learning_accelerator --cov-report=term-missing --cov-report=xml
```

`pyproject.toml` 已配置 coverage 阈值和报告规则；CI 配置位于 `.github/workflows/ci.yml`，会在 push 和 pull request 时安装 `pytest-cov` 并运行单元测试与覆盖率检查，生成 `coverage.xml`。
