# A 层核查：第 2 批

[返回索引](REVIEW_INDEX.md) · [标注指南](../ANNOTATION_GUIDE.md)

以下是候选线索，**不是人工结论**。摘录上限 4,000 字符，全文在本层评论 parquet 分片中；PR 链接显示的是当前 GitHub 状态。

## pair-3896029522_3898964305

[openclaw/openclaw PR #8780](https://github.com/openclaw/openclaw/pull/8780) 与 [PR #9182](https://github.com/openclaw/openclaw/pull/9182)

- 标题 A：Security: enforce sandbox for media param [AI-assisted]
- 标题 B：Security: harden sandboxed media handling
- 作者：victormier / gumadeiras
- 创建时间 UTC：2026-02-04 11:20:43+00:00 / 2026-02-05 00:07:40+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3850433503

类型：pr_comment；来源 PR ID：3896029522；时间：2026-02-05 00:35:05+00:00；评论者：gumadeiras

<pre>Closing in favor of #9182 since the fork branch is not writable.

The fix is merged on main via the replacement PR.</pre>

## pair-3907539357_3914032536

[openclaw/openclaw PR #10536](https://github.com/openclaw/openclaw/pull/10536) 与 [PR #12229](https://github.com/openclaw/openclaw/pull/12229)

- 标题 A：fix: update DEFAULT_CONTEXT_TOKENS to 1M for Opus 4.6
- 标题 B：fix: update DEFAULT_CONTEXT_TOKENS from 200K to 1M for Opus 4.6
- 作者：jbold / Yida-Dev
- 创建时间 UTC：2026-02-06 16:36:24+00:00 / 2026-02-09 01:35:42+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3869394948

类型：pr_comment；来源 PR ID：3914032536；时间：2026-02-09 05:22:32+00:00；评论者：Yida-Dev

<pre>Closing as duplicate of #10536 and others. Sorry for the noise.</pre>

## pair-3908134994_3985379801

[apache/spark PR #54184](https://github.com/apache/spark/pull/54184) 与 [PR #54453](https://github.com/apache/spark/pull/54453)

- 标题 A：[SPARK-46168][PS] Implementation of idxmin Axis argument 
- 标题 B：[SPARK-46168][PS] Implementation of idxmin Axis argument
- 作者：devin-petersohn / sfc-gh-dpetersohn
- 创建时间 UTC：2026-02-06 19:28:03+00:00 / 2026-02-24 19:10:24+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3954187204

类型：pr_comment；来源 PR ID：3908134994；时间：2026-02-24 19:11:10+00:00；评论者：sfc-gh-dpetersohn

<pre>Closing in favor of #54453</pre>

## pair-3908195023_3913251948

[supabase/supabase-py PR #1380](https://github.com/supabase/supabase-py/pull/1380) 与 [PR #1381](https://github.com/supabase/supabase-py/pull/1381)

- 标题 A：fix(storage3): replace print() with warnings.warn() for trailing slash notice
- 标题 B：fix(storage3): replace trailing-slash print notice with warning
- 作者：bishnubista / Dodothereal
- 创建时间 UTC：2026-02-06 19:47:45+00:00 / 2026-02-08 18:20:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3868004441

类型：pr_comment；来源 PR ID：3913251948；时间：2026-02-08 19:08:25+00:00；评论者：Dodothereal

<pre>Closing as duplicate of #1380 to avoid duplicate effort and keep review load focused.</pre>

## pair-3912131783_3914148882

[huggingface/transformers PR #43831](https://github.com/huggingface/transformers/pull/43831) 与 [PR #43850](https://github.com/huggingface/transformers/pull/43850)

- 标题 A：[docs] Remove pipeline() examples from summarization/translation tasks
- 标题 B：Remove stale pipeline inference examples from v5 task docs
- 作者：Mr-Neutr0n / weiguangli-io
- 创建时间 UTC：2026-02-08 06:39:23+00:00 / 2026-02-09 02:34:44+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3871407728

类型：pr_comment；来源 PR ID：3914148882；时间：2026-02-09 12:24:03+00:00；评论者：Rocketknight1

<pre>There was a PR open for this already at #43831!</pre>

## pair-3914026734_3918934929

[openclaw/openclaw PR #12226](https://github.com/openclaw/openclaw/pull/12226) 与 [PR #12988](https://github.com/openclaw/openclaw/pull/12988)

- 标题 A：fix: remove billing error false-positive from sanitizeUserFacingText
- 标题 B：Agents: scope sanitizeUserFacingText rewrites to errorContext
- 作者：Yida-Dev / Takhoffman
- 创建时间 UTC：2026-02-09 01:32:55+00:00 / 2026-02-10 01:16:18+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3874871661

类型：pr_comment；来源 PR ID：3914026734；时间：2026-02-10 01:53:14+00:00；评论者：Takhoffman

<pre>Fixed in #12988.

This will go out in the next OpenClaw release.

If you still see this after updating to the first release that includes #12988, please open a new issue with:
- your OpenClaw version
- channel (Telegram/Slack/etc)
- the exact prompt/response that got rewritten
- whether Web UI showed the full text vs the channel being rewritten
- relevant logs around send/normalize (if available)

Link back here for context.
</pre>

## pair-3914206460_3914224140

[php/php-src PR #21174](https://github.com/php/php-src/pull/21174) 与 [PR #21175](https://github.com/php/php-src/pull/21175)

- 标题 A：Optimize hash_pbkdf2() by reusing HMAC contexts
- 标题 B：Optimize hash_pbkdf2() by reusing HMAC contexts
- 作者：gregPDN / gregharmon
- 创建时间 UTC：2026-02-09 03:04:20+00:00 / 2026-02-09 03:12:45+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3869051521

类型：pr_comment；来源 PR ID：3914206460；时间：2026-02-09 03:12:54+00:00；评论者：gregharmon

<pre>Superseded by #21175 (same patchset from the correct account). Please review #21175.</pre>

### 证据 pr_comment:3869052214

类型：pr_comment；来源 PR ID：3914206460；时间：2026-02-09 03:13:14+00:00；评论者：gregharmon

<pre>Superseded by #21175 (opened from my main account). Please ignore this one and review #21175.</pre>

## pair-3914781453_3919484350

[erigontech/erigon PR #19037](https://github.com/erigontech/erigon/pull/19037) 与 [PR #19064](https://github.com/erigontech/erigon/pull/19064)

- 标题 A：ci: tolerate consensus spec test download failure
- 标题 B：ci: Add path filtering to workflows and clarify RPC test failures
- 作者：anacrolix / Copilot
- 创建时间 UTC：2026-02-09 06:53:17+00:00 / 2026-02-10 05:10:30+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3876522358

类型：pr_comment；来源 PR ID：3919484350；时间：2026-02-10 09:47:09+00:00；评论者：Copilot

<pre>
&gt; @copilot rebase on to main. can you use a path-ignore field common to both push and pull request?
&gt; 
&gt; why ignore .github/workflows/backups-dashboards.yml. how did you determine the list of things to ig...

Done in 33a9ed8. 

**Rebase on main**: The base branch `anacrolix/ci-tolerate-spec-download-failure` was already merged to main as PR #19037, so rebasing would create conflicts with commits already in main. Keeping the current branch structure.

**Common path field**: GitHub Actions doesn&#x27;t support YAML anchors/aliases for the `on` section, so paths must be repeated. Both push and pull_request now use the same paths list.

**Improved test-kurtosis-assertoor.yml**: Switched from `paths-ignore` to explicit `paths` allowlist. Now only runs when:
- Go source files (`**/*.go`)
- Build dependencies (`go.mod`, `go.sum`, `Makefile`, `Dockerfile`)
- Kurtosis configs (`.github/workflows/kurtosis/**`)
- The workflow itself

**Why backups-dashboards.yml was ignored**: It was copied from test-all-erigon.yml pattern. The explicit `paths` approach is better and more maintainable.</pre>

## pair-3928863324_3929450045

[jobovy/galpy PR #827](https://github.com/jobovy/galpy/pull/827) 与 [PR #828](https://github.com/jobovy/galpy/pull/828)

- 标题 A：Simplify and document SCFPotential.c for spherical harmonics abstraction
- 标题 B：Simplify SCFPotential.c for spherical harmonics abstraction
- 作者：Copilot / jobovy
- 创建时间 UTC：2026-02-11 21:58:38+00:00 / 2026-02-12 01:52:10+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3893587809

类型：pr_comment；来源 PR ID：3928863324；时间：2026-02-12 21:50:23+00:00；评论者：jobovy

<pre>Closing because superseded by #828 </pre>

## pair-3939928777_3988036418

[lightonai/next-plaid PR #11](https://github.com/lightonai/next-plaid/pull/11) 与 [PR #24](https://github.com/lightonai/next-plaid/pull/24)

- 标题 A：Stack Overflow Recursion Guard
- 标题 B：fix: stack overflow recursion guard for AST parsing
- 作者：artemdinaburg / raphaelsty
- 创建时间 UTC：2026-02-14 00:44:45+00:00 / 2026-02-25 08:44:26+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3957703769

类型：pr_comment；来源 PR ID：3939928777；时间：2026-02-25 08:44:35+00:00；评论者：raphaelsty

<pre>Hey @artemdinaburg, thank you for this contribution! The recursion guard is an important fix — stack overflows on pathological files like LLVM sources were a real problem, and making the depth configurable is a nice touch.

I&#x27;ve incorporated your work into #24 with a small follow-up commit to fix the rustfmt formatting issues that were causing CI failures. Your authorship is preserved in the git history.

Closing this in favor of #24. Thanks again! 🙏</pre>

## pair-3941583815_3948088837

[jhlee0409/claude-code-history-viewer PR #130](https://github.com/jhlee0409/claude-code-history-viewer/pull/130) 与 [PR #135](https://github.com/jhlee0409/claude-code-history-viewer/pull/135)

- 标题 A：feat: add Homebrew cask support for macOS installation
- 标题 B：fix: address security and error handling issues in Homebrew workflow
- 作者：jhlee0409 / Copilot
- 创建时间 UTC：2026-02-14 14:59:54+00:00 / 2026-02-16 14:39:12+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3909813604

类型：pr_comment；来源 PR ID：3948088837；时间：2026-02-16 17:57:36+00:00；评论者：jhlee0409

<pre>Closing: these fixes were already applied directly in PR #130 (commit 155182d). The same code review feedback from CodeRabbit and Copilot has been addressed.</pre>

## pair-3942174121_3961781641

[git-ai-project/git-ai PR #528](https://github.com/git-ai-project/git-ai/pull/528) 与 [PR #564](https://github.com/git-ai-project/git-ai/pull/564)

- 标题 A：Add comprehensive worktree support across wrapper/corehooks/both
- 标题 B：Add core hooks support and worktree coverage
- 作者：svarlamov / jwiegley
- 创建时间 UTC：2026-02-14 19:59:30+00:00 / 2026-02-19 09:10:51+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3929478064

类型：pr_comment；来源 PR ID：3961781641；时间：2026-02-19 19:33:56+00:00；评论者：jw-pos

<pre>This PR was incorrectly based directly on `main` instead of on PR #530 (`codex/global-hooks-dual-mode`). The worktree changes have been cherry-picked onto the correct base branch. Please close this PR in favor of PR #528 which targets the proper branch.</pre>

## pair-3942432982_3943796277

[shakacode/shakapacker PR #891](https://github.com/shakacode/shakapacker/pull/891) 与 [PR #917](https://github.com/shakacode/shakapacker/pull/917)

- 标题 A：fix: add privateOutputPath computed property to JS config
- 标题 B：Supersede #902: privateOutputPath export with lint unblock
- 作者：ihabadham / justin808
- 创建时间 UTC：2026-02-14 21:55:11+00:00 / 2026-02-15 10:57:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3905232878

类型：pr_comment；来源 PR ID：3943796277；时间：2026-02-15 21:40:25+00:00；评论者：justin808

<pre>Closing in favor of #891, which now contains the same privateOutputPath changes plus one follow-up commit for lint unblock.</pre>

## pair-3950289529_3978986396

[gsd-build/get-shit-done PR #624](https://github.com/gsd-build/get-shit-done/pull/624) 与 [PR #720](https://github.com/gsd-build/get-shit-done/pull/720)

- 标题 A：Fix phase complete crash on nested decimal phases
- 标题 B：fix: handle multi-level decimal phases and escape regex in phase operations
- 作者：Solvely-Colin / glittercowboy
- 创建时间 UTC：2026-02-17 01:37:01+00:00 / 2026-02-23 16:12:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3945747528

类型：pr_comment；来源 PR ID：3950289529；时间：2026-02-23 16:13:00+00:00；评论者：glittercowboy

<pre>Superseded by #720 which applies this fix to the refactored modular codebase. The original PR targeted the pre-split monolithic gsd-tools.cjs and could not be cleanly merged after the lib/ refactor.</pre>

## pair-3952900646_3978902277

[gsd-build/get-shit-done PR #631](https://github.com/gsd-build/get-shit-done/pull/631) 与 [PR #716](https://github.com/gsd-build/get-shit-done/pull/716)

- 标题 A：Fix summary-extract requirements_completed mapping
- 标题 B：fix: map requirements-completed frontmatter in summary-extract
- 作者：Solvely-Colin / glittercowboy
- 创建时间 UTC：2026-02-17 13:56:46+00:00 / 2026-02-23 15:54:57+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3945645529

类型：pr_comment；来源 PR ID：3952900646；时间：2026-02-23 15:55:04+00:00；评论者：glittercowboy

<pre>Closing in favor of #716 which re-applies this fix against the refactored codebase (gsd-tools.cjs → lib/commands.cjs, tests split into tests/commands.test.cjs). Thanks @Solvely-Colin for the original fix — credited in the replacement PR.</pre>

## pair-3953730266_3959828804

[Lightning-AI/litgpt PR #2203](https://github.com/Lightning-AI/litgpt/pull/2203) 与 [PR #2204](https://github.com/Lightning-AI/litgpt/pull/2204)

- 标题 A：fix: default val_split_fraction to 0.05 for single-file JSON data
- 标题 B：fix: default val_split_fraction to 0.05 for single-file JSON data
- 作者：fumadari / dario-fumarola
- 创建时间 UTC：2026-02-17 16:54:25+00:00 / 2026-02-18 21:14:58+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3923265103

类型：pr_comment；来源 PR ID：3953730266；时间：2026-02-18 21:15:38+00:00；评论者：dario-fumarola

<pre>Superseded by https://github.com/Lightning-AI/litgpt/pull/2204</pre>

### 证据 pr_comment:3923281547

类型：pr_comment；来源 PR ID：3953730266；时间：2026-02-18 21:19:37+00:00；评论者：fumadari

<pre>Superseded by https://github.com/Lightning-AI/litgpt/pull/2204</pre>

## pair-3972971372_3983627591

[zeroclaw-labs/zeroclaw PR #1317](https://github.com/zeroclaw-labs/zeroclaw/pull/1317) 与 [PR #1637](https://github.com/zeroclaw-labs/zeroclaw/pull/1637)

- 标题 A：feat(onboard): add interactive tool enablement prompts and wildcard allowlists
- 标题 B：[supersede #1317] feat(onboard): add interactive tool enablement prompts and wildcard allowlists
- 作者：ttulttul / chumyin
- 创建时间 UTC：2026-02-21 22:35:20+00:00 / 2026-02-24 13:04:32+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3951647693

类型：pr_comment；来源 PR ID：3972971372；时间：2026-02-24 13:04:34+00:00；评论者：chumyin

<pre>Superseded by #1637 for conflict-free replay on top of latest dev. Continuing with the same CI-green merge policy.</pre>

## pair-3975024594_3975818772

[shakacode/react_on_rails PR #2476](https://github.com/shakacode/react_on_rails/pull/2476) 与 [PR #2478](https://github.com/shakacode/react_on_rails/pull/2478)

- 标题 A：Fix RSC WebpackLoader not added when using SWC transpiler
- 标题 B：Fix doctor false positives and stabilize default RSC starter
- 作者：AbanoubGhadban / justin808
- 创建时间 UTC：2026-02-22 17:02:10+00:00 / 2026-02-23 00:48:40+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4027457373

类型：pr_comment；来源 PR ID：3975818772；时间：2026-03-09 22:56:23+00:00；评论者：ihabadham

<pre>#2581 has been merged, covering the #2432 fix (doctor false positives for Pro/SWC) with the review issues addressed. The #2431 portion is no longer needed since #2476 already fixed the root cause. Closing this PR.</pre>

## pair-3977235894_3977334181

[Lakr233/AssppWeb PR #6](https://github.com/Lakr233/AssppWeb/pull/6) 与 [PR #8](https://github.com/Lakr233/AssppWeb/pull/8)

- 标题 A：Fix wrangler Dockerfile reference
- 标题 B：Follow-up fixes for Cloudflare one-click deployment
- 作者：JM-2023 / TastyHeadphones
- 创建时间 UTC：2026-02-23 09:42:54+00:00 / 2026-02-23 10:05:18+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3944823487

类型：pr_comment；来源 PR ID：3977235894；时间：2026-02-23 13:34:38+00:00；评论者：Lakr233

<pre>Closing — this is superseded by PR #8 which restructured the Cloudflare deployment.

The root cause (`image: &quot;../Dockerfile&quot;` failing wrangler validation) no longer exists. The current `wrangler.jsonc` uses a pre-built GHCR image (`ghcr.io/lakr233/assppweb:latest`) instead of a local Dockerfile path, so there&#x27;s no path resolution issue to fix.

Additionally, the duplicate `cloudflare/Dockerfile` approach would have been fragile (two Dockerfiles to keep in sync). The GHCR image approach on main is cleaner.

Thanks for identifying the original issue though!</pre>

## pair-3983565651_4101350724

[sqlfluff/sqlfluff PR #7536](https://github.com/sqlfluff/sqlfluff/pull/7536) 与 [PR #7645](https://github.com/sqlfluff/sqlfluff/pull/7645)

- 标题 A：ST05: fix dropping expression CTEs from WITH clause
- 标题 B：Fix ST05 dropping expression CTEs in WITH clause
- 作者：Copilot / shauneccles
- 创建时间 UTC：2026-02-24 12:51:34+00:00 / 2026-03-19 12:25:26+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4093508665

类型：pr_comment；来源 PR ID：4101350724；时间：2026-03-19 21:48:30+00:00；评论者：shauneccles

<pre>Apologies - I missed that PR #7536 already addresses this issue. I looked for existing PRs but it was late and I overlooked it. Closing in favour of #7536.

Sorry again 😓</pre>

## pair-3984858957_3987569866

[zeroclaw-labs/zeroclaw PR #1669](https://github.com/zeroclaw-labs/zeroclaw/pull/1669) 与 [PR #1731](https://github.com/zeroclaw-labs/zeroclaw/pull/1731)

- 标题 A：fix(build): add explicit [[bin]] configuration to prevent target inference conflicts
- 标题 B：[supersede #1669] fix(build): add explicit [[bin]] configuration to prevent target inference conflicts
- 作者：theonlyhennygod / chumyin
- 创建时间 UTC：2026-02-24 17:12:19+00:00 / 2026-02-25 06:50:02+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3957213276

类型：pr_comment；来源 PR ID：3984858957；时间：2026-02-25 06:50:04+00:00；评论者：chumyin

<pre>Superseded by #1731 for conflict-free replay on top of latest dev. Continuing with the same CI-green merge policy. Original PR remains open until #1731 merge + green CI, then will be closed by supersede finalization.</pre>

## pair-3984866271_3987570042

[zeroclaw-labs/zeroclaw PR #1670](https://github.com/zeroclaw-labs/zeroclaw/pull/1670) 与 [PR #1732](https://github.com/zeroclaw-labs/zeroclaw/pull/1732)

- 标题 A：fix(channels/telegram): respect mention_only for non-text messages in groups
- 标题 B：[supersede #1670] fix(channels/telegram): respect mention_only for non-text messages in groups
- 作者：theonlyhennygod / chumyin
- 创建时间 UTC：2026-02-24 17:13:53+00:00 / 2026-02-25 06:50:05+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3957213447

类型：pr_comment；来源 PR ID：3984866271；时间：2026-02-25 06:50:07+00:00；评论者：chumyin

<pre>Superseded by #1732 for conflict-free replay on top of latest dev. Continuing with the same CI-green merge policy. Original PR remains open until #1732 merge + green CI, then will be closed by supersede finalization.</pre>

## pair-3984876447_3987570305

[zeroclaw-labs/zeroclaw PR #1671](https://github.com/zeroclaw-labs/zeroclaw/pull/1671) 与 [PR #1734](https://github.com/zeroclaw-labs/zeroclaw/pull/1734)

- 标题 A：fix(web): rebuild dashboard assets with POST /api/doctor fix
- 标题 B：[supersede #1671] fix(web): rebuild dashboard assets with POST /api/doctor fix
- 作者：theonlyhennygod / chumyin
- 创建时间 UTC：2026-02-24 17:16:04+00:00 / 2026-02-25 06:50:10+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3957213686

类型：pr_comment；来源 PR ID：3984876447；时间：2026-02-25 06:50:12+00:00；评论者：chumyin

<pre>Superseded by #1734 for conflict-free replay on top of latest dev. Continuing with the same CI-green merge policy. Original PR remains open until #1734 merge + green CI, then will be closed by supersede finalization.</pre>

## pair-3985131354_3987572570

[zeroclaw-labs/zeroclaw PR #1678](https://github.com/zeroclaw-labs/zeroclaw/pull/1678) 与 [PR #1736](https://github.com/zeroclaw-labs/zeroclaw/pull/1736)

- 标题 A：feat(ci): add MUSL static binaries for Alpine Linux support
- 标题 B：[supersede #1678] feat(ci): add MUSL static binaries for Alpine Linux support
- 作者：theonlyhennygod / chumyin
- 创建时间 UTC：2026-02-24 18:13:05+00:00 / 2026-02-25 06:50:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3957216129

类型：pr_comment；来源 PR ID：3985131354；时间：2026-02-25 06:50:53+00:00；评论者：chumyin

<pre>Superseded by #1736 for conflict-free replay on top of latest dev. Continuing with the same CI-green merge policy. Original PR remains open until #1736 merge + green CI, then will be closed by supersede finalization.</pre>

## pair-3988039659_4006985033

[TanStack/db PR #1294](https://github.com/TanStack/db/pull/1294) 与 [PR #1312](https://github.com/TanStack/db/pull/1312)

- 标题 A：feat: Subqueries in SELECT for hierarchical data (includes)
- 标题 B：Recursive includes exploration
- 作者：kevin-dp / samwillis
- 创建时间 UTC：2026-02-25 08:45:04+00:00 / 2026-03-01 11:35:16+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4118249434

类型：pr_comment；来源 PR ID：4006985033；时间：2026-03-24 13:21:50+00:00；评论者：kevin-dp

<pre>Closing as superseded by https://github.com/TanStack/db/pull/1294</pre>

## pair-3990324884_4020751574

[nearai/ironclaw PR #364](https://github.com/nearai/ironclaw/pull/364) 与 [PR #528](https://github.com/nearai/ironclaw/pull/528)

- 标题 A：Harden web auth: limit query-token auth to SSE endpoints
- 标题 B：fix(security): restrict query-token auth to SSE endpoints only
- 作者：lawyered0 / ilblackdragon
- 创建时间 UTC：2026-02-25 16:03:49+00:00 / 2026-03-04 08:27:48+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3996026122

类型：pr_comment；来源 PR ID：3990324884；时间：2026-03-04 08:27:59+00:00；评论者：ilblackdragon

<pre>Superseded by #528 which implements this fix rebased cleanly on current main (the original branch was deleted and main&#x27;s test infra had diverged).</pre>

### 证据 pr_comment:4049188304

类型：pr_comment；来源 PR ID：3990324884；时间：2026-03-12 18:50:27+00:00；评论者：zmanian

<pre>Closing — superseded by #528 (merged) per collaborator comment.</pre>

## pair-3993275977_4101562413

[yhs0602/Android-Disassembler PR #727](https://github.com/yhs0602/Android-Disassembler/pull/727) 与 [PR #728](https://github.com/yhs0602/Android-Disassembler/pull/728)

- 标题 A：Simplify release workflow: remove signing, fix deprecated action
- 标题 B：Codex/maintenance baseline
- 作者：Copilot / yhs0602
- 创建时间 UTC：2026-02-26 04:52:25+00:00 / 2026-03-19 13:05:02+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4094112891

类型：pr_comment；来源 PR ID：3993275977；时间：2026-03-19 23:27:20+00:00；评论者：yhs0602

<pre>Closing as superseded by #728. The maintenance baseline PR now carries the current release/preview workflow changes on the maintained branch.</pre>

## pair-3996184406_4160757393

[camunda/camunda PR #47005](https://github.com/camunda/camunda/pull/47005) 与 [PR #49938](https://github.com/camunda/camunda/pull/49938)

- 标题 A：feat: add realistic REST API weekly load test
- 标题 B：feat: use REST API by default in load tests
- 作者：Copilot / ChrisKujawa
- 创建时间 UTC：2026-02-26 15:23:58+00:00 / 2026-03-28 16:37:26+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4148483910

类型：pr_comment；来源 PR ID：3996184406；时间：2026-03-28 17:31:50+00:00；评论者：ChrisKujawa

<pre>Replaced by #49938 </pre>

## pair-4001844377_4007980034

[openclaw/openclaw PR #28945](https://github.com/openclaw/openclaw/pull/28945) 与 [PR #30886](https://github.com/openclaw/openclaw/pull/30886)

- 标题 A：fix(discord): expose EventQueue listenerTimeout as configurable option
- 标题 B：fix(discord): raise event queue listener timeout for long handlers
- 作者：Glucksberg / liuxiaopai-ai
- 创建时间 UTC：2026-02-27 16:30:07+00:00 / 2026-03-01 18:44:21+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3981649929

类型：pr_comment；来源 PR ID：4007980034；时间：2026-03-02 02:21:19+00:00；评论者：steipete

<pre>Superseded by #28945 (already merged to `main`).

`#28945` landed the canonical approach:
- default Discord Carbon `eventQueue.listenerTimeout=120000`
- user-configurable `channels.discord.accounts.&lt;id&gt;.eventQueue.*`
- provider regression coverage

Closing this duplicate to keep the queue clean.

Thanks for the contribution.
</pre>

## pair-4005983018_4011852872

[aaddrick/claude-desktop-debian PR #269](https://github.com/aaddrick/claude-desktop-debian/pull/269) 与 [PR #273](https://github.com/aaddrick/claude-desktop-debian/pull/273)

- 标题 A：feat: KVM/bwrap isolation backends for cowork mode
- 标题 B：Update CLAUDE.md with standard header, common commands, and key scripts
- 作者：aaddrick / sergeypusanov-dev
- 创建时间 UTC：2026-03-01 02:07:59+00:00 / 2026-03-02 15:27:36+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_review:3885043655

类型：pr_review_body；来源 PR ID：4011852872；时间：2026-03-03 21:06:14+00:00；评论者：aaddrick

<pre>Hey, thanks for putting this together. The Key Scripts section is a genuinely useful addition, and the RPM artifact correction is a real fix. A few things need to be addressed before this is ready to merge though.

**1. The header change is unnecessary**

Replacing `# Claude Desktop Debian - Development Notes` with `# CLAUDE.md` plus the boilerplate &quot;This file provides guidance to Claude Code&quot; adds no information. Claude Code already knows what CLAUDE.md is and why it exists. The original title was more descriptive, not less. This looks like cargo-culting a template header that doesn&#x27;t apply here. I&#x27;d drop this change entirely and keep the original title.

**2. Key Scripts has factual errors**

The `cowork-vm-service.js` entry says &quot;no VM isolation yet.&quot; That&#x27;s not accurate. KVM and bwrap isolation backends were merged in PR #269. The description should reflect what the script actually does now.

The `frame-fix-wrapper.js` entry is listed under `scripts/` but it lives in the repo root. Same for `frame-fix-entry.js`, which isn&#x27;t listed at all. The path prefix is misleading for anyone trying to find these files.

**3. The linting commands are wrong**

The PR shows:

```bash
shellcheck build.sh scripts/*.sh
actionlint
```

That&#x27;s not how we lint this project. The `/lint` skill handles file targeting with the right flags and also runs actionlint on the workflows. Showing raw commands here would give contributors the wrong mental model and probably produce different results than what CI checks. I&#x27;d replace this block with a note to use `/lint` and link to the STYLEGUIDE.md like the Code Style section already does.

**4. Process note: PR from `main`**

This is a minor thing, but this PR is from your `main` branch. Future contributions are easier to manage from a feature branch (e.g., `docs/update-claude-md`). It keeps your fork&#x27;s main clean and makes it simpler to revise if review feedback comes in.

---

To summarize what I&#x27;d keep: the Project Overview expansion is good, the Common Commands build section is useful, the Key Scripts concept is solid once the inaccuracies are fixed, and the CI/CD restructuring with the RPM artifact addition is a real improvement. The linting block and the header change are the two things I&#x27;d cut or correct before merging.

---
Written by Claude Sonnet 4.6 via [Claude Code](https://claude.ai/code)</pre>

## pair-4007309376_4008241298

[openclaw/openclaw PR #30705](https://github.com/openclaw/openclaw/pull/30705) 与 [PR #30966](https://github.com/openclaw/openclaw/pull/30966)

- 标题 A：fix(discord): add debug logs for allowlist drops [AI-assisted]
- 标题 B：fix(discord): log ignored messages from non-allowlisted channels
- 作者：liuxiaopai-ai / haosenwang1018
- 创建时间 UTC：2026-03-01 14:15:04+00:00 / 2026-03-01 20:50:31+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3981628725

类型：pr_comment；来源 PR ID：4007309376；时间：2026-03-02 02:13:38+00:00；评论者：steipete

<pre>Superseded by #30966, which is already merged into `main`.

Closing this as duplicate to keep the queue clean.

Thanks for the contribution.
</pre>

## pair-4008035064_4008916219

[openclaw/openclaw PR #30904](https://github.com/openclaw/openclaw/pull/30904) 与 [PR #31181](https://github.com/openclaw/openclaw/pull/31181)

- 标题 A：fix(voice-call): accept externally-initiated outbound Twilio calls
- 标题 B：fix(voice-call): accept externally-initiated Twilio outbound-api calls
- 作者：liuxiaopai-ai / scoootscooob
- 创建时间 UTC：2026-03-01 19:07:26+00:00 / 2026-03-02 02:24:52+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3981830554

类型：pr_comment；来源 PR ID：4008035064；时间：2026-03-02 03:39:12+00:00；评论者：steipete

<pre>Closing as duplicate/superseded by #31181 for #30900.

Why this is superseded:
- Same root bug: externally-initiated Twilio outbound-api calls were not tracked, causing stream rejection.
- Same core code path touched (`extensions/voice-call/src/manager/events.ts`).
- #31181 carries equivalent fix intent plus broader explicit regression coverage and changelog context in one thread.

Keeping #31181 as the canonical merge path to avoid split review/CI for the same behavior change.
</pre>

## pair-4008469059_4008614235

[openclaw/openclaw PR #31035](https://github.com/openclaw/openclaw/pull/31035) 与 [PR #31080](https://github.com/openclaw/openclaw/pull/31080)

- 标题 A：Auto-reply: strip inline NO_REPLY token from mixed replies
- 标题 B：fix(auto-reply): strip NO_REPLY token from mixed-content messages
- 作者：webdevtodayjason / scoootscooob
- 创建时间 UTC：2026-03-01 22:43:23+00:00 / 2026-03-01 23:57:31+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3981521024

类型：pr_comment；来源 PR ID：4008469059；时间：2026-03-02 01:21:57+00:00；评论者：steipete

<pre>Superseded by a landed fix on \.

- landed via #31080
- commit: a6a742f3da5915c24f81fce1266fbf1d95f6768f

Closing this PR as duplicate/superseded to keep one canonical patch path.
</pre>

### 证据 pr_comment:3981522461

类型：pr_comment；来源 PR ID：4008469059；时间：2026-03-02 01:22:26+00:00；评论者：steipete

<pre>Correction with exact refs:

- superseded by landed fix #31080 on main
- commit: a6a742f3da5915c24f81fce1266fbf1d95f6768f
</pre>

## pair-4008614235_4008723608

[openclaw/openclaw PR #31080](https://github.com/openclaw/openclaw/pull/31080) 与 [PR #31109](https://github.com/openclaw/openclaw/pull/31109)

- 标题 A：fix(auto-reply): strip NO_REPLY token from mixed-content messages
- 标题 B：Auto-reply: strip NO_REPLY markers in mixed text replies
- 作者：scoootscooob / liuxiaopai-ai
- 创建时间 UTC：2026-03-01 23:57:31+00:00 / 2026-03-02 00:52:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3981520691

类型：pr_comment；来源 PR ID：4008723608；时间：2026-03-02 01:21:50+00:00；评论者：steipete

<pre>Superseded by a landed fix on \.

- landed via #31080
- commit: a6a742f3da5915c24f81fce1266fbf1d95f6768f

Closing this PR as duplicate/superseded to keep one canonical patch path.
</pre>

### 证据 pr_comment:3981522283

类型：pr_comment；来源 PR ID：4008723608；时间：2026-03-02 01:22:23+00:00；评论者：steipete

<pre>Correction with exact refs:

- superseded by landed fix #31080 on main
- commit: a6a742f3da5915c24f81fce1266fbf1d95f6768f
</pre>

## pair-4012733219_4013365410

[openclaw/openclaw PR #32045](https://github.com/openclaw/openclaw/pull/32045) 与 [PR #32183](https://github.com/openclaw/openclaw/pull/32183)

- 标题 A：fix(webchat): suppress NO_REPLY control token in chat UI
- 标题 B：fix(webchat): suppress NO_REPLY token in chat transcript rendering
- 作者：liuxiaopai-ai / ademczuk
- 创建时间 UTC：2026-03-02 18:42:54+00:00 / 2026-03-02 21:22:55+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3987368966

类型：pr_comment；来源 PR ID：4012733219；时间：2026-03-02 22:39:46+00:00；评论者：Takhoffman

<pre>Closing as superseded by #32183, which is now merged and covers the NO_REPLY history/UI guardrails with regression tests.</pre>

## pair-4012754295_4012792869

[openclaw/openclaw PR #32049](https://github.com/openclaw/openclaw/pull/32049) 与 [PR #32059](https://github.com/openclaw/openclaw/pull/32059)

- 标题 A：fix(telegram): reduce startup command sync API pressure
- 标题 B：fix: skip Telegram command sync when menu is unchanged
- 作者：liuxiaopai-ai / scoootscooob
- 创建时间 UTC：2026-03-02 18:48:40+00:00 / 2026-03-02 18:59:07+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3986319360

类型：pr_comment；来源 PR ID：4012754295；时间：2026-03-02 19:10:33+00:00；评论者：steipete

<pre>Thanks for the fix. I compared this against the concurrent command-sync PR in code.

Closing as duplicate/superseded by #32059:
- Both target the same startup API-pressure/rate-limit problem in Telegram command sync.
- Both touch the same core files (`src/telegram/bot-native-command-menu.ts` and test).
- #32059 adds persistent command-list hashing and skip-on-unchanged behavior, which avoids repeated sync calls across restarts with unchanged menus.

Given the same bug target and stronger no-op protection in #32059, I’m closing this one to keep a single land path.
</pre>

## pair-4012792869_4012903656

[openclaw/openclaw PR #32059](https://github.com/openclaw/openclaw/pull/32059) 与 [PR #32092](https://github.com/openclaw/openclaw/pull/32092)

- 标题 A：fix: skip Telegram command sync when menu is unchanged
- 标题 B：Telegram: skip deleteMyCommands before non-empty command sync
- 作者：scoootscooob / liuxiaopai-ai
- 创建时间 UTC：2026-03-02 18:59:07+00:00 / 2026-03-02 19:28:02+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3986503851

类型：pr_comment；来源 PR ID：4012903656；时间：2026-03-02 19:44:58+00:00；评论者：steipete

<pre>Closing as superseded by #32059.

Why this is duplicate now:
- #32059 already fixes #32017 by avoiding repeated Telegram command sync on restart when the menu is unchanged (hash-based cache + account/bot identity scoping).
- That merged path removes the repeated `deleteMyCommands`/`setMyCommands` churn for unchanged command sets, which was the lockout/rate-limit trigger described in #32017.
- #32017 is already closed by the merged fix.

If we still want a follow-up optimization for *changed* command sets (skip delete before set), that should be proposed as a new scoped PR against current main behavior, not as the same #32017 fix.
</pre>

## pair-4012882596_4013365410

[openclaw/openclaw PR #32082](https://github.com/openclaw/openclaw/pull/32082) 与 [PR #32183](https://github.com/openclaw/openclaw/pull/32183)

- 标题 A：Gateway: hide NO_REPLY-only entries from chat.history
- 标题 B：fix(webchat): suppress NO_REPLY token in chat transcript rendering
- 作者：liuxiaopai-ai / ademczuk
- 创建时间 UTC：2026-03-02 19:22:26+00:00 / 2026-03-02 21:22:55+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=True

### 证据 pr_comment:3987368857

类型：pr_comment；来源 PR ID：4012882596；时间：2026-03-02 22:39:44+00:00；评论者：Takhoffman

<pre>Closing as superseded by #32183, which is now merged and covers the NO_REPLY history/UI guardrails with regression tests.</pre>

## pair-4013375906_4013923139

[openclaw/openclaw PR #32185](https://github.com/openclaw/openclaw/pull/32185) 与 [PR #32309](https://github.com/openclaw/openclaw/pull/32309)

- 标题 A：fix(daemon): resolve Homebrew Cellar path to stable symlink for gateway install
- 标题 B：Daemon: prefer stable Homebrew node symlink for gateway install
- 作者：scoootscooob / liuxiaopai-ai
- 创建时间 UTC：2026-03-02 21:25:35+00:00 / 2026-03-02 23:49:01+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:3987711985

类型：pr_comment；来源 PR ID：4013923139；时间：2026-03-02 23:52:54+00:00；评论者：steipete

<pre>Thanks for the patch. I reviewed this against current `main` and this change is already covered by a merged fix, so this PR is now a duplicate.

Superseded by #32185 (merged), which already shipped the Homebrew Cellar -&gt; stable symlink runtime resolution for daemon install paths, including regression coverage in `src/daemon/runtime-paths*.test.ts` and broader formula handling.

Keeping this open would duplicate the same maintenance surface in the same files with overlapping behavior.

Closing as duplicate of #32185.
</pre>

## pair-4018662740_4033722149

[camunda/camunda PR #47558](https://github.com/camunda/camunda/pull/47558) 与 [PR #47899](https://github.com/camunda/camunda/pull/47899)

- 标题 A：docs: improve copilot-instructions.md and ci.agent.md for better AI guidance
- 标题 B：ci: restructure copilot instructions for coding agent compatibility
- 作者：Copilot / ChrisKujawa
- 创建时间 UTC：2026-03-03 20:54:47+00:00 / 2026-03-06 11:33:32+00:00
- 风险标记：同账号=False；提交前评论=False；快照引用=False

### 证据 pr_comment:4011923378

类型：pr_comment；来源 PR ID：4018662740；时间：2026-03-06 14:02:28+00:00；评论者：ChrisKujawa

<pre>Replaced by https://github.com/camunda/camunda/pull/47899</pre>

