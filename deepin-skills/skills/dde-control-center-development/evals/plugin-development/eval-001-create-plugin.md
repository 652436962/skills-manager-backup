# Eval: 创建控制中心插件

## 任务

创建一个适用于 deepin/UOS v25 的简单控制中心插件：
1. CMakeLists.txt 配置
2. 插件类继承控制中心基类
3. JSON 元数据文件

## 期望输出

代码应：
1. 使用 `find_package(DdeControlCenter REQUIRED)` 和 `Dde::Control-Center`
2. 使用 `DCC_FACTORY_CLASS` 注册数据对象
3. 使用 `dcc_install_plugin` 安装插件并提供 v25 元数据

## 验证要点

- [ ] `find_package(DdeControlCenter REQUIRED)`
- [ ] 链接 `Dde::Control-Center`
- [ ] 使用 `DCC_FACTORY_CLASS(MyPluginModule)`，并包含生成的 moc 文件
- [ ] 使用 `dcc_install_plugin(NAME myplugin TARGET myplugin)`
- [ ] `qml/metadata.json` 是合法 JSON，且 `Version` 为 `1.0`

## 参考

参见 [插件开发](../../references/plugin-development.md) 了解控制中心插件开发流程。
