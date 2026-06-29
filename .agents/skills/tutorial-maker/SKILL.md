---
name: tutorial-maker
description: 当用户说"写教程"、"整理成教程"、"搭教程工程"、"做成书"、"输出PDF教程"、"写一本"、"出本书"时触发。将碎片化学习记录转化为结构化教程，搭建 Markdown → PDF 自动化管线。
---

# Tutorial Maker —— 教程创作方法论

## 核心理念

> 好的教程不是"写出来的"，是**做出来的副产品**。

## 流程

1. 理解用户要写的主题范围和现有素材
2. 规划章节目录（每章 5 分钟可读完，独立完整）
3. 按五阶段方法论推进
4. 搭建 Markdown → PDF 工程管线
5. 配置 CI 自动发布

## 五阶段闭环

```
精输入 → 学模式 → 动手做 → 费曼输出 → 工程化发布
```

### 阶段 1：精输入 —— Follow Builders, Not Influencers

- 不读二手评测，直接打开原始代码、配置文件一行一行读
- 锁定亲手做产品的实践者，而不是自媒体
- 判断标准：这个作者自己有没有落地过产品？
- 全部案例来自公开开源仓库，零成本可复现

### 阶段 2：学模式 —— 拆解 → 验证 → 踩坑 → 修正

- 把参考代码库的设计模式逐一拆解
- 在自己的场景里验证，不是复制粘贴
- **踩坑是最高价值内容**——记录"我以为会怎样 → 实际发生了什么 → 为什么 → 怎么修"
- 每条结论都来自亲自跑过、改过、验证过的代码

### 阶段 3：动手做 —— 内容是实践副产品

- **不要为了写教程而写教程**。教程应该是搭建工作流、研究能力边界过程中自然产出的记录
- 真实踩坑经验比凭空编造的教程更有说服力
- 先在实践中把东西做出来，再反刍成文字

### 阶段 4：费曼输出 —— 隐性知识显性化

- 不写"官方文档的翻译"，写"我学到的、做到的、踩过坑的"
- 每章回答一个具体问题，5 分钟读完
- 标准结构：问题 → 为什么重要 → 怎么做 → 真实案例 → 常见坑点
- **MVP 驱动**：60 分完整可用就上线，先写 3 章核心内容发布，看反馈再扩展

### 阶段 5：工程化 —— Markdown → PDF 管线

#### 目录结构
```
tutorial/
├── chapters/              # 章节 markdown（每个独立完整）
├── appendices/            # 附录
├── images/                # 配图
├── README.md              # 英文（GitHub 默认展示）
├── README.zh-CN.md        # 中文
├── style.css              # PDF 排版样式
├── build-pdf.sh           # 一键构建 PDF
├── print-to-pdf.js        # Puppeteer HTML → PDF
├── add-outline.py         # 自动生成 PDF 目录书签
├── find-chapter-pages.py  # 章节页码自动定位
├── package.json           # 仅依赖 puppeteer
└── .github/workflows/     # CI 自动发布 PDF 到 Release
```

#### PDF 管线关键点
- 章章独立文件：方便按需跳读和协作编辑
- CSS `page-break-before: always` 每章另起一页
- 封面独立 HTML 渲染，不参与正文页码计算
- 目录书签用 `pdftotext` + 搜索定位章节页码，`pypdf` 写入 PDF outline
- 代码块 `white-space: pre-wrap` 防止长行溢出
- GitHub Actions → 构建 PDF → 自动上传 Release

#### 技术栈
- Markdown 拼接 → 单个 HTML
- Puppeteer 渲染 HTML → PDF
- Python（pypdf + pdftotext）→ PDF 目录书签
- GitHub Actions → 自动化发布

## 关键原则

1. **不被动假学习**：每章都能停下来动手试，读完前几章就够开干
2. **持续产出 > 一次性完美**：先上线 60 分版本，迭代到 90 分
3. **开放生态优先**：全部案例来自公开开源仓库，零成本复现
4. **内容即副产品**：不是"写教程项目"，是实践的自然记录
5. **双语 README**：README.md 英文 + README.zh-CN.md 中文，GitHub 首页可切换

## 常见坑点

见 [gotchas.md](gotchas.md)
