# A 层核查：第 3 批

[返回索引](REVIEW_INDEX.md) · [标注指南](../ANNOTATION_GUIDE.md)

以下是候选线索，**不是人工结论**。摘录上限 4,000 字符，全文在本层评论 parquet 分片中；PR 链接显示的是当前 GitHub 状态。

## pair-4019169217_4108829077

[hyperlane-xyz/hyperlane-warp-ui-template PR #986](https://github.com/hyperlane-xyz/hyperlane-warp-ui-template/pull/986) 与 [PR #1020](https://github.com/hyperlane-xyz/hyperlane-warp-ui-template/pull/1020)

- 标题 A：feat: wire stableswap-only remote registry route with mc-public sdk
- 标题 B：feat: cross-collateral implementation
- 作者：nambrot / Xaroz
- 创建时间 UTC：2026-03-03 23:14:30+00:00 / 2026-03-20 16:29:38+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4099560212

类型：pr_comment；来源 PR ID：4019169217；时间：2026-03-20 16:52:59+00:00；评论者：Xaroz

<pre>closing in favor of #1020 </pre>

## pair-4026507377_4040206076

[openclaw/openclaw PR #35719](https://github.com/openclaw/openclaw/pull/35719) 与 [PR #39374](https://github.com/openclaw/openclaw/pull/39374)

- 标题 A：fix(config): accept openclaw browser profile driver
- 标题 B：fix(config): accept &quot;openclaw&quot; as browser profile driver in Zod schema
- 作者：7inspire / gambletan
- 创建时间 UTC：2026-03-05 07:51:19+00:00 / 2026-03-08 02:11:56+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4018687599

类型：pr_comment；来源 PR ID：4026507377；时间：2026-03-08 09:06:39+00:00；评论者：altaywtf

<pre>Closing — this was already fixed on `main`.

**What landed:**

- e5fdfec9 ([`fix(config): accept &quot;openclaw&quot; as browser profile driver in Zod schema`](https://github.com/openclaw/openclaw/commit/e5fdfec9dc1fee5a33775a10f47dc4ff90246737)) merged via #39374 on March 8, 2026.

**Why this PR is no longer needed:**

- This PR and #39374 both fix the same `browser.profiles.*.driver` validation bug from #35620.
- The landed fix now covers the user-visible behavior on `main`, so keeping this open would just duplicate the same schema-only change.

Thank you for the contribution, @7inspire.
</pre>

## pair-4029166508_4112489506

[aaddrick/claude-desktop-debian PR #287](https://github.com/aaddrick/claude-desktop-debian/pull/287) 与 [PR #324](https://github.com/aaddrick/claude-desktop-debian/pull/324)

- 标题 A：fix(doctor): detect virtiofsd installed outside PATH on Debian
- 标题 B：fix(doctor): detect virtiofsd outside PATH + document COWORK_VM_BACKEND
- 作者：jarrodcolburn / CyPack
- 创建时间 UTC：2026-03-05 15:59:23+00:00 / 2026-03-21 13:11:56+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4107609529

类型：pr_comment；来源 PR ID：4029166508；时间：2026-03-23 02:36:27+00:00；评论者：aaddrick

<pre>Hey! Thanks for catching this issue and putting together a fix. The virtiofsd PATH detection problem on Debian is real and your PR helped surface it clearly.

We&#x27;re going to close this in favor of #324 by CyPack, which covers the same Debian fix along with Fedora support and COWORK_VM_BACKEND documentation. It ended up being a superset of this work.

We&#x27;ll credit you in the acknowledgments when #324 merges since you identified the problem first.

---
Written by Claude Opus 4.6 via [Claude Code](https://claude.ai/code)</pre>

## pair-4029788943_4030084320

[openclaw/openclaw PR #36538](https://github.com/openclaw/openclaw/pull/36538) 与 [PR #36603](https://github.com/openclaw/openclaw/pull/36603)

- 标题 A：fix(config): use SHA256 hash for schema cache key (fixes #36508)
- 标题 B：fix(config): hash merged schema cache key to prevent RangeError with many channels
- 作者：Octane0411 / powermaster888
- 创建时间 UTC：2026-03-05 18:04:37+00:00 / 2026-03-05 19:13:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4008306257

类型：pr_comment；来源 PR ID：4029788943；时间：2026-03-05 22:48:07+00:00；评论者：Takhoffman

<pre>AI-assisted merge/triage note: this overlap path was reviewed in the same stream and superseded.\n\nThanks again for this contribution.\nThis work landed via synthesized PR #36603; attribution and co-author credit are preserved there.\nContributors are credited in changelog attribution and as co-authors on the merge commit.\nClosing this PR as superseded by #36603. If anything looks incorrect or incomplete, reply here and we will reopen and reassess.\n\nClose reason: superseded\nApproved by: Tak</pre>

## pair-4029966308_4030084320

[openclaw/openclaw PR #36580](https://github.com/openclaw/openclaw/pull/36580) 与 [PR #36603](https://github.com/openclaw/openclaw/pull/36603)

- 标题 A：gateway: hash merged schema cache key
- 标题 B：fix(config): hash merged schema cache key to prevent RangeError with many channels
- 作者：Octane0411 / powermaster888
- 创建时间 UTC：2026-03-05 18:45:40+00:00 / 2026-03-05 19:13:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4008306722

类型：pr_comment；来源 PR ID：4029966308；时间：2026-03-05 22:48:17+00:00；评论者：Takhoffman

<pre>AI-assisted merge/triage note: this overlap path was reviewed in the same stream and superseded.\n\nThanks again for this contribution.\nThis work landed via synthesized PR #36603; attribution and co-author credit are preserved there.\nContributors are credited in changelog attribution and as co-authors on the merge commit.\nClosing this PR as superseded by #36603. If anything looks incorrect or incomplete, reply here and we will reopen and reassess.\n\nClose reason: superseded\nApproved by: Tak</pre>

## pair-4034355214_4035187334

[openclaw/openclaw PR #37876](https://github.com/openclaw/openclaw/pull/37876) 与 [PR #38173](https://github.com/openclaw/openclaw/pull/38173)

- 标题 A：fix(models): use 1M context for openai-codex gpt-5.4
- 标题 B：refactor(agents): unify canonical codex model facts
- 作者：yuweuii / who96
- 创建时间 UTC：2026-03-06 13:56:29+00:00 / 2026-03-06 16:55:21+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4047084038

类型：pr_comment；来源 PR ID：4035187334；时间：2026-03-12 14:11:34+00:00；评论者：who96

<pre>Closing — the core gpt-5.4 forward-compat fixes have landed via #37876, #38736, #39753, #39902, and #40160. The remaining reasoning-default and NO_REPLY work is covered by #37940 and #38232 respectively.</pre>

## pair-4037485952_4049263237

[affaan-m/everything-claude-code PR #348](https://github.com/affaan-m/everything-claude-code/pull/348) 与 [PR #371](https://github.com/affaan-m/everything-claude-code/pull/371)

- 标题 A：fix(hooks): scrub secrets and harden hook security
- 标题 B：fix: harden hook portability and plugin docs
- 作者：jtzingsheim1 / affaan-m
- 创建时间 UTC：2026-03-07 05:43:47+00:00 / 2026-03-10 04:07:53+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4028522363

类型：pr_comment；来源 PR ID：4049263237；时间：2026-03-10 04:08:13+00:00；评论者：coderabbitai[bot]

<pre>&lt;!-- This is an auto-generated comment: summarize by coderabbit.ai --&gt;
&lt;!-- walkthrough_start --&gt;

&lt;details&gt;
&lt;summary&gt;📝 Walkthrough&lt;/summary&gt;

## Walkthrough

This PR updates hooks, shell scripts, continuous-learning tooling, tests, and documentation: it adds project-root and package-manager-aware formatter runner logic, improves dev-server command parsing to avoid heredoc false positives, makes Python invocation portable across platforms, derives plugin/script roots more robustly, clarifies agent/install docs, and expands tests.

## Changes

|Cohort / File(s)|Summary|
|---|---|
|**Formatter hook &amp; runner** &lt;br&gt; `scripts/hooks/post-edit-format.js`|Add project-root discovery via config markers; introduce runner abstraction (`getRunnerBin`, `getFormatterRunner`); make formatter command runner-aware; change `getFormatterCommand` signature to accept `projectRoot`; add `runFormatterCommand` with Windows-aware execution.|
|**Dev-server blocking hook** &lt;br&gt; `scripts/hooks/pre-bash-dev-server-block.js`|Add token parsing utilities and constants (DEV_COMMAND_WORDS, SKIPPABLE_PREFIX_WORDS, PREFIX_OPTION_VALUE_WORDS); detect leading command word and restrict dev-pattern checks to avoid heredoc/string false positives.|
|**Windows &amp; plugin-root robustness** &lt;br&gt; `scripts/hooks/run-with-flags-shell.sh`|Compute `SCRIPT_DIR` and derive `PLUGIN_ROOT` fallback; replace `CLAUDE_PLUGIN_ROOT` usages with `PLUGIN_ROOT`; guard missing SCRIPT_PATH with an early exit.|
|**Continuous-learning Python portability** &lt;br&gt; `skills/continuous-learning-v2/hooks/observe.sh`, `skills/continuous-learning-v2/scripts/detect-project.sh`, `skills/continuous-learning-v2/agents/start-observer.sh`|Add Python-command resolution (CLV2_PYTHON_CMD/CLV2 → python3/python); expose/export resolved var; conditionally run Python-dependent steps and preserve sensible defaults when Python is absent.|
|**Docs &amp; plugin assets** &lt;br&gt; `commands/e2e.md`, `commands/plan.md`, `commands/tdd.md`, `skills/iterative-retrieval/SKILL.md`, `README.md`, `.opencode/*`, `.opencode/index.ts`|Replace incorrect user-home agent path references with wording that agents/skills are provided by ECC; add manual-install path hints; clarify plugin vs repo asset behavior; add metadata feature flag `configAssets: true`.|
|**Schema** &lt;br&gt; `schemas/plugin.schema.json`|Add top-level `features` object with properties (agents, commands, skills, configAssets, hookEvents, customTools) and disallow additional properties within `features`.|
|**Tests** &lt;br&gt; `tests/hooks/hooks.test.js`|Add shimming utilities and extensive test scenarios covering formatter discovery, package-manager runner fallbacks, dev-server blocking edge cases, Python resolution, plugin-root/script resolution, and many regression/edge-case cases.|
|**Continuous-learning scripts (misc)** &lt;br&gt; `skills/continuous-learning-v2/*`|Make observer start/observe scripts robust to missing Python and use resolved interpreter when available; optional config loading via Python when present.|

## Sequence Diagram(s)

```mermaid
sequenceDiagram
    participant Hook as post-edit-format.js
    participant FR as findProjectRoot()
    participant FM as detectFormatter()
    participant GR as getFormatterRunner()
    participant PM as PackageManager
    participant Exec as FormatterExec

    Hook-&gt;&gt;FR: findProjectRoot(filePath)
    FR-&gt;&gt;FR: walk parents for PROJECT_ROOT_MARKERS
    FR--&gt;&gt;Hook: projectRoot

    Hook-&gt;&gt;FM: detectFormatter(projectRoot)
    FM--&gt;&gt;Hook: formatterType (biome / prettier)

    Hook-&gt;&gt;GR: getFormatterRunner(projectRoot)
    GR-&gt;&gt;PM: detect package manager / node_modules bin
    PM--&gt;&gt;GR: chosen runner (npx / pnpm dlx / bunx / etc.)
    GR-&gt;&gt;GR: getRunnerBin() (apply .cmd on Windows)
    GR--&gt;&gt;Hook: {bin, prefixArgs}

    Hook-&gt;&gt;Exec: construct command with bin + prefix + formatter args
    Exec--&gt;&gt;Hook: run formatter (Windows-aware exec)
```

## Estimated code review effort

🎯 4 (Complex) | ⏱️ ~60 minutes

## Possibly related PRs

- affaan-m/everyt</pre>

（摘录，原文 33,310 字符。完整内容请按 evidence_id 在评论分片中读取。）

## pair-4039293139_4088971916

[hyperlane-xyz/hyperlane-warp-ui-template PR #995](https://github.com/hyperlane-xyz/hyperlane-warp-ui-template/pull/995) 与 [PR #1014](https://github.com/hyperlane-xyz/hyperlane-warp-ui-template/pull/1014)

- 标题 A：Widgetized embed
- 标题 B：feat: embeddable iframe widget via /embed route
- 作者：nambrot / Xaroz
- 创建时间 UTC：2026-03-07 19:41:56+00:00 / 2026-03-17 14:33:36+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4120293787

类型：pr_comment；来源 PR ID：4039293139；时间：2026-03-24 17:56:13+00:00；评论者：Xaroz

<pre>closing in favor of #1014 </pre>

## pair-4039459323_4040312761

[openclaw/openclaw PR #39172](https://github.com/openclaw/openclaw/pull/39172) 与 [PR #39414](https://github.com/openclaw/openclaw/pull/39414)

- 标题 A：fix(ui): preserve Telegram sender attribution in dashboard chat
- 标题 B：fix(chat): preserve Telegram sender labels in dashboard history
- 作者：jskoiz / obviyus
- 创建时间 UTC：2026-03-07 20:51:45+00:00 / 2026-03-08 03:23:15+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4018174256

类型：pr_comment；来源 PR ID：4039459323；时间：2026-03-08 03:47:48+00:00；评论者：obviyus

<pre>Superseded by #39414.

Why:
- the root cause is upstream of the UI: sender attribution needs to survive gateway history sanitization
- this PR reparses inline metadata in the UI after that metadata has already been stripped on the real `chat.history` path
- #39414 preserves a top-level `senderLabel` in the gateway first, then keeps the UI change small: group/render from that field only
</pre>

## pair-4039563423_4039962972

[openclaw/openclaw PR #39196](https://github.com/openclaw/openclaw/pull/39196) 与 [PR #39278](https://github.com/openclaw/openclaw/pull/39278)

- 标题 A：fix(voice-call): honor vadThreshold: 0 and silenceDurationMs: 0 in STT config
- 标题 B：fix(voice-call): use nullish coalescing for STT vadThreshold and silenceDurationMs
- 作者：scoootscooob / mvanhorn
- 创建时间 UTC：2026-03-07 21:26:53+00:00 / 2026-03-08 00:13:37+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4017920482

类型：pr_comment；来源 PR ID：4039962972；时间：2026-03-08 01:42:29+00:00；评论者：mvanhorn

<pre>Closing in favor of #39196 which includes focused regression tests. Thanks @steipete for the triage.</pre>

## pair-4039569654_4039962071

[openclaw/openclaw PR #39197](https://github.com/openclaw/openclaw/pull/39197) 与 [PR #39276](https://github.com/openclaw/openclaw/pull/39276)

- 标题 A：fix(synology-chat): respect SYNOLOGY_RATE_LIMIT=0 in env var parsing
- 标题 B：fix(synology-chat): use nullish coalescing for SYNOLOGY_RATE_LIMIT=0
- 作者：scoootscooob / mvanhorn
- 创建时间 UTC：2026-03-07 21:29:00+00:00 / 2026-03-08 00:13:03+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4017920420

类型：pr_comment；来源 PR ID：4039962071；时间：2026-03-08 01:42:27+00:00；评论者：mvanhorn

<pre>Closing in favor of #39197 which has better NaN handling and test coverage. Thanks @steipete for the triage.</pre>

## pair-4041736635_4129388250

[openclaw/openclaw PR #40099](https://github.com/openclaw/openclaw/pull/40099) 与 [PR #53825](https://github.com/openclaw/openclaw/pull/53825)

- 标题 A：Fix openai-codex OAuth email profile detection
- 标题 B：fix(auth): derive OpenAI Codex OAuth profile ids from JWT claims
- 作者：MeCKodo / thePober
- 创建时间 UTC：2026-03-08 17:11:28+00:00 / 2026-03-24 17:09:40+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4125712183

类型：pr_comment；来源 PR ID：4041736635；时间：2026-03-25 11:14:19+00:00；评论者：steipete

<pre>Closing as superseded by #53825, merged on March 25, 2026. Same missing-email -&gt; openai-codex:default overwrite bug; #53825 landed the fix in the current provider-owned auth flow with contract coverage.</pre>

## pair-4041951406_4045263338

[openclaw/openclaw PR #40176](https://github.com/openclaw/openclaw/pull/40176) 与 [PR #40959](https://github.com/openclaw/openclaw/pull/40959)

- 标题 A：fix: resolve target agent workspace for cross-agent subagent spawns
- 标题 B：Fix cross-agent sessions_spawn workspace inheritance
- 作者：moshehbenavraham / kangkangzi2025
- 创建时间 UTC：2026-03-08 18:58:30+00:00 / 2026-03-09 12:17:38+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4057183359

类型：pr_comment；来源 PR ID：4045263338；时间：2026-03-13 18:30:22+00:00；评论者：mcaxtr

<pre>Thanks for the PR and for working on this. We checked the current main branch, and this bug is now fixed by #40176, which landed in commit [55e79adf6916ffed4b745744793f1502338f1b92](https://github.com/openclaw/openclaw/commit/55e79adf6916ffed4b745744793f1502338f1b92).

The landed fix now does the intended split:

- cross-agent subagent spawns use the target agent’s configured workspace
- same-agent spawns preserve inherited workspace behavior
- regression coverage was added for both paths

Because that has landed, I’m closing this PR as superseded by #40176.

Thanks again for the work here. If you think this closure is mistaken and your PR still fixes something meaningfully different on current main, feel free to reopen with that explanation.</pre>

## pair-4044879292_4058407360

[openclaw/openclaw PR #40892](https://github.com/openclaw/openclaw/pull/40892) 与 [PR #43240](https://github.com/openclaw/openclaw/pull/43240)

- 标题 A：fix(ui): preserve control-ui auth across refresh
- 标题 B：Fix session-link reload dropping Control UI token
- 作者：velvet-shark / lynnzc
- 创建时间 UTC：2026-03-09 10:56:28+00:00 / 2026-03-11 13:58:58+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4044932000

类型：pr_comment；来源 PR ID：4058407360；时间：2026-03-12 08:35:57+00:00；评论者：velvet-shark

<pre>Thanks for the careful follow-up work on this.

I reviewed it against #40892, now merged to `main` in [f2f561fab1bf3808baed61ebdd55ec3bfe3c8b65](https://github.com/openclaw/openclaw/commit/f2f561fab1bf3808baed61ebdd55ec3bfe3c8b65).

The merged fix restores current-tab Control UI token continuity through `sessionStorage`, so clicking a session link no longer loses auth even if the route change causes a same-tab reload. That resolves the underlying regression this PR is targeting, so we no longer need the separate session-link interception path to fix auth disconnects.

Closing as superseded by #40892. If we want SPA-only session-link behavior later for UX reasons independent of auth, that can come back as a narrower follow-up.
</pre>

## pair-4045720026_4048103185

[openclaw/openclaw PR #41072](https://github.com/openclaw/openclaw/pull/41072) 与 [PR #41466](https://github.com/openclaw/openclaw/pull/41466)

- 标题 A：fix(discord): preserve thread session binding
- 标题 B：ACP: fix native thread-bound session placement
- 作者：comeran / cgdusek
- 创建时间 UTC：2026-03-09 13:48:47+00:00 / 2026-03-09 21:54:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4028072389

类型：pr_comment；来源 PR ID：4045720026；时间：2026-03-10 01:56:51+00:00；评论者：comeran

<pre>Closing this in favor of #41466.

This PR fixed the original Discord existing-thread regression, but #41466 carries that same direction forward and also covers the remaining native ACP placement cases called out during review:
- Telegram current-only placement
- Discord DM current-conversation binding

To avoid duplicate review and overlapping fixes, I’m deferring to the broader follow-up in #41466.
</pre>

## pair-4045836014_4078244000

[openclaw/openclaw PR #41103](https://github.com/openclaw/openclaw/pull/41103) 与 [PR #47274](https://github.com/openclaw/openclaw/pull/47274)

- 标题 A：fix(telegram): avoid mid-word message chunking
- 标题 B：fix: preserve Telegram word boundaries when rechunking HTML
- 作者：comeran / obviyus
- 创建时间 UTC：2026-03-09 14:10:22+00:00 / 2026-03-15 12:01:43+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4149809767

类型：pr_comment；来源 PR ID：4045836014；时间：2026-03-29 09:48:09+00:00；评论者：obviyus

<pre>Closing as duplicate; this was superseded by #47274.</pre>

## pair-4046010653_4117372768

[openclaw/openclaw PR #41141](https://github.com/openclaw/openclaw/pull/41141) 与 [PR #52516](https://github.com/openclaw/openclaw/pull/52516)

- 标题 A：fix(edit): include current file contents on mismatch
- 标题 B：fix(agents): harden edit tool recovery
- 作者：wangyaok1 / mbelinky
- 创建时间 UTC：2026-03-09 14:42:12+00:00 / 2026-03-22 23:26:31+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4117798564

类型：pr_comment；来源 PR ID：4046010653；时间：2026-03-24 12:22:25+00:00；评论者：mbelinky

<pre>This has been superseded by the merged version in #52516.

Merged PR: https://github.com/openclaw/openclaw/pull/52516
Merge commit: https://github.com/openclaw/openclaw/commit/922f4e66ea1af8963ec9c16b4c116c22bc5014be

That landed slice keeps the same exact-match edit contract, but consolidates the user-visible mismatch-content improvement with the related recovery hardening that was needed to ship it safely on current `main`.

Closing as superseded by the merged implementation above.
</pre>

## pair-4058837487_4059023885

[PrefectHQ/prefect PR #21087](https://github.com/PrefectHQ/prefect/pull/21087) 与 [PR #21089](https://github.com/PrefectHQ/prefect/pull/21089)

- 标题 A：Fix: reload automations after PostgreSQL LISTEN/NOTIFY reconnect
- 标题 B：Reconcile automations when Postgres notifications are unavailable
- 作者：devin-ai-integration[bot] / zzstoatzz
- 创建时间 UTC：2026-03-11 15:12:13+00:00 / 2026-03-11 15:44:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4040433148

类型：pr_comment；来源 PR ID：4058837487；时间：2026-03-11 16:23:34+00:00；评论者：desertaxle

<pre>Closing in favor of https://github.com/PrefectHQ/prefect/pull/21089</pre>

## pair-4061962986_4075023767

[legendaryvibecoder/gigabrain PR #33](https://github.com/legendaryvibecoder/gigabrain/pull/33) 与 [PR #39](https://github.com/legendaryvibecoder/gigabrain/pull/39)

- 标题 A：fix: tighten recall routing for identity and preference prompts
- 标题 B：chore: release v0.5.3
- 作者：vibeputin / vibecodooor
- 创建时间 UTC：2026-03-12 04:01:30+00:00 / 2026-03-14 07:40:32+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4060521183

类型：pr_comment；来源 PR ID：4061962986；时间：2026-03-14 13:04:35+00:00；评论者：vibecodooor

<pre>Closing this as superseded by #39, which shipped in v0.5.3 and preserves the relevant code, tests, and attribution from this PR. Thank you again for the contribution here.</pre>

## pair-4063470773_4066836079

[nearai/ironclaw PR #1030](https://github.com/nearai/ironclaw/pull/1030) 与 [PR #1067](https://github.com/nearai/ironclaw/pull/1067)

- 标题 A：fix(safety): remove misleading sanitized attr, escape tool output content
- 标题 B：fix(safety): escape tool output XML content and remove misleading sanitized attr
- 作者：nick-stebbings / zmanian
- 创建时间 UTC：2026-03-12 09:54:20+00:00 / 2026-03-12 19:41:14+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_review:3945525362

类型：pr_review_body；来源 PR ID：4063470773；时间：2026-03-13 16:49:24+00:00；评论者：zmanian

<pre>This PR is superseded by #1067, which applies the same fix to the correct location (crates/ironclaw_safety/src/lib.rs rather than the src/safety/mod.rs shim) and includes more comprehensive test coverage (4 test cases vs 1 updated test). Per project convention, new safety code should go in the extracted ironclaw_safety crate.

Recommend closing in favor of #1067.</pre>

### 证据 pr_comment:4085078003

类型：pr_comment；来源 PR ID：4063470773；时间：2026-03-18 19:28:38+00:00；评论者：nick-stebbings

<pre>Closing — superseded by #1067 which applies the same fix to the extracted ironclaw_safety crate with more comprehensive tests.</pre>

## pair-4063944911_4079607523

[datahub-project/datahub PR #16553](https://github.com/datahub-project/datahub/pull/16553) 与 [PR #16597](https://github.com/datahub-project/datahub/pull/16597)

- 标题 A：Source category documentation
- 标题 B：feat(docs): streamline integrations page and catalog generation
- 作者：sgomezvillamor / shirshanka
- 创建时间 UTC：2026-03-12 11:21:41+00:00 / 2026-03-16 00:42:17+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4065794226

类型：pr_comment；来源 PR ID：4063944911；时间：2026-03-16 08:02:46+00:00；评论者：sgomezvillamor

<pre>superseded by https://github.com/datahub-project/datahub/pull/16597</pre>

## pair-4069259293_4077469019

[gsd-build/get-shit-done PR #1029](https://github.com/gsd-build/get-shit-done/pull/1029) 与 [PR #1051](https://github.com/gsd-build/get-shit-done/pull/1051)

- 标题 A：fix(codex): avoid duplicate [agents] header in config merge
- 标题 B：fix: remove deprecated Codex config keys causing UI instability
- 作者：medhatgalal / glittercowboy
- 创建时间 UTC：2026-03-13 06:40:48+00:00 / 2026-03-15 03:21:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4062109645

类型：pr_comment；来源 PR ID：4069259293；时间：2026-03-15 03:31:24+00:00；评论者：glittercowboy

<pre>Superseded by #1051 which removes the deprecated `[features]` section and `max_threads`/`max_depth` from Codex config entirely.</pre>

## pair-4069405399_4168307704

[nearai/ironclaw PR #1109](https://github.com/nearai/ironclaw/pull/1109) 与 [PR #1756](https://github.com/nearai/ironclaw/pull/1756)

- 标题 A：fix(routines): refresh event cache after web mutations and on ticker
- 标题 B：fix(routines): clone Arc before await in web handler event cache refresh
- 作者：G7CNF / ilblackdragon
- 创建时间 UTC：2026-03-13 07:18:36+00:00 / 2026-03-30 07:37:33+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4152911307

类型：pr_comment；来源 PR ID：4069405399；时间：2026-03-30 07:37:42+00:00；评论者：ilblackdragon

<pre>Superseded by #1756 — rebased onto staging, reduced scope to just the `.cloned()` fix + regression test per @ilblackdragon&#x27;s review.</pre>

## pair-4073290570_4091712948

[datadog-labs/pup PR #203](https://github.com/datadog-labs/pup/pull/203) 与 [PR #211](https://github.com/datadog-labs/pup/pull/211)

- 标题 A：feat(ci): add Windows build and release support
- 标题 B：feat(ci): add Windows build and release support with checksum provenance
- 作者：lucaspimentel / platinummonkey
- 创建时间 UTC：2026-03-13 20:35:03+00:00 / 2026-03-17 23:18:08+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4078951932

类型：pr_comment；来源 PR ID：4073290570；时间：2026-03-18 01:01:27+00:00；评论者：platinummonkey

<pre>pulled these into #211 and made a few fixes, thanks for doing this!</pre>

## pair-4074842525_4075023767

[legendaryvibecoder/gigabrain PR #38](https://github.com/legendaryvibecoder/gigabrain/pull/38) 与 [PR #39](https://github.com/legendaryvibecoder/gigabrain/pull/39)

- 标题 A：Fix OpenClaw install path and setup config
- 标题 B：chore: release v0.5.3
- 作者：Emphasonic / vibecodooor
- 创建时间 UTC：2026-03-14 06:20:51+00:00 / 2026-03-14 07:40:32+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4060521184

类型：pr_comment；来源 PR ID：4074842525；时间：2026-03-14 13:04:35+00:00；评论者：vibecodooor

<pre>Closing this as superseded by #39, which shipped in v0.5.3 and preserves the relevant code, tests, and attribution from this PR. Thank you again for the contribution here.</pre>

## pair-4075004266_4077302635

[gastownhall/beads PR #2587](https://github.com/gastownhall/beads/pull/2587) 与 [PR #2608](https://github.com/gastownhall/beads/pull/2608)

- 标题 A：Fix: scope backup/restore to current project prefix
- 标题 B：fix(backup): scope shared-server backup restore/export by issue prefix
- 作者：mistakeknot / garitar
- 创建时间 UTC：2026-03-14 07:31:27+00:00 / 2026-03-15 01:34:04+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4063703662

类型：pr_comment；来源 PR ID：4077302635；时间：2026-03-15 19:13:20+00:00；评论者：steveyegge

<pre>The core backup prefix scoping fix landed via #2587 (mistakeknot), and your test additions were cherry-picked on top. Both contributors attributed. Thanks for the excellent test coverage!</pre>

## pair-4076586711_4076697375

[gsd-build/gsd-2 PR #403](https://github.com/gsd-build/gsd-2/pull/403) 与 [PR #412](https://github.com/gsd-build/gsd-2/pull/412)

- 标题 A：feat(gsd): implement auto-mode fallback model rotation on network errors (refactored)
- 标题 B：feat: cross-provider fallback when rate/quota limits hit
- 作者：kassieclaire / jeremymcs
- 创建时间 UTC：2026-03-14 19:47:42+00:00 / 2026-03-14 20:46:05+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4063271119

类型：pr_comment；来源 PR ID：4076586711；时间：2026-03-15 15:53:20+00:00；评论者：glittercowboy

<pre>Closing — the core cross-provider fallback was merged in #412. The model rotation on network errors can be revisited as a follow-up if needed, but the draft has fallen behind main significantly.</pre>

## pair-4076747286_4134096162

[nodetool-ai/nodetool PR #2138](https://github.com/nodetool-ai/nodetool/pull/2138) 与 [PR #2303](https://github.com/nodetool-ai/nodetool/pull/2303)

- 标题 A：Fix high-severity npm dependency vulnerabilities in web package
- 标题 B：security: Fix multiple high-severity dependency vulnerabilities
- 作者：Copilot / claude[bot]
- 创建时间 UTC：2026-03-14 21:11:51+00:00 / 2026-03-25 09:54:39+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4132882469

类型：pr_comment；来源 PR ID：4076747286；时间：2026-03-26 09:06:58+00:00；评论者：georgi

<pre>Closing — dependency vulnerability fixes from 12 days ago are now stale (lockfiles drift quickly). Fresh security updates have been merged via #2303 and #2326. Re-run vulnerability fixes on the active branch if needed.

---
_Generated by [Claude Code](https://claude.ai/code)_</pre>

## pair-4077603512_4079387195

[gsd-build/gsd-2 PR #450](https://github.com/gsd-build/gsd-2/pull/450) 与 [PR #543](https://github.com/gsd-build/gsd-2/pull/543)

- 标题 A：Enforce research→planner separation of concerns in GSD auto-mode
- 标题 B：fix(prompts): worktree cwd, pipeline awareness, depth calibration, template improvements
- 作者：Copilot / glittercowboy
- 创建时间 UTC：2026-03-15 04:51:03+00:00 / 2026-03-15 22:55:54+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4064152584

类型：pr_comment；来源 PR ID：4077603512；时间：2026-03-15 23:21:59+00:00；评论者：glittercowboy

<pre>Closing — superseded by #543 (merged), which added pipeline awareness with role sections to all prompts (researchers write for planners, planners trust research, executors build from plans). #543&#x27;s approach is more comprehensive and covers the same separation of concerns this PR targeted.</pre>

## pair-4078288449_4101350312

[sqlfluff/sqlfluff PR #7615](https://github.com/sqlfluff/sqlfluff/pull/7615) 与 [PR #7644](https://github.com/sqlfluff/sqlfluff/pull/7644)

- 标题 A：Fix placeholder colon param incorrectly prefixed with table alias when followed by `::` cast
- 标题 B：Fix RF03 incorrectly qualifying placeholder parameters
- 作者：Copilot / shauneccles
- 创建时间 UTC：2026-03-15 12:31:18+00:00 / 2026-03-19 12:25:20+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4093508426

类型：pr_comment；来源 PR ID：4101350312；时间：2026-03-19 21:48:27+00:00；评论者：shauneccles

<pre>Apologies — I missed that PR #7615 already addresses this issue. I looked for existing PRs but it was late and I overlooked it. Closing in favour of #7615 which has a more complete fix (regex + RF03).

Sorry for the noise!</pre>

## pair-4079317988_4079341741

[gsd-build/gsd-2 PR #533](https://github.com/gsd-build/gsd-2/pull/533) 与 [PR #536](https://github.com/gsd-build/gsd-2/pull/536)

- 标题 A：Restore `git.isolation` for auto-mode and keep worktrees as the default
- 标题 B：fix: prevent merge loop, auto-resolve .gsd/ conflicts, restore git.isolation (#530, #531)
- 作者：Copilot / jeremymcs
- 创建时间 UTC：2026-03-15 22:18:39+00:00 / 2026-03-15 22:32:11+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4064172882

类型：pr_comment；来源 PR ID：4079317988；时间：2026-03-15 23:32:16+00:00；评论者：glittercowboy

<pre>Superseded by #536 which restored git.isolation as an active setting (plus merge loop and .gsd/ conflict fixes). Already merged.</pre>

## pair-4086678514_4089819321

[openclaw/openclaw PR #48812](https://github.com/openclaw/openclaw/pull/48812) 与 [PR #49148](https://github.com/openclaw/openclaw/pull/49148)

- 标题 A：fix(telegram): fallback to alternative API IP when DNS-resolved endpoint is unreachable
- 标题 B：fix(telegram): unify transport fallback chain
- 作者：Cypherm / obviyus
- 创建时间 UTC：2026-03-17 07:15:42+00:00 / 2026-03-17 16:52:00+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4076458694

类型：pr_comment；来源 PR ID：4086678514；时间：2026-03-17 16:52:10+00:00；评论者：obviyus

<pre>Superseded by #49148.

I kept the same fallback goal, but rewrote it as one ordered transport retry chain shared by normal Telegram API calls and media downloads, instead of adding another special-case branch inside `resolveTelegramTransport()`.
</pre>

### 证据 pr_comment:4149809360

类型：pr_comment；来源 PR ID：4086678514；时间：2026-03-29 09:47:50+00:00；评论者：obviyus

<pre>Closing as duplicate; this was superseded by #49148.</pre>

## pair-4090325787_4090340396

[airbytehq/airbyte PR #75141](https://github.com/airbytehq/airbyte/pull/75141) 与 [PR #75143](https://github.com/airbytehq/airbyte/pull/75143)

- 标题 A：fix(source-amazon-seller-partner): correct URL path for settlement report fetching
- 标题 B：fix(source-amazon-seller-partner): fix incorrect URL path for GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE (AI-Triage PR)
- 作者：ald-ahmed / devin-ai-integration[bot]
- 创建时间 UTC：2026-03-17 18:17:01+00:00 / 2026-03-17 18:20:25+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4081849764

类型：pr_comment；来源 PR ID：4090340396；时间：2026-03-18 11:42:57+00:00；评论者：devin-ai-integration[bot]

<pre>↪️ Triggering `/ai-prove-fix` per [Hands-Free AI Triage Project](https://airbytehq-team.slack.com/archives/C0A30PKB8HK) triage next step.

Reason: Draft PR with CI fully green (503/503 tests pass). One-line manifest fix for missing `/reports/` path segment causing 403 on all settlement report syncs.

Note: Duplicate community PR exists at https://github.com/airbytehq/airbyte/pull/75141 with the same fix. This PR (airbytehq/airbyte#75143) was selected as the primary candidate since it has cleaner CI and was created from the AI triage workflow.

https://github.com/airbytehq/oncall/issues/11682

[Devin session](https://app.devin.ai/sessions/1c0fd20401af49f2b8b8a3f4983ec060)
</pre>

## pair-4093644800_4100668106

[foxglove/mcap PR #1603](https://github.com/foxglove/mcap/pull/1603) 与 [PR #1605](https://github.com/foxglove/mcap/pull/1605)

- 标题 A：Restrict strict-message-order to doctor
- 标题 B：Move strict-message-order to doctor only
- 作者：vvezre / james-rms
- 创建时间 UTC：2026-03-18 08:44:07+00:00 / 2026-03-19 10:10:14+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4107484029

类型：pr_comment；来源 PR ID：4093644800；时间：2026-03-23 01:43:30+00:00；评论者：james-rms

<pre>Fixed in https://github.com/foxglove/mcap/pull/1605</pre>

## pair-4103073293_4105234265

[milady-ai/milady PR #1139](https://github.com/milady-ai/milady/pull/1139) 与 [PR #1154](https://github.com/milady-ai/milady/pull/1154)

- 标题 A：chore: make env-prefixed scripts cross-platform on develop
- 标题 B：release: integrate green hardening for develop
- 作者：dutchiono / Dexploarer
- 创建时间 UTC：2026-03-19 17:13:35+00:00 / 2026-03-20 02:02:55+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4094881252

类型：pr_comment；来源 PR ID：4103073293；时间：2026-03-20 02:03:19+00:00；评论者：Dexploarer

<pre>Superseded by #1154. The develop-safe changes from this PR were absorbed/adapted onto codex/release-green-integration at 324b0801 and revalidated with bun run check, bun run build, bun run pre-review:local, and bun run test.</pre>

## pair-4104800869_4105234265

[milady-ai/milady PR #1151](https://github.com/milady-ai/milady/pull/1151) 与 [PR #1154](https://github.com/milady-ai/milady/pull/1154)

- 标题 A：Codex/develop forwardport
- 标题 B：release: integrate green hardening for develop
- 作者：dutchiono / Dexploarer
- 创建时间 UTC：2026-03-19 23:35:18+00:00 / 2026-03-20 02:02:55+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4094881129

类型：pr_comment；来源 PR ID：4104800869；时间：2026-03-20 02:03:17+00:00；评论者：Dexploarer

<pre>Superseded by #1154. The develop-safe changes from this PR were absorbed/adapted onto codex/release-green-integration at 324b0801 and revalidated with bun run check, bun run build, bun run pre-review:local, and bun run test.</pre>

## pair-4111054003_4124203474

[openclaw/openclaw PR #51381](https://github.com/openclaw/openclaw/pull/51381) 与 [PR #53220](https://github.com/openclaw/openclaw/pull/53220)

- 标题 A：fix(ui): prevent double-qualifying already-qualified model values
- 标题 B：fix(ui): resolve model provider from catalog instead of stale session default
- 作者：Cypherm / hclsys
- 创建时间 UTC：2026-03-21 02:30:56+00:00 / 2026-03-23 23:05:36+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4119237386

类型：pr_comment；来源 PR ID：4111054003；时间：2026-03-24 15:34:11+00:00；评论者：Cypherm

<pre>Closing as superseded by #53220, which fixes all three external callers of `resolveServerChatModelValue()` with catalog-first resolution. The remaining internal caller (`resolvePreferredServerChatModel`) only reaches the fallback when the model name has no `/`, so the `startsWith` guard from this PR would never trigger. Thanks @steipete for the fix!</pre>

## pair-4116914762_4117684848

[aaddrick/claude-desktop-debian PR #333](https://github.com/aaddrick/claude-desktop-debian/pull/333) 与 [PR #336](https://github.com/aaddrick/claude-desktop-debian/pull/336)

- 标题 A：fix: force layout recalculation on tiling WM workspace switches
- 标题 B：fix: debounced jiggle for same-size tiling WM workspace switches
- 作者：lukedev45 / aaddrick
- 创建时间 UTC：2026-03-22 19:36:46+00:00 / 2026-03-23 01:47:34+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4107499524

类型：pr_comment；来源 PR ID：4116914762；时间：2026-03-23 01:50:23+00:00；评论者：aaddrick

<pre>Hey Luke! Thanks for putting this together. Your diagnosis was spot-on — PR #331&#x27;s resize handler alone doesn&#x27;t cover the case where Hyprland fires blur/focus instead of resize on same-size workspace switches. Your video on #331 confirmed the gap and saved us a lot of guesswork.

We went ahead and merged #336 as an alternative implementation. It uses the same armed-pair concept from your PR (blur→focus, hide→show) but adds some guardrails for stacking WMs:

1. Debounce on the jiggle (100ms) to avoid stacking timer callbacks
2. A `jiggling` flag that suppresses the cascade from setSize&#x27;s own resize events
3. A `will-resize` guard so it doesn&#x27;t fire during interactive drag
4. Only jiggles when `fixChildBounds()` finds no actual bounds mismatch

The core idea of detecting the blur→focus transition and forcing a recalculation came from your work here. I appreciate you digging into this.

One ask — we don&#x27;t have Hyprland hardware to test on. If you get a chance, try building from main and let us know if #323 is fully resolved on your setup. That would be really helpful.

Closing this in favor of #336. Thanks again for the contribution.

---
Written by Claude Opus 4.6 via [Claude Code](https://claude.ai/code)</pre>

## pair-4119248766_4125150124

[tninja/ai-code-interface.el PR #260](https://github.com/tninja/ai-code-interface.el/pull/260) 与 [PR #262](https://github.com/tninja/ai-code-interface.el/pull/262)

- 标题 A：[codex] fix selected byte-compile warnings
- 标题 B：Raise Emacs floor to 29.1 and document byte-compile/checkdoc expectations
- 作者：Silex / Copilot
- 创建时间 UTC：2026-03-23 08:47:52+00:00 / 2026-03-24 04:22:21+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4115385665

类型：pr_comment；来源 PR ID：4119248766；时间：2026-03-24 04:52:23+00:00；评论者：tninja

<pre>&gt; ```
&gt; The failing job 68149760321 is caused by missing or incorrect Emacs version dependencies in your package files.
&gt; Multiple errors such as “You should depend on (emacs &quot;29.1&quot;) if you need ...” are reported for functions and 
&gt; modes only available in Emacs 29.1 and later.
&gt; 
&gt; Update the Package-Requires header in your main Emacs Lisp package file (likely ai-code.el) to 
&gt; require Emacs 29.1 or higher.
&gt; ```

addressed at https://github.com/tninja/ai-code-interface.el/pull/262/changes</pre>

## pair-4123539314_4128487439

[gastownhall/gastown PR #3205](https://github.com/gastownhall/gastown/pull/3205) 与 [PR #3230](https://github.com/gastownhall/gastown/pull/3230)

- 标题 A：feat: add push_strategy config — fork push + GitHub PR workflow (gas-ddg)
- 标题 B：feat: pluggable PushStrategy interface for gt done submission path
- 作者：outdoorsea / quad341
- 创建时间 UTC：2026-03-23 20:30:21+00:00 / 2026-03-24 14:47:12+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:4118893579

类型：pr_comment；来源 PR ID：4123539314；时间：2026-03-24 14:47:23+00:00；评论者：quad341

<pre>Thanks for this — the fork push workflow is a real need. However, this will likely be superseded by #3230 which implements the pluggable `PushStrategy` interface that Steve requested in #3152.

The architecture in #3230:
- `PushStrategy` interface with `Push()` and `Submit()` methods
- Per-rig configuration (not town-wide)
- `ForkPushStrategy` as one implementation, `DefaultPushStrategy` (MR beads) as another
- Tap guard integration at the strategy level

The fork workflow logic you&#x27;ve written here is very similar to what ends up in `ForkPushStrategy` — so the work isn&#x27;t wasted, it&#x27;s just wrapped in an interface.

See Steve&#x27;s feedback on #3152 for the full rationale.</pre>

### 证据 pr_comment:4120146130

类型：pr_comment；来源 PR ID：4123539314；时间：2026-03-24 17:39:55+00:00；评论者：outdoorsea

<pre>Closing — superseded by #3230 which implements the pluggable PushStrategy interface. Thanks for the pointer!</pre>

