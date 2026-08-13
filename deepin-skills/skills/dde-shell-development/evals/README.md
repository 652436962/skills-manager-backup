# dde-shell-development Evals

本目录包含 dde-shell 插件开发的验证测试用例，按 references 文档结构分类。

## 目录结构

```
evals/
├── plugin-development/    # 插件开发流程 evals
├── api/                   # C++ API 使用 evals
├── qml-api/              # QML API 使用 evals
├── layershell/           # LayerShell 窗口 evals
└── eval-template.md      # 模板文件
```

## Evals 列表

### plugin-development (6 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | pure-qml-applet | 纯 QML Applet 创建 |
| eval-002 | cpp-applet | 带 C++ 后端的 Applet |
| eval-003 | containment-plugin | Containment 容器插件 |
| eval-004 | panel-plugin | Panel 面板插件 |
| eval-005 | cmake-config | CMake 构建配置 |
| eval-006 | cross-plugin-communication | 跨插件通信 |

### api (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | dapplet-lifecycle | DApplet 生命周期 |
| eval-002 | dpluginloader | DPluginLoader 插件加载 |
| eval-003 | dappletdata | DAppletData 数据模型 |
| eval-004 | dpanel-windows | DPanel 窗口管理 |

### qml-api (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | appletitem | AppletItem QML 组件 |
| eval-002 | containmentitem | ContainmentItem QML 组件 |
| eval-003 | panel-popup | PanelPopup/PanelMenu 组件 |
| eval-004 | layershell | DLayerShellWindow QML 使用 |

### layershell (5 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | dock-panel | 底部 Dock 面板 |
| eval-002 | top-bar | 顶栏窗口 |
| eval-003 | sidebar | 侧栏窗口 |
| eval-004 | overlay | 浮动覆盖层 |
| eval-005 | cpp-usage | C++ LayerShell 使用 |

## 总计

共 **19** 个 evals，覆盖 dde-shell 插件开发的核心场景。
