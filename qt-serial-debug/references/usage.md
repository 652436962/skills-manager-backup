# 调试话术速查

不需要用户记工具名，按场景把意图+参数说清即可。完整版见 `~/.mcp-manager/qt-serial-assist/USAGE.md`。

## 场景例句

**串口**
- "有哪些串口可用"
- "打开 /dev/ttyUSB0，115200，8 数据位 1 停止位 无校验"
- "用 hex 发送 01 03 00 00 00 0A"（无空格自动补空格）
- "发送 AT 并追加回车换行"
- "等设备回 'OK'，超时 2 秒"

**接收/缓冲**
- "清空接收缓冲" → `serial_clear_buffer`
- "等收到 5 条数据再返回" → `serial_await(count=5)`
- "把缓冲里最新的数据读出来" → `serial_read_buffer`（读后即清）

**Modbus**
- "读从站 1 的 0~9 保持寄存器" → `modbus_read_holdings(slave=1, start_addr=0, count=10)`
- "把从站 1 的寄存器 4 写成 100" → `modbus_write_register(slave=1, addr=4, value=100)`
- "用 Modbus TCP 读从站 1 的 0~9" → `fmt="tcp"`
- "每 1 秒读一次，读 3 次" → 循环调用或 `run_sequence`

**网络**
- "开 TCP server 监听 127.0.0.1:8080"
- "TCP 客户端连接 192.168.1.10:502"
- "UDP 目标 192.168.1.10:5000"

**快捷/定时**
- "有哪些快捷命令组" / "发快捷命令组 '默认' 里的 '重启'"
- "每 1000ms 自动发送一次 'AA 55'" / "停掉定时自动发送"

**回归**
- "按 examples/regression_test.json 跑一遍回归，输出 pass/fail 报告" → `run_sequence`

## 完整调试 SOP

**串口 + Modbus**
1. "扫描串口" → `list_serial_ports`
2. "打开 /dev/ttyUSB0，115200" → `open_serial`
3. "读从站 1 的 0~9 保持寄存器" → `modbus_read_holdings`
4. "把寄存器 4 写成 100，再读一次确认" → `modbus_write_register` + 再读
5. "关闭串口" → `close_serial`

**终端登录（uboot / 嵌入式 shell）**
1. 打开串口
2. 发送回车唤醒，`serial_await(keyword="login:")`
3. 输用户名，`serial_await(keyword="Password:")`
4. 输密码（不要写进日志/回归模板；本服务仅监听 127.0.0.1）

## 常见坑

| 坑 | 现象 | 正确做法 |
|----|------|---------|
| 串口被占用 | open 失败 | 一个串口只能被一个程序占用；让 AI 管就别在 GUI 手动开 |
| await 读到旧数据 | 回包对不上 | 先 `serial_clear_buffer` 再等待 |
| 数据总是同一条 | 一直读到老数据 | 用消费型 `serial_read_buffer` 或先 clear |
| await 超时 | 等不到关键字 | 不填 keyword 等任意回包，再用 `serial_read_buffer` 看实际内容 |
| Modbus 读不到 | 回包格式不符 | 检查波特率/从站/寄存器范围；先清噪声 |
