---
title: "摘要-openspec-schema-yaml"
type: source
tags: [来源, OpenSpec, Schema, 工作流DSL]
sources: [raw/01-articles/openspec-schema/schema.yaml]
last_updated: 2026-06-18
---

## 核心摘要

OpenSpec Workflow DSL Schema定义文件,定义opsx命令/阶段/门禁/产物约束。核心命令:explore(自由探索无产物要求无人工门禁)/propose(Spec+Design一体化生成有人工门禁)/apply(编码实现SHA256校验前置产物)/verify(评审+测试有人工门禁)/archive(提PR+资料整理)。门禁类型:none(无门禁自动流转)/sha256_check(自动校验SHA256哈希不一致则中止)/manual_review(人工评审门禁)。产物目录结构包含openspec/schemas/spec-driven-nio/templates目录。

## 命令定义

### explore命令
- **alias**: `/opsx:explore`
- **description**: 自由探索,无产物要求,无人工门禁
- **stage**: explore
- **produces**: [] (无产物)
- **gate**: none (无门禁)
- **superpowers**: [] (不使用Superpowers技能)

### propose命令
- **alias**: `/opsx:propose`
- **description**: Spec + Design 一体化生成,有人工门禁
- **stage**: propose
- **produces**: proposal.md, spec.md, design.md, tasks.md
- **gate**: manual_review (人工评审门禁)
- **superpowers**: brainstorming (注意:propose阶段使用brainstorming辅助生成,但explore阶段不使用)
- **constraints**: 所有产物必须通过SHA256锁定;design.md必须包含测试策略

### apply命令
- **alias**: `/opsx:apply`
- **description**: 编码实现
- **stage**: apply
- **produces**: plan.md, implementation_code
- **gate**: sha256_check (启动时校验前置产物哈希)
- **superpowers**: using-git-worktrees, writing-plans, subagent-driven-development, test-driven-development
- **dependencies**: /opsx:propose (强依赖propose阶段产物)
- **constraints**: plan.md中的任务必须拆分为2-5分钟可完成的小任务;必须遵循RED-GREEN-REFACTOR循环

### verify命令
- **alias**: `/opsx:verify`
- **description**: 评审 + 测试,有人工门禁
- **stage**: verify
- **produces**: review_report, test_report
- **gate**: manual_review (人工评审门禁)
- **superpowers**: requesting-code-review
- **dependencies**: /opsx:apply

### archive命令
- **alias**: `/opsx:archive`
- **description**: 提PR + 资料整理
- **stage**: archive
- **produces**: pull_request, archive_summary
- **gate**: none (无门禁)
- **superpowers**: finishing-a-development-branch
- **dependencies**: /opsx:verify

## 门禁类型

### none
- **description**: 无门禁,自动流转

### sha256_check
- **description**: 自动校验前置产物SHA256哈希,不一致则中止并报警
- **action**:
  1. 读取 .opsx/lock/{stage}.sha256
  2. 重新计算当前产物SHA256
  3. 比对:一致→继续;不一致→中止,输出差异文件列表,强制重新走人工确认

### manual_review
- **description**: 人工评审门禁
- **action**:
  1. Agent生成产物
  2. 自动计算SHA256并写入.opsx/lock/
  3. 提交人工评审
  4. 评审通过→进入下一阶段
  5. 评审不通过→填写结构化修改意见,Agent迭代重生成

## 产物目录结构

```
{project_root}/
├── openspec/
│   ├── schemas/
│   │   └── spec-driven-nio/
│   │       ├── schema.yaml
│   │       └── templates/
│   │           ├── proposal.md
│   │           ├── spec.md
│   │           ├── design.md
│   │           ├── tasks.md
│   │           └── plan.md
│   ├── specs/              # 当前系统的行为描述
│   │   └── <domain>/
│   │       └── spec.md
│   ├── changes/            # 拟议的修改
│   │   └── <change-name>/
│   │       ├── proposal.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── tasks.md
│   │       ├── plan.md
│   │       └── specs/      # Delta规约
│   │           └── <domain>/
│   │               └── spec.md
│   └── config.yaml
├── .opsx/
│   ├── lock/               # SHA256锁定文件
│   │   ├── propose.sha256
│   │   ├── apply.sha256
│   │   └── verify.sha256
│   └── state/              # 当前阶段状态
│       └── current.json
└── docs/
    └── superpowers/        # Superpowers产物
        ├── specs/
        ├── plans/
        └── reviews/
```

## 关联连接
- [[OpenSpec]] — 规约驱动开发框架
- [[摘要-openspec-superpowers-collaboration]] — OpenSpec+Superpowers协同
- [[摘要-openspec-superpowers-nio-workflow]] — NIO定制版