# Story Format

## 用途

单个 Story/Issue 的格式模板。

## 使用场景

`story` skill 创建 Issues 时使用此格式。

## Issue 标题格式

```
[PRD-NNNN] <垂直切片描述> — <核心行为>
```

**规则**：
- `[PRD-NNNN]` — 所属 PRD 编号（稳定短引用）
- `<垂直切片描述>` — 一句话描述这个切片的范围
- `—` — 分隔符（en-dash + 空格）
- `<核心行为>` — 用户可感知的核心行为

**示例**：
```
[PRD-0003] 用户订阅数据模型 — schema + CRUD API + 测试
[PRD-0003] 支付流程 — 支付网关集成 + webhook 处理 + 测试
[PRD-0003] 订阅管理 UI — 查看/取消/升级 + E2E 测试
```

## Issue Body 模板

```markdown
## Meta

- **PRD**: PRD-NNNN-<title>.md
- **Type**: AFK | HITL
- **Siblings**: #<issue-2>, #<issue-3> (如有)

## Parent

#<parent-issue-number> (如存在父 Issue；独立 Issue 或删除此段)

## What to build

此垂直切片的简明描述。描述端到端行为，而不是逐层实现。

避免具体文件路径或代码片段 —— 它们很快过时。例外：如果原型生成的片段比散文更精确地编码决策（状态机、reducer、schema、类型形状），在此内联并简要说明它来自原型。修剪到决策丰富的部分 —— 不是工作演示，只是重要部分。

## Acceptance Criteria

* [ ] Criterion 1
* [ ] Criterion 2
* [ ] Criterion 3

## Blocked by

#<blocking-issue> (如有阻塞)

或 "None - can start immediately"（如无 blockers）
```

## 字段说明

| 字段 | 说明 |
|------|------|
| Meta → PRD | 所属 PRD 文件路径（PRD-NNNN-<title>.md）|
| Meta → Type | AFK（可自动完成）或 HITL（需人工交互）|
| Meta → Siblings | 同一 PRD 的其他 Child Issues（用于交叉引用）|
| Parent | 父 Issue 引用（如有）|
| What to build | 端到端行为描述 |
| Acceptance Criteria | 可测试的验收标准 |
| Blocked by | 依赖的 Issues |

## 垂直切片示例

**好（垂直切片）：**
```
Story: 用户可以订阅付费计划

What to build:
- 创建订阅时生成订阅记录
- 处理支付成功/失败
- 更新用户权限
- 发送确认邮件

Acceptance:
* [ ] 用户完成支付流程后拥有订阅
* [ ] 支付失败时显示错误
* [ ] 订阅激活后用户可访问高级功能
```

**不好（水平切片）：**
```
Story: 创建数据库表

What to build:
- subscriptions 表
- subscription_items 表

（这是水平切片，不端到端）
```

## HITL vs AFK

| 类型 | 说明 | 示例 |
|------|------|------|
| **HITL** | 需要人工交互 | UI 设计审查、架构决策 |
| **AFK** | 可自动完成 | API 开发、测试编写 |
