# QtSerialAssist MCP 工具清单

MCP server：`~/.mcp-manager/qt-serial-assist/server.py`（stdio）
所有工具参数均为字符串/数字，由 FastMCP 自动转换。

## 原子工具

| 工具 | 签名 | 说明 |
|------|------|------|
| `get_device_status` | `()` | 查询设备状态：串口/网络连接、定时发送配置 |
| `list_serial_ports` | `()` | 枚举可用串口列表 |
| `open_serial` | `(port, baud=115200, data_bits=8, stop_bits=1.0, parity="none")` | 打开串口；parity: none/even/odd |
| `close_serial` | `()` | 关闭串口 |
| `serial_status` | `()` | 查询串口状态与参数 |
| `serial_send` | `(data, hex_mode=False, newline=False)` | 发送数据；hex_mode=True 时 data 为十六进制字符串（无空格自动规范化）；newline=True 追加 `\r\n` |
| `serial_await` | `(timeout_ms=3000, keyword="", count=1)` | **阻塞**等待回包；keyword 为 hex 或 ASCII 文本（忽略大小写）；不匹配则超时返回。**不消费缓冲** |
| `serial_read_buffer` | `(max_items=100)` | 读取并**清空**缓冲中最新的数据（消费型，非阻塞） |
| `serial_clear_buffer` | `()` | 清空接收缓冲，开始新一轮调试 |
| `network_open` | `(protocol, ip="127.0.0.1", port=8080)` | protocol: `tcp_server` / `tcp_client` / `udp` |
| `network_send` | `(data, hex_mode=False)` | 通过网络发送数据（TCP/UDP） |
| `network_status` | `()` | 查询网络连接状态 |
| `network_close` | `()` | 关闭网络连接 |
| `generate_modbus_frame` | `(slave, function, start_addr=0, count=1, fmt="rtu")` | 生成 Modbus RTU/ASCII/TCP 帧（含 CRC/LRC）；fmt: rtu/ascii/tcp |
| `list_quick_commands` | `(group="")` | 列出快捷命令组；指定 group 返回该组命令列表 |
| `send_quick_command` | `(data="", hex_mode=False, group="", name="")` | 发送快捷命令：直接传 data；或 group+name 从命令库查找 |
| `set_auto_send` | `(enabled, interval_ms=1000)` | 设置/取消定时自动发送 |

## 组合工具（推荐优先使用）

| 工具 | 签名 | 自动完成 |
|------|------|---------|
| `modbus_read_holdings` | `(slave, start_addr, count, timeout_ms=2000, fmt="rtu")` | 生成帧 → 清缓冲 → 发送 → 等回包 → 解析数值列表 |
| `modbus_write_register` | `(slave, addr, value, timeout_ms=2000, fmt="rtu")` | 生成写帧 → 清缓冲 → 发送 → 校验响应 |
| `run_sequence` | `(steps_json)` | 按 JSON 步骤列表依次执行并汇总 pass/fail 报告 |

## run_sequence 支持的动作类型

`serial.open` / `serial.close` / `serial.send` / `serial.await` / `serial.read` / `serial.clear`、
`net.open` / `net.close` / `net.send` / `net.await` / `net.read` / `net.clear`、
`delay`（ms）、`modbus.frame`、`note`。

模板：`~/.mcp-manager/qt-serial-assist/examples/regression_test.json`

## 注意

- `serial_await` 是"预匹配 + 不消费"：匹配到即返回，数据留在缓冲里
- 想"读"数据用 `serial_read_buffer`（读后即清），避免下一条命令读到旧数据
- Modbus 组合工具要求**串口已打开**
