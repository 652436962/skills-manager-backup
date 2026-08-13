# 核心概念

## 1. 概述

DConfig 涉及几个核心概念：appId、配置 id、meta 文件、override 文件等。理解这些概念是正确使用 DConfig 的基础。

**核心概念：**
- `appId` — 应用唯一标识
- 配置 id（name）— 配置描述文件标识
- meta 文件 — 配置元信息文件
- override 文件 — OEM 覆盖值文件

## 2. appId

应用程序唯一 ID。meta 文件安装到 `/usr/share/dsg/configs/{appId}/` 子目录下。

不指定 appId 时，`DConfig` 会通过 `DSGApplication::id()` 获取 appId，通常应优先使用这个默认行为。若无法使用默认 appId，再通过 `DConfig::create(appId, name, ...)` 显式指定。

## 配置 id（name）

配置描述文件的唯一标识，即 JSON 文件名（不含 `.json` 后缀）。

## meta 文件

安装包携带，描述配置项元信息和默认值。JSON 格式，`magic` 为 `"dsg.config.meta"`。

```json
{
    "magic": "dsg.config.meta",
    "version": "1.0",
    "contents": {
        "canExit": {
            "value": true,
            "permissions": "readwrite",
            "visibility": "private",
            "flags": [],
            "name": "Can Exit",
            "description": "Whether the application can exit"
        }
    }
}
```

### contents 中每个配置项属性

| 属性 | 说明 |
|------|------|
| `value` | 默认值，支持 bool、double、string、array、object |
| `permissions` | `readwrite` 可读可写 / 为空时，只读 |
| `visibility` | `private` 仅程序内部可见 / `public` 外部程序可见 |
| `flags` | 字符串数组，可选 `"nooverride"`、`"global"`、`"user-public"` |
| `name` | 显示名称（可选） |
| `description` | 描述文本（可选） |

### CMake 安装

```cmake
# APPID=应用id, BASE=根目录, FILES=配置文件列表
# 示例：/a 为子路径
dtk_add_config_meta_files(APPID dconfigexample BASE ./configs FILES ./configs/example.json ./configs/a/example.json)
```

## override 文件

可选，OEM/管理员用于覆盖 meta 文件中的 `value` 和 `permissions`。`magic` 为 `"dsg.config.override"`。

优先级从低到高：
1. `/usr/share/dsg/configs/overrides/{appId}/{配置id}/*.json`
2. `/usr/share/dsg/configs/overrides/{配置id}/*.json`
3. `/etc/dsg/configs/overrides/{appId}/{配置id}/*.json`（最高优先级）

配置项设置 `flags: ["nooverride"]` 后不可被 override 覆盖。

## subpath

配置文件子路径，格式以 `/` 开头，如 `"/feature/v2"`。查找 meta 文件时从子目录向上逐级查找，用于配置分层和优先级。

```cpp
auto *config = new DConfig("example", "/feature/v2", this);
```

## flags

| flag | 说明 |
|------|------|
| `"global"` | **系统级配置**，所有用户共享同一份数据，读写忽略用户身份。缓存存系统全局目录，不可写时降级到用户目录。典型场景：系统主题、默认语言 |
| `"nooverride"` | 该配置项不可被 override 文件覆盖 |
| `"user-public"` | 对用户级外部可见（DBus 访问权限控制） |

### global 详解（高频使用）

- **所有用户共享同一份数据**，任意用户的修改对所有用户生效
- 缓存存储在系统全局目录 `{DSG_APP_DATA}/configs/{appId}/`
- 全局目录不可写时自动降级到 `~/.config/dsg/configs/{appId}-fake-global/`

## 应用无关配置

不指定 appId 的通用配置，所有应用共享。使用 `DConfig::createGeneric()` 访问。

## 配置文件路径

以下是 DConfig 元数据和 override 的系统管理路径。应用代码不应手动拼接用户配置、缓存或持久化目录；只需要保持 appId、配置 name 和 meta 文件定义一致。

| 类型 | 路径 |
|------|------|
| 应用 meta 文件 | `/usr/share/dsg/configs/{appId}/{name}.json` |
| 应用无关 meta | `/usr/share/dsg/configs/{name}.json` |
| override 文件 | `/etc/dsg/configs/overrides/{appId}/{配置id}/*.json` |
