# dde-tray-development Evals

本目录包含 DDE 托盘插件开发的验证测试用例，按 references 文档结构分类。

## 目录结构

```
evals/
├── tray-plugin-spec/      # 托盘插件接口规范 evals
├── quick-panel/           # 快捷面板插件 evals
├── message-protocol/      # 消息协议 evals
├── context-menu/          # 右键菜单 evals
└── eval-template.md       # 模板文件
```

## Evals 列表

### tray-plugin-spec (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | basic-plugin | 基础托盘插件创建 |
| eval-002 | flags-config | PluginFlags 配置 |
| eval-003 | proxy-interface | PluginProxyInterface 使用 |
| eval-004 | position-change | 任务栏位置变化处理 |

### quick-panel (3 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | quick-plugin | 快捷面板插件创建 |
| eval-002 | panel-size | 控件尺寸设置 |
| eval-003 | detail-page | 子页面显示 |

### message-protocol (3 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | message-handler | 消息处理实现 |
| eval-002 | support-flag | 插件可用性通知 |
| eval-003 | active-state | 激活状态报告 |

### context-menu (3 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | menu-data | 菜单数据格式 |
| eval-002 | checkable-menu | 可勾选菜单项 |
| eval-003 | open-control-center | 打开控制中心 |

## 总计

共 **13** 个 evals，覆盖 DDE 托盘插件开发的核心场景。
