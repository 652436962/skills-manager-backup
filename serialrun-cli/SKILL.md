---
name: serialrun-cli
description: 使用 SerialRUN 命令行（serialrun / serialrun-cli）做串口操作。触发词：serialrun、serialrun-cli、串口命令行收发、AT 指令测试、Modbus RTU 命令行抓包、串口脚本录制回放、agent JSON 模式自动化。当需要用命令（而非 GUI）列出串口、发送数据、监听抓包、录放脚本，或排查串口读写问题时使用。
disable-model-invocation: false
---

# SerialRUN 命令行

## 概述

SerialRUN（<https://github.com/YaoIsAI/SerialRUN>）是面向嵌入式开发者的跨平台串口工具，GUI 与 CLI 同源。命令行部分由 `serialrun-cli` 提供；安装 deb 包后 `serialrun`、`serialrun-cli`、`serialrun-mcp` 三个命令**参数完全一致**，可互换使用。本文以 `serialrun` 为简称。

核心能力：串口收发（文本/HEX/时间戳/CRC）、Modbus RTU/TCP、PLC 轮询、CAN（SLCAN）、I²C/SPI、文件传输、STM32/ESP32 串口烧录、脚本录放、JSON 模式的 agent 接口、内嵌 MCP server（23 工具）。

## 环境准备

```bash
# 安装（Linux）
sudo apt install ./serialrun_0.4.8_amd64.deb
# 运行时依赖（Ubuntu/Debian，GUI 或首启失败时补装）
sudo apt install libudev1 libxkbcommon0 libx11-6 libxcursor1 libxrandr2 libxi6 libgl1 libwayland-client0

# 串口权限（Linux 必做，执行后需注销重新登录）
sudo usermod -aG dialout $USER     # Arch 系用 uucp
```

先确认命令可用再继续：

```bash
serialrun list
```

若命令不存在，说明未安装或不在 PATH（deb 安装位置 `/usr/bin`）；不要假设它存在。

## 命令总览

| 子命令 | 作用 | 形式 |
| --- | --- | --- |
| `list` | 列出可用串口 | `serialrun list [--format json]` |
| `connect` | 连接并进入交互模式 | `serialrun connect <端口> [选项]` |
| `send` | 发送一次数据 | `serialrun send <端口> <数据> [选项]` |
| `monitor` | 监听端口打印接收数据 | `serialrun monitor <端口> [选项]` |
| `record` | 录制会话为脚本 | `serialrun record <端口> -o <文件>` |
| `replay` | 回放脚本 | `serialrun replay <端口> <脚本>` |
| `agent` | JSON 输出模式（自动化） | `serialrun agent [端口] <动作>` |

端口写法：Linux `/dev/ttyUSB0`、`/dev/ttyS0`、`/dev/ttyACM0`；Windows `COM1`、`COM3`。

## 连接参数（connect，send/monitor 同理）

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `-b, --baud` | `115200` | 波特率 |
| `-d, --data-bits` | `8` | 数据位（5/6/7/8） |
| `-s, --stop-bits` | `1` | 停止位（1/2） |
| `-p, --parity` | `none` | 校验位：`none` / `odd` / `even` |
| `-f, --flow` | `none` | 流控：`none` / `software` / `hardware` |

## 常用操作

### 列端口

```bash
serialrun list
serialrun list --format json      # 供脚本解析：name / description / manufacturer / vid / pid
```

### 连接并交互（AT 指令调试）

```bash
serialrun connect /dev/ttyUSB0 -b 115200
# 交互模式中直接输入：AT / AT+RST / AT+CWMODE=1
```

### 发送数据

```bash
serialrun send /dev/ttyUSB0 "AT+RST"                  # 文本，支持 \r\n 等转义
serialrun send /dev/ttyUSB0 "48 65 6C 6C 6F" --hex    # 十六进制（空格分隔）
```

### 监听 / 抓包

| 选项 | 说明 |
| --- | --- |
| `-t` | 加时间戳 |
| `-x` | HEX 模式显示 |
| `-l <文件>` | 同时写入日志文件 |

```bash
serialrun monitor /dev/ttyUSB0 -t
serialrun monitor /dev/ttyUSB0 -x -t -l modbus.log    # Modbus 抓包常用组合
```

### 脚本录制 / 回放

```bash
serialrun record /dev/ttyUSB0 -o script.txt   # 先手工操作一遍，录制下来
serialrun replay /dev/ttyUSB0 script.txt      # 之后一键重放，做回归测试
```

### agent 模式（JSON 输出）

| 用法 | 作用 |
| --- | --- |
| `serialrun agent list-ports` | JSON 列出端口 |
| `serialrun agent <端口> send "<数据>" [-b 速率]` | 发送，返回 `{"success":true,"bytes_written":N}` |
| `serialrun agent <端口> read --timeout <ms> [--max-bytes <n>]` | 读取，返回 `bytes_read` / `data_hex` / `data_text` |
| `serialrun agent <端口> run-script <脚本>` | 执行脚本 |

```bash
serialrun agent /dev/ttyUSB0 send "AT+RST" -b 115200
serialrun agent /dev/ttyUSB0 read --timeout 1000 --max-bytes 1024 | jq -r .data_text
```

## 典型工作流

### Modbus RTU：一边抓包一边发请求

```bash
serialrun monitor /dev/ttyUSB0 -x -t -l modbus.log &
# 从站 01 / 功能码 03 / 起始 0x0000 / 读 10 个寄存器
serialrun send /dev/ttyUSB0 "01 03 00 00 00 0A C5 CD" --hex
```

### 自动化脚本里读串口

```bash
serialrun agent /dev/ttyUSB0 send "AT+RST" -b 115200; sleep 2
serialrun agent /dev/ttyUSB0 read --timeout 1000 | jq -r .data_text
```

## 排查规则

| 现象 | 先查什么 |
| --- | --- |
| 命令不存在 | 是否装了 deb / tar 包；`which serialrun`；deb 装到 `/usr/bin` |
| 端口列表为空 / 缺端口 | `ls /dev/ttyUSB* /dev/ttyACM*`；驱动 CH340/CP210x/FTDI/PL2303；线缆是否只能充电；`lsof` 看是否被占用 |
| `Permission denied` | 用户不在 `dialout` 组（Arch 为 `uucp`），改组后必须重新登录 |
| 乱码 | `-b/-d/-s/-p` 与设备不一致，先对齐波特率再怀疑系统 |
| 收发都无数据 | 确认 TX/RX 交叉接线、`-f` 流控设置、对端确实在发 |
| 自定义波特率无效 | 需 v0.4.5+，输入速率后回车或点 Connect |

## 注意事项

- 官方 README 未逐项列出 CLI 参数，参数表来自 `docs/MANUAL_CN.md` 与 `CLAUDE_CN.md`；遇到本文未覆盖的选项，先查这两份文档，不要臆造参数。
- `monitor` 是长时阻塞命令，在脚本中调用需自行加超时或放后台。
- 数据目录 `~/.serialrun/`（`config.toml`、`logs.json`、`terminal.json`、`warnings.json`、`mcp_access_log.json`），配置键可用 MCP 工具 `get_config_keys` 查询。
- MCP server 默认 `127.0.0.1:9527`，JSON-RPC over TCP，需在 GUI 侧边栏启用。

## 参考资料

- 完整中文说明：`references/serialrun-cli-manual.md`（含安装、全部子命令、MCP 工具表、故障排查、速查表）
- 上游仓库：<https://github.com/YaoIsAI/SerialRUN>
