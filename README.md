# Pstack for Codex

把 pstack 的工程方法改写为 Codex 可加载的技能包。统一入口是 `$pstack`。安装一次后，可在本机各个 Codex 工作区使用。

本包是独立改写版本。上游为 [cursor/plugins 的 pstack](https://github.com/cursor/plugins/tree/main/pstack)，基线提交为 `8b3326d99fd4b993cb33a24dad8af03175c642c5`。保留 MIT 许可和原作者署名。

## 快速安装

需要 Python 3.9 或更新版本。安装脚本仅使用标准库。

首次安装：

```bash
git clone https://github.com/WSL0809/codex-pstack.git
cd codex-pstack
python3 scripts/manage.py install
```

已有源码或解压包时，在本目录执行：

```bash
python3 scripts/manage.py install
python3 scripts/manage.py status
```

默认复制全部 8 个技能到 `~/.agents/skills/`。安装后的技能不依赖此源码目录的位置。安装脚本不会修改 `AGENTS.md`、Codex 模型配置、MCP 配置或项目文件。

在 Codex 新会话中输入：

```text
$pstack 实现这个需求，先确认现有行为，再修改并验证。
$pstack-debug 复现这个错误，定位根因，然后修复。
$pstack-review 审查当前 diff，不修改代码。
```

Codex CLI 和 IDE 可以用 `$` 或 `/skills` 选择技能。桌面界面也可能通过 `@` 或技能列表选择。Codex 会检测技能变化；如果没有出现，重启客户端。用户级目录、项目级目录和调用方式见 [OpenAI 官方技能文档](https://developers.openai.com/codex/skills)。

安装只让技能可用。自动选择取决于请求与技能描述是否匹配；输入 `$pstack` 可明确指定使用。技能不会自动改写所有任务，也不会在会话结束后持续执行。

## 入口

| 技能 | 用途 |
|---|---|
| `$pstack` | 选择流程，完成开发任务 |
| `$pstack-design` | 数据模型、接口、模块边界与方案比较 |
| `$pstack-debug` | 复现、根因、性能与测量 |
| `$pstack-review` | 代码审查与影响分析 |
| `$pstack-verify` | 行为验证、验证配方与形式化检查 |
| `$pstack-explain` | 机制、历史原因、教学与上下文恢复 |
| `$pstack-improve` | 反复纠错、复盘、技能改写与评估 |
| `$pstack-orchestrate` | 长任务、依赖、交接、暂停与恢复 |

普通请求可自动匹配专项技能。主入口按需读取参考文件，不要求每次加载全部流程。所有技能应当一起安装，因为它们使用包内相对链接共享规则。

## 更新与卸载

更新源码或解压新版后，在新版目录执行：

```bash
python3 scripts/manage.py update
python3 scripts/manage.py status
python3 scripts/manage.py uninstall
```

重复安装相同内容不会改写文件。更新会移除上一版管理的旧文件。若发现同名的其他技能或已安装副本有本地修改，脚本停止并报告路径。先把修改保存在别处，再处理安装；脚本不提供强制覆盖选项。其他技能不受影响。

安装记录位于技能目录的 `.pstack-install.json`，包括每个受管文件的 SHA-256。普通写入失败会回滚。进程被强制终止或机器断电时，可能留下 `.pstack-install.lock` 和 `.pstack-stage-*`。先确认没有安装进程运行，再检查临时目录中的 `old/` 备份和安装记录。不要直接清空它们。

## 仅供一个项目使用

```bash
python3 scripts/manage.py install --project /absolute/path/to/project
python3 scripts/manage.py status --project /absolute/path/to/project
python3 scripts/manage.py uninstall --project /absolute/path/to/project
```

技能将复制到该项目的 `.agents/skills/`。如果团队需要共享，可以把这部分文件及安装记录纳入版本控制。不要同时安装同名的用户级和项目级副本，否则技能选择器可能出现重复项。

对于仍使用旧技能目录的客户端，可以显式指定目标：

```bash
python3 scripts/manage.py install --target "$HOME/.codex/skills"
```

这是兼容选项。默认使用官方当前记录的 `~/.agents/skills/`。不要把同一套技能装到两个用户级目录。

本机安装不会自动同步到另一台电脑、远程主机或云环境。在那些环境执行安装，或者使用随仓库分发的项目级副本。

## 插件分发

本目录也可作为一个完整插件分发。`plugin.json` 是标准插件清单，`.codex-plugin/plugin.json` 是兼容清单。`marketplace.json` 提供本地市场条目。

要在支持本地插件市场的 Codex 客户端中测试，将下面的目录结构作为一个市场根目录：

```text
some-directory/
  .agents/plugins/marketplace.json
  codex-pstack/
    plugin.json
    skills/
```

把本包中的 `marketplace.json` 复制到上图位置，然后按客户端的本地市场流程安装。市场条目中的 `./codex-pstack` 相对于 `some-directory`。本项目尚未提交到 OpenAI 公共插件目录。流程见 [OpenAI 官方插件文档](https://developers.openai.com/plugins/build/plugins)。

个人跨工作区使用时，直接运行 Python 安装脚本即可。不要同时通过插件和直接复制安装同一套技能。

## 验证与维护

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/check_codex.py
```

包验证检查元数据、链接、迁移表和许可证。安装测试检查更新、回滚、冲突和文件保护。最后一个命令需要已安装的 Codex CLI 和用户级技能，检查当前目录与独立目录中的实际发现结果。这些检查不能证明代理在所有任务中都会正确执行技能。行为验证的记录位于 [VALIDATION.md](docs/VALIDATION.md)。

修改原则和迁移范围见 [MIGRATION.md](docs/MIGRATION.md)。每个上游技能和工作流的去向记录在 `migration.json`。改写不会通过替换产品名称自动同步上游。更新时应逐项复查工具、权限、模型和运行环境假设。
