# Contributing

[简体中文](CONTRIBUTING.md)

Thank you for contributing to deepin Skills. Follow the deepin [Contribution Guide for Developers](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers-en) together with the repository conventions below.

## Updating An Existing Skill

- Keep every skill under `skills/<skill-name>/`.
- Preserve the `SKILL.md`, `agents/openai.yaml`, `references/`, and `evals/` layout.
- Keep `SKILL.md` focused on trigger scope, task routing, and essential workflow. Select and read only the references relevant to the user's task to avoid loading unrelated content.
- Put detailed technical material in `references/` and evaluation scenarios in `evals/`. Do not add a README or other auxiliary documentation for repository users inside an individual skill.
- When changing capabilities or references, update related entry links, `agents/openai.yaml` metadata, and evaluation cases.

## Adding A Skill

Before adding a skill, confirm that an existing skill does not already cover the task domain. New skills use lowercase hyphenated names and must follow this layout:

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
└── evals/
```

- After adding a skill, update the maintained-skill lists in `README.md` and `README_EN.md`.

## Submitting Changes

- Submit only changes relevant to the task; avoid unrelated formatting or refactoring.
- Ensure documentation links, directory structure, and examples match the repository contents.
- Add appropriate evaluation cases for new or substantially changed capabilities.
