# Eval: dccData 为 undefined 问题

## 任务

用户在插件 QML 中访问 `dccData` 属性，但运行时显示 `undefined`。帮助用户排查问题。

## 期望输出

回答应：
1. 解释 `dccData` 的加载时机
2. 列出可能的原因（工厂类未正确注册、CMake 链接问题）
3. 给出验证方法

## 验证要点

- [ ] 提到 `{Name}.qml` 加载时 C++ 插件可能未加载
- [ ] 提到检查 `DCC_FACTORY_CLASS` 宏是否正确调用
- [ ] 提到检查 `.moc` 包含是否正确
- [ ] 提到检查 CMake 是否链接了 `Dde::Control-Center`
