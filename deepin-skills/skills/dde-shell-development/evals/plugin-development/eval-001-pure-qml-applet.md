# Eval: 创建纯 QML Applet

## 任务

用户想创建一个简单的天气显示插件，只需要在托盘区显示当前温度，不需要 C++ 后端。

指导用户创建纯 QML Applet 插件。

## 期望输出

回答应：
1. 展示 metadata.json 配置
2. 展示 main.qml 文件内容
3. 展示 CMakeLists.txt 配置（使用 ds_install_package）
4. 说明 AppletItem 的使用

## 验证要点

- [ ] metadata.json 包含 Plugin.Id、Plugin.Version、Plugin.Url、Plugin.Parent
- [ ] main.qml 使用 AppletItem 作为根元素
- [ ] CMakeLists.txt 使用 ds_install_package(PACKAGE <id>) 无 TARGET
- [ ] 说明 QML 中通过 Applet.pluginId 访问插件 ID
