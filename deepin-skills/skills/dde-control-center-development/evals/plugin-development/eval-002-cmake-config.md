# Eval: CMake 配置

## 任务

编写控制中心插件的 CMakeLists.txt：
1. 项目名 "myplugin"
2. 依赖 Dtk6::Core、Dtk6::Widget
3. 安装到正确路径

## 验证要点

- [ ] cmake_minimum_required(VERSION 3.16)
- [ ] find_package(Dtk6 REQUIRED COMPONENTS Core Widget)
- [ ] install(TARGETS myplugin LIBRARY DESTINATION lib/dde-control-center/plugins)
