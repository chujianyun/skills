# Hermes Ops Command Cheatsheet

这份参考给执行运维的 agent 快速查命令。

## 先手三板斧

```bash
hermes status --all
hermes doctor
hermes gateway status
```

## 配置相关

```bash
hermes config
hermes config path
hermes config env-path
hermes config check
hermes config migrate
hermes config edit
```

## Gateway 相关

```bash
hermes gateway start
hermes gateway stop
hermes gateway restart
hermes gateway status
hermes gateway setup
```

## Profiles

```bash
hermes profile list
hermes profile show <name>
hermes -p <name> gateway status
hermes -p <name> skills list
```

## Skills / Tools

```bash
hermes skills list
hermes skills check
hermes skills update
hermes tools list
hermes tools enable <name>
hermes tools disable <name>
```

## 调度与自动化

```bash
hermes cron list --all
hermes cron status
hermes cron run <job_id>
hermes webhook list
```

## 认证 / 记忆

```bash
hermes auth list
hermes auth add
hermes auth reset <provider>
hermes memory status
```

## 判断顺序

1. 先看 status / doctor / gateway status
2. 再看 config check / migrate
3. 再看 profile、skills、tools、cron
4. 还不对，再回源码层排查
