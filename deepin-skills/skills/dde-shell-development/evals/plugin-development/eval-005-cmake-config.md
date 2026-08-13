# Eval: 配置 CMake 构建

## 任务

用户有一个 dde-shell 插件项目，需要配置 CMake 构建和翻译。

指导用户正确配置 CMakeLists.txt。

## 期望输出

回答应：
1. 展示 find_package 和 target_link_libraries
2. 展示 ds_install_package 用法
3. 展示 ds_handle_package_translation 用法
4. 说明安装路径

## 验证要点

- [ ] find_package(DDEShell REQUIRED)
- [ ] target_link_libraries(... PRIVATE Dde::Shell)
- [ ] ds_install_package(PACKAGE <id> TARGET <libname>)
- [ ] ds_handle_package_translation(PACKAGE <id>)
- [ ] 说明安装路径：/usr/share/dde-shell/<id>/ 和 /usr/lib/dde-shell/plugins/
