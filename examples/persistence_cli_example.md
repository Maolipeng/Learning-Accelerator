# 示例：用 CLI 持久化学习状态

## 场景

用户希望 Learning Accelerator 不只在回答里输出“状态更新”，还要把学习画像、当前主题、薄弱点和复习计划保存到本地 JSON，方便下一次继续学习。

## 初始化状态文件

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
```

这会创建一个符合 `references/learning_os_protocol.md` schema 的 JSON 文件。

## 记录学习画像

```bash
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --known-stack JavaScript TypeScript React \
  --goal "用 FastAPI 构建 AI 工具后端" \
  --project "RAG notebook API" \
  --constraint "每天 30 分钟"
```

## 设置当前主题

```bash
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
```

## 记录掌握和薄弱概念

```bash
python -m learning_accelerator.cli --state-file .learning/state.json concept mastered "path operation"
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
```

## 安排复习

```bash
python -m learning_accelerator.cli --state-file .learning/state.json review \
  "dependency injection" \
  "用一句话解释 Depends 解决了什么问题" \
  --result incorrect
```

`incorrect` 会把复习项安排在当前会话或当天再次复习；`correct`、`second_correct`、`third_correct` 会分别使用 1、3、7 天间隔。

## 查看到期复习

```bash
python -m learning_accelerator.cli --state-file .learning/state.json due
```

## Agent 使用方式

当宿主 Agent 有文件访问能力时，可以在每轮学习前读取 `.learning/state.json`，在回答后用 CLI 或 Python API 更新状态。没有文件访问能力时，仍然按 Skill 的 `学习状态 / 状态更新` 区块输出可复制的状态摘要。
