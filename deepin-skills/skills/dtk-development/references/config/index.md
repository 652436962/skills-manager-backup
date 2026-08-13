# 配置系统决策树

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- 应用配置/持久化存储
- 跨应用/跨进程配置共享
- 系统级配置/用户级配置
- 配置热加载/配置调试

**API 接口描述：**
- DConfig / DSettings
- dde-dconfig / dconfig2cpp

---

## 概述

DConfig 是 DDE 的配置持久化方案，支持跨应用配置共享、系统级/用户级配置分离、OEM 预置覆盖等特性。

## 相关项目

| 项目 | 仓库 | 说明 |
|------|------|------|
| dtkcore | [linuxdeepin/dtkcore](https://github.com/linuxdeepin/dtkcore) | DConfig 客户端 API、dconfig2cpp 工具 |
| dde-app-services | [linuxdeepin/dde-app-services](https://github.com/linuxdeepin/dde-app-services) | dde-dconfig-daemon 服务、dde-dconfig CLI |

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 了解核心概念（appId/meta/override/flags） | [concepts.md](concepts.md) |
| C++ 中使用 DConfig（含 dconfig2cpp） | [dconfig-cpp.md](dconfig-cpp.md) |
| DBus 方式操作配置 | [dconfig-dbus.md](dconfig-dbus.md) |
| 调试、热加载、缓存路径 | [dconfig-debug.md](dconfig-debug.md) |
