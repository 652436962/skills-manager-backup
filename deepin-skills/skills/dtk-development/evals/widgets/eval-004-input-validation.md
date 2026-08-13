# Eval: 输入框验证

## 任务

创建一个带验证的输入框，要求：
1. 验证邮箱格式
2. 格式错误时显示警告消息
3. 格式正确时清除警告

## 期望输出

代码应：
1. 使用 DLineEdit
2. 使用 setAlert() 控制警告状态
3. 使用 showAlertMessage() 显示错误提示

## 验证要点

- [ ] #include <DLineEdit>
- [ ] edit->setAlert(true) 显示警告
- [ ] edit->showAlertMessage("邮箱格式不正确")
- [ ] edit->setAlert(false) 清除警告
