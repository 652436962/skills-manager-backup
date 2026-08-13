# Eval: 图标系统架构

## 任务

理解 DTK 图标系统的架构：
1. 说明 dci 图标的特点和优势
2. 解释 DDciIcon 和 DDciIconPlayer 的关系
3. 说明 DIconTheme 的统一查找入口

## 期望输出

回答应：
1. 描述三种图标类型的适用场景
2. 说明 dci 图标的主题感知机制
3. 解释图标动画的播放方式

## 验证要点

- [ ] dci 图标：主题感知、支持动画、矢量格式
- [ ] builtin 图标：内置资源、无需额外文件
- [ ] icon theme 图标：XDG 标准、系统主题集成
- [ ] DDciIconPlayer 用于播放 dci 图标动画
- [ ] DIconTheme 提供统一查找入口
