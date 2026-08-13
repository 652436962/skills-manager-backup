# Eval: 应用身份与翻译加载

## 任务

为 DTK 应用配置应用身份和中文翻译，要求：
1. `applicationName` 与可执行文件名一致
2. 在创建窗口前加载翻译
3. 翻译文件 basename 与 `applicationName` 一致
4. `px` 作为专业单位不进入翻译

## 验证要点

- [ ] 设置了与可执行文件一致的 `applicationName`
- [ ] `DApplication::loadTranslator()` 位于 UI 创建之前
- [ ] 未将应用显示名称、应用 ID 和单实例 key 混为一个值
- [ ] 使用 `QStringLiteral("px")`，而不是 `tr("px")`
