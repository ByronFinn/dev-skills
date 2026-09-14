# 共享规则目录在安装副本中不可见（`skills/rules/`）

> **日期**: 2026-09-14 · **发现于**: `/review`（工程原则目录落地时的分发评估，Impact Review 提出，orchestrator 复核） · **性质**: **既有产品级缺陷**，非本次改动引入

## 现象

1. 运行中的 agent 从 `~/.agents/skills/` 加载技能：19 个技能目录，**没有 `rules/` 目录**，也没有任何其他非技能目录。
2. 该副本与 `origin/main`（`84d21101`）**逐字一致** —— 校验方式：`git show HEAD:skills/<s>/SKILL.md | shasum` 与 `shasum ~/.agents/skills/<s>/SKILL.md` 对比，`review` / `tdd` / `improve-architecture` / `implement` 四个 SKILL.md 全部相同。（此前的"已安装版本与仓库不同"结论是拿工作区改动比对造成的测量错误，已更正。）
3. 但安装副本内有 **22 处** `../rules/*.md` 引用：`anti-patterns.md`、`entry-protocol.md`、`sub-agent-runtime.md`、`writing-skills.md`，以及新增的 `engineering-principles.md`。

## 根因（安装器源码证据）

`skills@1.5.22`（`~/.npm/_npx/9c23c80e9d788249/node_modules/skills/dist/cli.mjs`）：

- **技能发现只认含 `SKILL.md` 的目录**：`hasSkillMd(dir)` 读取 `join(dir, "SKILL.md")`；批量发现处的条件是 `isContainer && parts.length >= 3 && parts.length <= 4 && parts.at(-1).toLowerCase() === "skill.md"`。
- **安装动作复制技能目录自身**：`await copySkillDirectory(skill.path, skillDir)`。

因此 `skills/rules/` 这类非技能目录**既不被发现、也不被复制**；而技能目录内部的子目录（例如 `skills/write/references/`）会随技能一起安装 —— 这也是本仓库按技能分目录的语言目录能正常工作的原因。

## 影响

- 安装副本中**所有跨技能共享规则链接悬空**：agent 按 `../rules/anti-patterns.md` 去读会失败。
- 受影响面：4 条共享规则文件 + 22 处引用；本次工程原则改动把依赖该路径的消费方从 2 类扩到 3 类（`review` / `improve-architecture` / `tdd` / `implement`）。
- **仓库内一切正常**（contributor 场景、本仓 dogfood、`scripts/check-docs.py` 全部通过），所以该缺陷在开发期不可见，只在安装后暴露。这也是它长期未被发现的原因。

## 决策：方案 A —— 让 `rules/` 成为可安装单元

**2026-09-14 决定并落地**：在 `skills/rules/SKILL.md` 放一个包清单（`disable-model-invocation: true`），使该目录成为安装器认可的"技能目录"，从而与其余技能一起被复制。

**推理（第一性原理）**：需求是「安装后的 agent 能读到共享规则」＋「仓库内只保留一份（#38）」＋「相对链接在两处都成立」。约束是「平台唯一的打包单位 = 含 `SKILL.md` 的目录」，且 CLI 不提供任何"随附额外文件"的机制（已验证：`.claude-plugin/marketplace.json` 只影响**发现**根路径，不影响复制内容）。因此让逻辑单位适配打包单位是唯一同时满足三者的解：**新增 1 个文件、零内容复制、零链接改写**，且仓库内与安装后的布局同构（两边都是 `skills/<unit>/...`，同一套 `../rules/*` 相对链接均成立）。

**实测证据**（真实安装器 `skills@1.5.22`，`--project --copy`，隔离临时目录与临时 HOME，未触碰任何真实 `~/.agents`）：

| | 修复前（HEAD） | 修复后（含 `rules/SKILL.md`） |
|---|---|---|
| CLI `--list` 发现数 | 12（无 `rules`） | **13（含 `rules`）** |
| 安装副本 `rules/` | **不存在** | 存在，规则文件齐备 |
| 已安装 `review/SKILL.md` 内 `../rules/*` | 0 可解析 / **3 悬空** | **3 可解析 / 0 悬空** |

**未采用的方案与代价**：

| 方案 | 为何不选 |
|---|---|
| B. 承认 `rules/` 仅仓库内可见 | 用户侧 12 个技能将失去全部共享规则（反模式、入口协议、子代理运行时、编写规范、工程原则），或迫使把规则复制进各技能——正是 #38 与本次 review 认定要消灭的漂移源 |
| C/D. 发布时内联/生成（build step） | 需要新增构建步骤与产物一致性维护；本仓的设计前提是"无构建、Markdown 即产品"（AGENTS.md） |
| 把链接改指向某个既有技能目录 | 任意指定宿主技能，语义更差，且让该技能被动承担共享库职责 |
| 依赖 CLI 的清单机制 | 不存在该机制（已验证源码），非可选路径 |

**代价与缓解**：安装集从 12 个单元变为 13 个（README/RESOLVER/evals 已同步说明它是 bundle 而非任务技能）；`disable-model-invocation` 保证零上下文占用、不参与路由竞争，因此**不需要 trigger-eval round**（已在 `docs/evals/trigger-eval.md` 记录理由）。

## 未验证的缺口

- 未确认 `~/.agents/skills/` 是否确为 `npx skills add ByronFinn/dev-skills` 的安装目标（依据是其中 dev-skills 技能名与本仓完全一致）——但本方案的实测是在等价的安装路径上完成的，不受此影响。
- 未在干净机器上跑完整安装流程（HTTP 拉取路径未测；`file://` 克隆路径已测）。
- 实测使用 `--project` 作用域与 `--copy`；全局作用域与符号链接模式未单独实测。
- `scripts/check-docs.py` 只能验证**仓库内**链接可解析，无法发现安装期缺失；本方案的效果只能由安装器实测证明（已在上面给出）。
- 一个附带事实：CLI 从 **git** 克隆源仓库，因此**未提交的文件不会随安装发布**——`rules/` 新增文件必须提交后才对用户生效。

## 复核条件

- 若 `skills` CLI 后续版本支持"随附目录/文件"清单或非技能目录分发，应改用它并移除 `rules/SKILL.md` 这一适配层（该文件届时只承担索引职责）。
- 若安装集单元数成为用户侧困扰（出现"`rules` 是什么"的疑问），考虑在 description 中进一步强化"not a task skill"表述，而不是删除该文件（删除即回退到本缺陷）。
