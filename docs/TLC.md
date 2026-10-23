# TLC 配置

原版 statechart 工具通过 `TLA2TOOLS` 找到 `tla2tools.jar`，通过 `JAVA` 指定 Java 可执行文件；未设置 `JAVA` 时使用 PATH 中的 `java`。Java 需要 11 或更新版本。

本次安装使用 [TLA+ 官方 v1.7.4 发布包](https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4)，其中 TLC 显示版本 `2.19`。官方发布页的 SHA-1 为 `bee4a54f3ee3d4afc347c3240ec2d9e93b075104`，下载后已核对。该 jar 的 SHA-256 为 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`。

本机使用以下布局：

- jar 位于 `~/.local/share/tlaplus/1.7.4/tla2tools.jar`。
- `~/.local/bin/tlc` 调用 `tlc2.TLC`，支持 `JAVA` 和 `TLA2TOOLS` 覆盖。
- `~/.config/tlaplus/env.sh` 设置 `TLA2TOOLS`，由 `.zprofile` 读取。
- 没有更改默认 Java 版本，也没有把 jar 加入技能仓库。

新登录 shell 可运行：

```bash
tlc -h
python3 -c 'import os; print(os.environ.get("TLA2TOOLS"))'
```

TLC 的帮助命令可能以非零状态退出；是否能检查模型需要实际模型运行证明。

原版状态图测试：

```bash
node --test skills/statechart/scripts/test/statechart.test.mjs
```

在 macOS 上，`/var` 与 `/private/var` 的路径别名会影响原测试中的字符串断言。可在运行测试时把 `TMPDIR` 设为其真实路径。原测试中的 Linux `LD_PRELOAD` 故障注入和 PID namespace 场景另有平台限制。保留原测试，不通过放宽断言制造通过结果。实际结果见 [VALIDATION.md](VALIDATION.md)。
