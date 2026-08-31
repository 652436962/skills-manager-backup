# 版本文件（CHANGELOG）规范

> 每个程序/项目在根目录维护一个版本文件（`CHANGELOG.md`），逐版本记录修改内容，
> 并与 git commit 一一对应，形成"版本号 ↔ 修改记录 ↔ 代码状态"的可追溯闭环。

## 1、文件与位置

- 项目根目录维护 `CHANGELOG.md`（版本记录文件），与 README、协议文档并列
- 固件工程中若存在版本宏文件（如 `version.h`），其中版本号必须与 CHANGELOG 最新条目一致
- 版本号格式沿用固件版本号规范：`V主.次.修订[.编译号]`

## 2、条目格式（参考）

```markdown
## [V1.3.2] - 2026-08-27 (265e20c)
```

- `[V1.3.2]`：版本号，V 大写，十进制，遵循固件版本号规范
- `2026-08-27`：发版日期，ISO 8601（`YYYY-MM-DD`）
- `(265e20c)`：该版本对应 git commit 的短哈希（7 位，`git rev-parse --short HEAD` 获取）

## 3、修改记录分组

按类别记录本版本改动，保持阅读一致：

| 分组 | 含义 | 是否影响版本号 |
|---|---|---|
| Added | 新增功能 | 次版本 |
| Changed | 行为/接口变更 | 视兼容性：不兼容→主版本；兼容→次版本 |
| Fixed | bug 修复 | 修订号 |
| Removed | 移除功能 | 视兼容性 |

> 每个分组条目一句话描述，指向具体模块/命令/字段，便于定位代码。

## 4、git 关联约定

- 每次发版流程：代码改动全部 commit → 获取短哈希 → 写入 CHANGELOG 正式条目 → 打 git tag → 推送
- tag 命名与版本号一一对应：`V1.3.2`（团队如约定小写也可统一为 `v1.3.2`，但 CHANGELOG 内版本号保持大写 V）
- 查看某版本改了什么：`git log --oneline <上一版本tag>..<当前版本tag>`
- 通过 `git tag -n` / `git describe` 可快速核对现场固件与代码版本是否一致

## 5、维护工作流

1. **日常**：功能改动或修复时，在 CHANGELOG 顶部的"Unreleased（未发布）"区登记
2. **发版前**：按变更影响确定新版本号（决策表见 `versioning-spec.md` 第四节）
3. **发版时**：commit 并取短哈希 → 将 Unreleased 区改写为正式条目 `## [Vx.y.z] - 日期 (短哈希)` → 打同名 tag → 推送远端
4. **校验**：版本号变化必须在 CHANGELOG 中有对应条目；CHANGELOG 无记录禁止变更版本号

## 6、示例

```markdown
# CHANGELOG

## [V1.4.0] - 2026-08-31 (e8f3a11)
### Added
- 上报 JSON 新增电量字段 battery
### Changed
- 通信协议升级至 2.1（向后兼容）

## [V1.3.2] - 2026-08-27 (265e20c)
### Fixed
- 修复 485 掉线后不自动重连的问题

## [V1.3.1] - 2026-08-20 (9f4a1b2)
### Added
- 新增读取版本信息命令 0x05

## [V1.3.0] - 2026-08-10 (7c2e9d0)
### Changed
- 配置文件结构变更，ConfigVersion 10 → 11（含迁移逻辑）
```

## 7、常用 git 命令

```bash
git rev-parse --short HEAD              # 取当前短哈希（写 CHANGELOG 用）
git log --oneline V1.3.1..V1.3.2        # 查看 V1.3.1 → V1.3.2 之间的提交
git tag -n                              # 查看所有 tag 及附注
git describe --tags                      # 最近 tag + 距离提交数，定位现场固件版本
```
