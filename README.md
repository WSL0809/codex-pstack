# Pstack for Codex

忠实移植 [原版 pstack](https://github.com/cursor/plugins/tree/main/pstack) 到 Codex。保留原来的技能、工作流、参考文件、提示模板、指南、图片和辅助脚本，只对运行环境增加兼容适配。

**v0.2.0 包含 57 个原名技能，以及 `$pstack` 快捷入口，共 58 个可调用入口。** 原版 23 个工作流全部保留。Benny 的 3 个技能仍属于休眠自动化包，保持原版的启动方式。

v0.1.0 曾把技能压缩为 8 个入口。v0.2.0 已撤销这一设计，恢复原版结构。`$pstack` 现在直接调用完整的 `$poteto-mode`。

## 安装

需要 Python 3.9 或更新版本，以及支持目录符号链接的系统。安装脚本只使用 Python 标准库。

```bash
git clone https://github.com/WSL0809/codex-pstack.git
cd codex-pstack
python3 scripts/manage.py install
python3 scripts/manage.py status
```

用户级安装可供本机各 Codex 工作区使用。安装器把完整包复制到 `~/.agents/.pstack-packages/<内容摘要>/`，再把 58 个技能目录链接到 `~/.agents/skills/`。复制后的安装不依赖源码仓库位置。原版 `skills/`、`docs/`、`agents/` 和 `automations/` 的相对关系保持完整。

Codex 官方支持用户级技能目录和符号链接，见 [OpenAI 技能文档](https://developers.openai.com/codex/skills)。若新入口没有出现，开启新会话或重启客户端。Windows 需要具备创建符号链接的权限；本版已验证 macOS，未验证 Windows。

不要只复制单个 `SKILL.md`，也不要只下载一个技能目录。原版工作流存在跨技能调用，并依赖包内参考文件。

## 使用

原名保持不变。当前 Codex CLI 会按插件清单加上 `codex-pstack:` 前缀，实际调用如下；其他客户端以技能选择器显示的名称为准：

```text
$codex-pstack:pstack 复现这个问题，定位根因，修复并验证。
$codex-pstack:poteto-mode 实现这个需求。
$codex-pstack:how 解释这个子系统如何运行。
$codex-pstack:why 查明这项设计的历史原因。
$codex-pstack:architect 为这个变化比较设计方案。
$codex-pstack:arena 比较这些方案。
$codex-pstack:interrogate 审查当前改动。
$codex-pstack:statechart 展示这个状态机和已发现的问题。
$codex-pstack:correct 分析反复出现的错误，并建立约束。
```

原版使用 `disable-model-invocation: true` 的技能，在 Codex 中对应 `allow_implicit_invocation: false`。这些技能保持显式调用。原版入口不会被合并到新的概括性技能中。完整说明见 [原版 README](docs/UPSTREAM_README.md) 和 [原版指南](docs/guide/README.md)。

原版指南中的 Cursor 命令、工具、模型名和路径按 [Codex 适配说明](docs/harness/codex.md) 解释。正文保留原始用语，便于对照来源。适配层不能让 Codex 自动获得 Cursor 云代理、Bugbot、Slack、自动化服务或特定模型；缺少必要能力时，必须明确说明步骤未完成。

## 原版技能目录

| 类别 | 原名入口 |
|---|---|
| 入口与设置 | `poteto-mode`、`poteto-help`、`setup-pstack` |
| 理解与上下文 | `how`、`why`、`teach`、`recall`、`ketchup`、`in-your-own-words` |
| 设计、并行与审查 | `architect`、`arena`、`swarm`、`interrogate`、`blast-radius` |
| 测试与验证 | `tdd`、`benchmark-checklist`、`create-verification-skill`、`maintain-verification-skill`、`create-formal-verification-skill`、`maintain-formal-verification-skill`、`statechart` |
| 改进与执行记录 | `correct`、`reflect`、`automate-me`、`figure-it-out`、`show-me-your-work` |
| 写作与代码规范 | `sharpen`、`unslop`、`bro`、`technical-writing`、`no-comments`、`typescript-best-practices` |
| 服务集成 | `make-bot-ui`，保留完整流程及外部服务前提 |
| 工程原则 | 全部 24 个 `principle-*` 独立技能，名称和正文保留 |

Benny 的 `setup-benny`、`triage-issue-reports`、`reproduce-and-fix-issues` 位于 `automations/benny/skills/`。与原版一致，它们不注册为顶层入口。通过 [FOR_AGENTS.md](automations/benny/FOR_AGENTS.md) 启动，并读取 [Benny 的 Codex 适配说明](docs/harness/codex-benny.md)。安装文件不会自动启用消息发送、工单写入或后台自动化。

## 从 v0.1.0 更新

```bash
git pull --ff-only
python3 scripts/manage.py update
python3 scripts/manage.py status
```

更新器识别旧安装记录。它会移除受管的 7 个精简专项入口，替换 `$pstack`，并安装 57 个原名技能。若原安装文件已被修改，或存在同名的其他技能，更新停止，不覆盖用户内容。先保存并处理冲突，再重新运行。

后续更新同样使用以上命令。安装记录包含文件摘要；重复安装相同版本不改写文件。更新失败时，安装器尝试恢复原入口和记录。

## 项目安装与卸载

只给一个项目使用：

```bash
python3 scripts/manage.py install --project /absolute/path/to/project
python3 scripts/manage.py status --project /absolute/path/to/project
```

这会创建该项目的 `.agents/skills/` 和 `.agents/.pstack-packages/`。链接采用相对路径，移动整个项目后仍可使用。团队提交时需要同时提交这两个目录。不要同时使用同名的用户级和项目级副本，以免重复发现。

卸载本包管理的入口和完整副本：

```bash
python3 scripts/manage.py uninstall
# 项目安装：
python3 scripts/manage.py uninstall --project /absolute/path/to/project
```

其他技能和 Codex 配置不受影响。旧客户端可用 `--target "$HOME/.codex/skills"` 显式指定目录。不要同时在两个用户目录安装。

安装进程被强制终止或机器断电后，可能留下 `.pstack-install.lock`、`.pstack-stage-*` 或完整包的暂存目录。先确认没有安装进程运行，再检查记录及 `old/` 备份。不要直接清空这些目录。普通异常回滚已有测试，断电恢复未自动化。

## 原版保留与校验

固定来源是上游 `0.15.30`，提交 `8b3326d99fd4b993cb33a24dad8af03175c642c5`。本版不声称跟随上游最新提交。

- `upstream/pstack.zip` 保存完整的 184 个原始文件。
- `upstream/lock.json` 保存来源、文件摘要和可执行权限。
- `migration.json` 逐文件记录安装路径、摘要和适配状态。
- `scripts/port_upstream.py` 从固定快照重建适配文件。
- `docs/harness/codex.md` 集中记录工具、模型、路径和权限差异。

所有原版技能正文均未删减。辅助脚本中只有 worktree 审计脚本做了窄范围调整：历史目录必须显式提供；缺少历史时，候选项保持待检查。其他原版脚本、锁文件、测试和示例保留原始字节。

```bash
python3 scripts/port_upstream.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/check_codex.py
```

最后一条命令需要已安装本包的本机 Codex CLI。完整验证结果及未覆盖范围见 [VALIDATION.md](docs/VALIDATION.md)，适配范围见 [MIGRATION.md](docs/MIGRATION.md)。Bun、Node、Java、TLC 及各种服务连接是原版工具的独立依赖。应在可写副本中安装工具依赖，避免修改受管安装。

TLC 的配置与测试说明见 [TLC.md](docs/TLC.md)。

## 插件分发与许可

本包保留 `plugin.json` 和 `.codex-plugin/plugin.json`。`marketplace.json` 是父目录市场的示例条目，`./codex-pstack` 相对于市场根目录。个人跨工作区使用时，运行安装脚本即可。不要同时通过插件和直接安装重复注册同名技能。

本项目已在 GitHub 公开，尚未提交到 OpenAI 公共插件目录。插件流程见 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。本机安装不会自动同步到其他机器或云环境。

保留原作者 Lauren Tan 的 [MIT 许可](LICENSE)。这是社区移植版本，不是原作者或 OpenAI 官方发布。
