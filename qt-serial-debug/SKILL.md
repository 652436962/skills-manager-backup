---
name: qt-serial-debug
description: 使用 QtSerialAssist 的 MCP 工具（~/.mcp-manager/qt-serial-assist/server.py）对串口/网络/Modbus 设备进行自动化调试。当需要枚举或打开串口、发送数据并等待设备回包、读写 Modbus 保持寄存器、终端登录 uboot/嵌入式设备、发送快捷命令、设置定时自动发送、或按 run_sequence 批量回归测试时使用。依赖 QtSerialAssist 正在运行且 AI 控制服务（127.0.0.1:45678）已开启。
---

# QtSerialAssist 调试

## 概述

通过 MCP 工具遥控运行中的 QtSerialAssist，完成串口 / 网络 / Modbus 设备的自动化调试。用户用自然语言描述意图（如"读从站 1 的 0~9 保持寄存器"），按本技能选择合适工具并编排调用顺序。

## 前置检查（每次调试开始前）

1. 确认 QtSerialAssist 正在运行且"AI 控制服务"已开启：调用 `get_device_status` 验证链路，失败则提示用户先启动程序并开启设置页的 AI 控制服务。
2. 需要 Modbus 时先确认串口已打开（`serial_status`），组合工具要求串口已开。

## 工作流决策

- **用户只提需求、不指定工具**：优先用组合工具（`modbus_read_holdings` / `modbus_write_register` / `run_sequence`），它们自动完成 清缓冲→发送→等待→解析。
- **需要中间查看原始数据**：用原子工具序列 `serial_clear_buffer` → `serial_send` → `serial_await` → `serial_read_buffer`。
- **等待设备回包**：一律先 `serial_clear_buffer` 再 `serial_await`；await 是预匹配且**不消费缓冲**，读数据用 `serial_read_buffer`。
- **串口独占**：一个串口同一时间只能被一个程序占用。若 GUI 已手动打开，`open_serial` 会失败——让 AI 管就全交给 AI。

## 调试 SOP

### 1. 串口连接
1. `list_serial_ports` 枚举可用串口。
2. `open_serial(port, baud, data_bits, stop_bits, parity)` 打开，默认 115200-8-N-1。
3. `serial_status` 复核参数。

### 2. 数据收发与等待
1. `serial_clear_buffer` 清空旧数据。
2. `serial_send(data, hex_mode, newline)` 发送；hex 无空格（如 `010300000002`）由服务端自动规范化。
3. `serial_await(timeout_ms, keyword, count)` 阻塞等待匹配；keyword 支持 hex 或 ASCII、忽略大小写。
4. 需要实际内容时 `serial_read_buffer(max_items)` 读取并清空缓冲。

### 3. Modbus 调试
1. 确认串口已打开。
2. 读：`modbus_read_holdings(slave, start_addr, count, fmt="rtu")` → 返回寄存器数值列表。
3. 写：`modbus_write_register(slave, addr, value, fmt="rtu")` → 返回写入结果。
4. 连续监控：循环读多次，或拼 `run_sequence`。
5. 读不到值时：检查波特率、从站地址、寄存器范围，先 `serial_clear_buffer` 清噪声再重试。

### 4. 终端登录（uboot / 嵌入式 shell）
1. 打开串口后先 `serial_clear_buffer`。
2. `serial_send("", newline=true)` 发送回车唤醒设备。
3. `serial_await(keyword="login:")` → 发用户名 → `serial_await(keyword="Password:")` → 发密码。
4. 密码等敏感内容不要写进日志、注释或回归测试模板；控制服务仅监听 127.0.0.1。

### 5. 网络调试
1. `network_open(protocol="tcp_server"|"tcp_client"|"udp", ip, port)`。
2. `network_send(data, hex_mode)` / `network_await` 收发。
3. `network_status` 查看、`network_close` 关闭。

### 6. 批量回归
1. 用 `run_sequence(steps_json)`，支持 `serial.*`、`net.*`、`delay`、`modbus.frame`、`note` 等 action。
2. 模板见 `~/.mcp-manager/qt-serial-assist/examples/regression_test.json`。
3. 汇总输出每步 pass/fail 报告。

### 7. 快捷命令与定时发送
- `list_quick_commands` 列出组/命令；`send_quick_command` 直接发 data 或按 group+name 发送。
- `set_auto_send(enabled, interval_ms)` 设置/取消定时自动发送。

## 资源

- `references/tools.md`：20 个 MCP 工具签名与说明（含组合工具、run_sequence action 类型）
- `references/usage.md`：按场景的"怎么说"例句、完整 SOP、常见坑对照表
- 详细文档：`~/.mcp-manager/qt-serial-assist/README.md`（部署）与 `USAGE.md`（话术）
