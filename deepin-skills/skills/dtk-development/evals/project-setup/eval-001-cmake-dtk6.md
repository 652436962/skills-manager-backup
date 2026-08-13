# Eval: CMake 配置 DTK6 依赖

## 任务

编写 CMakeLists.txt 配置 DTK6 依赖，要求：
1. 项目名 "myapp"
2. 依赖 Dtk6::Core、Dtk6::Gui、Dtk6::Widget
3. 链接到可执行目标

## 期望输出

CMakeLists.txt 应：
1. 使用 find_package 查找 DTK 组件
2. 使用 target_link_libraries 链接

## 验证要点

- [ ] find_package(Dtk6Core REQUIRED)
- [ ] find_package(Dtk6Gui REQUIRED)
- [ ] find_package(Dtk6Widget REQUIRED)
- [ ] target_link_libraries(myapp PRIVATE Dtk6::Core Dtk6::Gui Dtk6::Widget)
