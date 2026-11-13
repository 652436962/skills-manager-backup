# SerialRUN 命令行使用说明

> 项目地址：<https://github.com/YaoIsAI/SerialRUN>
> 官网：<https://www.serialrun.com>
> 当前版本：**v0.4.8**
> 参考文档：`README.md`、`docs/MANUAL_CN.md`、`CLAUDE_CN.md`
> 整理日期：2026-11-13

---

## 1. 概述

SerialRUN 是面向嵌入式开发者的跨平台串口工具，一套程序同时提供 GUI 与 CLI：

- 串口终端收发（文本 / HEX / 时间戳 / CRC 校验）
- Modbus RTU/TCP 监控、帧构建、TCP↔RTU 桥接、HMI 模拟
- PLC 寄存器轮询（西门子、三菱、台达、欧姆龙预设）
- CAN（SLCAN）、I²C/SPI、示波器、文件传输（XMODEM/YMODEM/ZMODEM）
- STM32 ISP / ESP32 串口烧录
- 脚本录制与回放、CSV 数据记录
- 内置 MCP server（23 个工具），可让 AI 智能体驱动串口

CLI 部分由 `serialrun-cli` 提供，安装 deb 包后同时提供 `serialrun`、`serialrun-cli`、`serialrun-mcp` 三个命令，三者参数完全一致。

---

## 2. 安装

### 2.1 Linux（deb 包，推荐）

```bash
sudo apt install ./serialrun_0.4.8_amd64.deb
```

安装后 `serialrun`、`serialrun-cli`、`serialrun-mcp` 位于 `/usr/bin`，依赖自动解决。

运行时依赖（Ubuntu/Debian）：

```bash
sudo apt install libudev1 libxkbcommon0 libx11-6 libxcursor1 libxrandr2 libxi6 libgl1 libwayland-client0
```

### 2.2 其他平台

| 平台 | 安装包 |
| --- | --- |
| Windows x64 | `serialrun-0.4.8-windows-x64-setup.exe`（或便携 zip，内含 `serialrun-cli.exe`、`serialrun-mcp.exe`） |
| macOS Apple Silicon | `serialrun-0.4.8-macos-arm64.dmg` |
| macOS Intel | `serialrun-0.4.8-macos-x64.dmg` |
| Linux x86_64 | `serialrun_0.4.8_amd64.deb` 或 `serialrun-0.4.8-linux-x64.tar.gz` |

### 2.3 源码构建

```bash
git clone https://github.com/YaoIsAI/SerialRUN.git
cd SerialRUN
cargo build --release      # 产物在 target/release/
```

### 2.4 Linux 串口权限（必做）

```bash
sudo usermod -aG dialout $USER     # Arch 系发行版用 uucp
```

执行后需**注销并重新登录**才生效。

---

## 3. 命令总览

```text
serialrun <子命令> [参数]
serialrun-cli <子命令> [参数]      # 与上等价
```

| 子命令 | 作用 | 形式 |
| --- | --- | --- |
| `list` | 列出可用串口 | `serialrun list` |
| `connect` | 连接串口并进入交互模式 | `serialrun connect <端口> [选项]` |
| `send` | 发送一次数据 | `serialrun send <端口> <数据> [选项]` |
| `monitor` | 监听端口并打印接收数据 | `serialrun monitor <端口> [选项]` |
| `record` | 录制会话为脚本 | `serialrun record <端口> -o <文件>` |
| `replay` | 回放录制的脚本 | `serialrun replay <端口> <脚本>` |
| `agent` | JSON 输出模式，供自动化调用 | `serialrun agent [端口] <动作>` |

端口写法：Windows 用 `COM1`、`COM3`；Linux 用 `/dev/ttyUSB0`、`/dev/ttyS0`。

---

## 4. 子命令详解

### 4.1 `list` —— 列出串口

```bash
serialrun list                 # 文本输出
serialrun list --format json   # JSON 输出
```

JSON 输出示例：

```json
{
  "success": true,
  "ports": [
    {
      "name": "/dev/ttyUSB0",
      "description": "USB Device 0403:6001",
      "manufacturer": "FTDI",
      "vid": 1027,
      "pid": 24577
    }
  ]
}
```

### 4.2 `connect` —— 连接并进入交互模式

```bash
serialrun connect /dev/ttyUSB0 -b 115200
serialrun connect COM1 -b 9600 -d 7 -s 2 -p odd -f hardware
```

参数表：

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `-b, --baud` | `115200` | 波特率 |
| `-d, --data-bits` | `8` | 数据位（5/6/7/8） |
| `-s, --stop-bits` | `1` | 停止位（1/2） |
| `-p, --parity` | `none` | 校验位（`none` / `odd` / `even`） |
| `-f, --flow` | `none` | 流控（`none` / `software` / `hardware`） |

进入交互模式后可直接输入内容发送，例如 AT 指令调试：

```text
> AT
> AT+RST
> AT+CWMODE=1
> AT+CWJAP="WiFi","password"
```

### 4.3 `send` —— 发送一次数据

```bash
serialrun send COM1 "Hello\r\n"               # 发送文本，支持 \r\n 等转义
serialrun send COM1 "48 65 6C 6C 6F" --hex    # 发送十六进制（空格分隔，可省略 0x）
```

`--hex` 表示把数据按十六进制解析。常用于发送 Modbus 请求帧：

```bash
serialrun send /dev/ttyUSB0 "01 03 00 00 00 0A C5 CD" --hex
```

### 4.4 `monitor` —— 监听端口

| 选项 | 说明 |
| --- | --- |
| `-t` | 每条数据前加时间戳 |
| `-x` | HEX 模式显示 |
| `-l <文件>` | 同时写入日志文件 |

```bash
serialrun monitor COM1 -t                  # 带时间戳
serialrun monitor COM1 -x                  # 十六进制模式
serialrun monitor COM1 -t -l output.log    # 时间戳 + 记录到文件
serialrun monitor /dev/ttyUSB0 -x -t -l modbus.log   # Modbus 抓包常用组合
```

### 4.5 `record` / `replay` —— 脚本录制与回放

```bash
serialrun record COM1 -o script.txt    # 录制会话到脚本
serialrun replay COM1 script.txt       # 按脚本回放
```

适合做重复性测试：先手工操作一遍录制，之后用 `replay` 一键重放。

### 4.6 `agent` —— JSON 输出模式

面向 CI 与脚本调用，所有结果以 JSON 返回，便于程序解析。

| 用法 | 作用 |
| --- | --- |
| `serialrun agent list-ports` | 以 JSON 列出端口 |
| `serialrun agent <端口> send "<数据>" [-b 波特率]` | 发送数据 |
| `serialrun agent <端口> read --timeout <毫秒> [--max-bytes <字节>]` | 读取数据 |
| `serialrun agent <端口> run-script <脚本>` | 执行脚本 |

示例与返回：

```bash
serialrun agent list-ports
```

```json
{ "success": true, "ports": [ { "name": "/dev/ttyUSB0", "manufacturer": "FTDI", "vid": 1027, "pid": 24577 } ] }
```

```bash
serialrun agent COM1 send "Hello" -b 115200
```

```json
{ "success": true, "bytes_written": 5 }
```

```bash
serialrun agent COM1 read --timeout 1000 --max-bytes 1024
```

```json
{
  "success": true,
  "bytes_read": 10,
  "data_hex": "48656C6C6F20576F726C64",
  "data_text": "Hello World"
}
```

```bash
serialrun agent COM1 run-script script.txt
```

---

## 5. 典型工作流

### 5.1 ESP8266 / ESP32 AT 指令调试

```bash
serialrun connect /dev/ttyUSB0 -b 115200
# 交互模式中输入：
# AT
# AT+RST
# AT+CWMODE=1
# AT+CWJAP="WiFi","password"
```

### 5.2 Modbus RTU 抓包与请求

```bash
# 一边监听（HEX + 时间戳 + 落盘）
serialrun monitor /dev/ttyUSB0 -x -t -l modbus.log

# 另一边发请求帧：从站 01、功能码 03、起始 0x0000、10 个寄存器
serialrun send /dev/ttyUSB0 "01 03 00 00 00 0A C5 CD" --hex
```

### 5.3 自动化回归测试

```bash
serialrun record /dev/ttyUSB0 -o test.txt    # 首次手工操作，录制
serialrun replay /dev/ttyUSB0 test.txt       # 后续回归直接回放
```

### 5.4 在脚本 / CI 中调用

```bash
serialrun agent /dev/ttyUSB0 send "AT+RST" -b 115200
sleep 2
serialrun agent /dev/ttyUSB0 read --timeout 1000 | jq -r .data_text
```

---

## 6. MCP Server（可选）

GUI 侧边栏启用后，MCP server 默认监听 `127.0.0.1:9527`，协议为 JSON-RPC 2.0 over TCP，可在 GUI 中切换 LAN 模式或改端口。

30 秒自测：

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_ports","arguments":{}}}' \
  | nc 127.0.0.1 9527
```

共 23 个工具，常用：`list_ports`、`connect`、`disconnect`、`send`、`read`、`send_command`、`modbus_read`、`modbus_write`、`plc_read`、`plc_write`、`status`、`get_device_info`、`get_config`/`set_config`/`get_config_keys`、`clear_buffers`、`set_dtr`/`set_rts`、`get_access_log`、`load_pcap`/`query_packets`/`get_packet`/`pcap_stats`。详见 `docs/MCP_API.md`。

---

## 7. 配置文件与数据目录

数据统一保存在 `~/.serialrun/`：

| 文件 | 内容 |
| --- | --- |
| `config.toml` | 主题、语言、波特率等设置 |
| `logs.json` | 应用日志（最多 2000 条） |
| `terminal.json` | 终端收发历史（最多 5000 条） |
| `warnings.json` | 警告/错误历史（最多 1000 条） |
| `mcp_access_log.json` | MCP 访问日志（最多 1000 条） |

可设置的配置键可用 MCP 工具 `get_config_keys` 查询。

---

## 8. 故障排查

| 现象 | 解决办法 |
| --- | --- |
| 端口不在列表中 | `serialrun list` 确认；安装 CH340/CP210x/FTDI/PL2303 驱动；换数据线；关闭占用端口的程序 |
| Linux 打开端口权限被拒 | `sudo usermod -aG dialout $USER`（Arch 用 `uucp`），重新登录 |
| 文本乱码 | 波特率、数据位、校验位与设备设置不一致 |
| 无数据接收 | 检查线缆与流控设置（`-f`），确认对端已发送 |
| 自定义波特率被忽略 | v0.4.5 已修复，升级后重输速率并回车/点 Connect |
| MCP 客户端连不上 | 确认 MCP 已启用、9527 端口未被占用、防火墙允许回环 |
| Linux 应用启动失败 | 安装第 2.1 节的运行时依赖 |
| 需要诊断 | 查看 GUI 日志查看器与 `~/.serialrun/` 下 `logs.json`、`warnings.json` |

---

## 9. 速查表

```bash
# 列端口
serialrun list
serialrun list --format json

# 连接（交互）
serialrun connect /dev/ttyUSB0 -b 115200

# 发送
serialrun send /dev/ttyUSB0 "AT+RST"
serialrun send /dev/ttyUSB0 "48 65 6C 6C 6F" --hex

# 监听
serialrun monitor /dev/ttyUSB0 -t
serialrun monitor /dev/ttyUSB0 -x -t -l modbus.log

# 录制 / 回放
serialrun record /dev/ttyUSB0 -o script.txt
serialrun replay /dev/ttyUSB0 script.txt

# JSON 自动化
serialrun agent list-ports
serialrun agent /dev/ttyUSB0 send "AT+RST" -b 115200
serialrun agent /dev/ttyUSB0 read --timeout 1000 --max-bytes 1024
serialrun agent /dev/ttyUSB0 run-script test.txt
```

---

## 10. 相关文档

| 文档 | 说明 |
| --- | --- |
| `docs/MANUAL_CN.md` | 中文用户手册（CLI + GUI） |
| `docs/MANUAL.md` | 英文用户手册 |
| `CLAUDE_CN.md` | 智能体操作指南 |
| `docs/MCP_API.md` | MCP API 参考 |
| `docs/BUILD_CN.md` | 构建指南 |
| `CHANGELOG.md` | 版本变更历史 |
