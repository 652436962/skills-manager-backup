# 贡献说明

[English](CONTRIBUTING_EN.md)

感谢你对 deepin Skills 的关注。提交改动前，请同时遵循 deepin 的[开发者贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers)和以下仓库约定。

## 修改已有 Skill

- 保持每个 Skill 位于 `skills/<skill-name>/`。
- 保留 `SKILL.md`、`agents/openai.yaml`、`references/` 和 `evals/` 的目录结构。
- `SKILL.md` 只描述 Skill 的触发范围、任务路由和必要工作流程；根据用户任务选择并读取对应的参考资料，避免加载无关内容。
- 将详细技术资料放在 `references/`，将验证场景放在 `evals/`，不要在单个 Skill 中添加 README 或其他面向仓库使用者的辅助文档。
- 更新功能或资料时，同步修改相关入口链接、`agents/openai.yaml` 元数据和评估用例。

## 新增 Skill

新增 Skill 前，先确认现有 Skill 是否已覆盖该任务领域。新 Skill 应使用小写连字符名称，并在 `skills/` 下建立以下结构：

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
└── evals/
```

- 新增 Skill 后，同步更新 `README.md` 和 `README_EN.md` 中的维护 Skill 列表。

## 提交改动

- 只提交与当前任务相关的改动，避免混入无关格式化或重构。
- 检查文档链接、目录结构和示例是否与实际内容一致。
- 为新增或明显变更的能力补充相应的评估用例。
