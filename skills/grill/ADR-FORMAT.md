# ADR Format

## 用途

架构决策记录（Architecture Decision Record）。记录重要的技术决策及其背景和后果。

## 文件位置

`docs/adr/<NNNN>-<title>.md`

编号从 0001 开始递增。

## 模板

```markdown
# <NNNN> - <Decision Title>

Date: <YYYY-MM-DD>

## Status

Accepted | Proposed | Deprecated | Superseded

## Context

<What is the issue that we're seeing that is motivating this decision or change?>

## Decision

<What is the change that we're proposing and/or doing?>

## Consequences

<What becomes easier or more difficult to do because of this change?>

### Positive

* <consequence 1>
* <consequence 2>

### Negative

* <consequence 1>
* <consequence 2>

## Alternatives Considered

* <alternative 1>
* <alternative 2>
* <alternative 3>

## References

* <link to reference 1>
* <link to reference 2>
```

## 创建条件

只在**所有三个**条件都满足时创建 ADR：

1. **难逆转** —— 改变想法的成本是有意义的
2. **没有上下文令人惊讶** —— 未来的读者会奇怪"为什么他们这样做？"
3. **真正权衡的结果** —— 有真正的替代品，你出于特定原因选择了一个

**否则，跳过 ADR。**

## 示例

```markdown
# 0001 - Event-Sourced Orders

Date: 2024-01-15

## Status

Accepted

## Context

We need to store Orders in a way that:
1. Allows us to reconstruct the state of an Order at any point in time
2. Enables us to react to Order-related events in real-time
3. Supports auditing and compliance requirements

A traditional CRUD approach would lose history and make temporal queries difficult.

## Decision

We will use Event Sourcing for Orders. Each Order will be stored as a sequence of events:
- OrderCreated
- ItemAdded
- ItemRemoved
- OrderCancelled
- OrderFulfilled

The current state of an Order is derived by replaying these events.

## Consequences

### Positive

* Complete audit trail is available
* We can reconstruct Order state at any point in time
* Easy to add new event types without changing schema
* Enables event-driven architecture (react to events in real-time)

### Negative

* More complex querying (need to replay events to get current state)
* Storage costs are higher (storing events vs current state)
* Learning curve for team unfamiliar with Event Sourcing
* Need to handle event versioning if schema changes

## Alternatives Considered

* **CRUD with audit table**: Simpler but loses event semantics, harder to query temporal state
* **Snapshot + events**: Reduces replay cost but adds complexity of snapshot management
* **Change Data Capture**: Tied to database, less flexible for event-driven architecture

## References

* [Event Sourcing by Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
```

## 状态更新

当决策被推翻或替代时：

1. 更新原 ADR 的 Status 为 "Superseded by <NNNN>"
2. 在新 ADR 中引用原 ADR

## 使用场景

- 重要的架构决策
- 技术选型
- 数据库/存储方案
- API 设计原则
- 安全相关决策
