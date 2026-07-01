# CONTEXT Format

## 用途

领域术语表（glossary）。定义代码库中使用的核心概念和术语。

## 文件位置

项目根目录：`CONTEXT.md`

对于多上下文项目（存在 CONTEXT-MAP.md）：每个上下文的 `CONTEXT.md`

## 模板

```markdown
# Context

## Core Concepts

### <Concept Name>

<definition>

**Related terms**: <term1>, <term2>

**Anti-patterns**:
- Don't say <X> when you mean <Y>
- Avoid <ambiguous term>

## Domain Glossary

| Term | Definition | Related |
|------|------------|---------|
| <term1> | <definition> | <related-term> |
| <term2> | <definition> | <related-term> |

## Key Relationships (optional)

<diagram or description of key relationships — only fill if relationships are non-obvious and a glossary row's "Related" column isn't enough. CONTEXT.md is primarily a glossary; most context does not need this section.>
```

## 示例

```markdown
# Context

## Core Concepts

### Order

A customer's request to purchase products. An Order exists from the moment it's created until it's either fulfilled or cancelled.

**Related terms**: Customer, LineItem, Fulfillment

**Anti-patterns**:
- Don't say "cart" when you mean "Order" (a cart is transient, an Order is persisted)
- Avoid "purchase order" (ambiguous with B2B context)

### Customer

A person who has registered and can place Orders. Distinct from a User (anonymous visitor).

**Related terms**: User, Order, Account

### Materialization

The process of giving a Lesson a concrete location in the filesystem. A Lesson exists in the abstract (as course content) and is materialized (as actual files).

**Related terms**: Lesson, Course, Cascade

## Domain Glossary

| Term | Definition | Related |
|------|------------|---------|
| Order | Customer's purchase request | Customer, LineItem |
| LineItem | Single product within an Order | Order, Product |
| Fulfillment | Process of delivering an Order | Order, Shipment |
| Cancellation | Customer's request to void an Order | Order, Refund |
| Materialization | Giving a Lesson a filesystem location | Lesson, Cascade |
| Cascade | When materializing one Lesson triggers materialization of related content | Lesson, Materialization |

## Key Relationships

```
Customer --places--> Order --contains--> LineItem --references--> Product
Order --fulfilled_by--> Fulfillment --results_in--> Shipment
Course --contains--> Lesson --materialized_to--> FileLocation
Lesson --triggers--> Cascade
```
```

## 更新规则

1. **立即更新** —— 在访谈中解决术语后立即更新，不要批量
2. **无实现细节** —— CONTEXT.md 是领域术语表，不是实现文档
3. **精确术语** —— 使用精确、无歧义的术语
4. **反模式** — 记录应避免的模糊术语或错误用法
5. **关系映射** — 记录核心概念之间的关系

## 使用场景

- AI 在写代码时参考术语表，确保命名一致
- 新成员了解项目核心概念
- 讨论时有共同语言
