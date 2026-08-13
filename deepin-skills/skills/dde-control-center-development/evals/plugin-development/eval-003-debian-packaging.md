# Eval: Debian 打包

## 任务

为控制中心插件创建 Debian 打包文件：
1. debian/control 文件
2. debian/rules 文件
3. debian/install 文件

## 验证要点

- [ ] Section: utils
- [ ] Depends 包含 dde-control-center
- [ ] debian/rules 使用 dh $@ --parallel
