---
title: "Mymat 实现细节规范"
type: synthesis
tags: [Mymat, 实现规范, Shell脚本, 状态机, Guard, SkillFile]
created: 2026-06-06
updated: 2026-06-06
sources: []
related:
  - wiki/syntheses/mymat-design
  - wiki/entities/OpenSpec
  - wiki/entities/Superpowers
  - wiki/entities/Gstack
---

> **本文档用途**：面向 Mymat 开发者的实现细节规范。阅读前请先阅读 [[mymat-design]]（系统设计方案）。本文档不重复设计决策，只补充"如何实现"。

---

## 一、完整文件结构

### 1.1 项目安装目录（`~/.mymat/` 或项目内 `.mymat/`）

```
{project_root}/
├── CLAUDE.md                          ← 已有文件，追加 Mymat 加载指令
├── .mymat/
│   ├── skills/                        ← Mymat skill 文件（安装时创建）
│   │   ├── mymat-core.md              ← 主入口 + 意图识别逻辑
│   │   ├── mymat-product.md           ← Phase P skill
│   │   ├── mymat-spec.md              ← Phase S skill
│   │   ├── mymat-design.md            ← Phase D skill
│   │   ├── mymat-build.md             ← Phase B skill
│   │   ├── mymat-verify.md            ← Phase Vt+Vp skill
│   │   └── mymat-release.md           ← Phase R skill
│   ├── scripts/                       ← Guard + 工具脚本（安装时创建）
│   │   ├── mymat-state.sh             ← 统一 state.json 读写
│   │   ├── mymat-guard-product.sh     ← P 阶段产物校验
│   │   ├── mymat-guard-spec.sh        ← S 阶段产物校验
│   │   ├── mymat-guard-spec-integrity.sh ← SHA256 全程完整性校验
│   │   ├── mymat-guard-build.sh       ← 每个 Build task 产物校验
│   │   ├── mymat-guard-verify.sh      ← Vt+Vp 产物校验
│   │   ├── mymat-guard-release.sh     ← R 阶段产物校验
│   │   └── mymat-workflow-detect.sh   ← diff 分析推荐工作流
│   ├── features/                      ← 每个 feature 的运行时状态
│   │   └── {feature_id}/
│   │       ├── state.json
│   │       ├── spec-graph.json
│   │       ├── trigger-log.txt            ← Skill 触发日志（由 guard-spec.sh PASS 后写入）
│   │       ├── warn-log.txt               ← 测试对齐警告日志（由 guard-build.sh AC 关键词检查写入）
│   │       ├── handoff/
│   │       │   └── design-context.json   ← Design→Build 交接包（由 guard-spec.sh HCG-2 后生成）
│   │       └── snapshots/
│   │           ├── hcg-1.json
│   │           ├── hcg-2.json
│   │           ├── hcg-3.json
│   │           └── hcg-4.json
│   └── config.json                    ← 项目级配置
└── openspec/                          ← OpenSpec 工具目录（已有）
```

### 1.2 Feature ID 命名规范

```
feat-{YYYYMMDD}-{slug}

示例：
feat-20260606-login-refactor
feat-20260606-payment-integration
feat-20260607-dashboard-v2
```

同一天同一 slug 时自动追加序号：`feat-20260606-login-refactor-2`

---

## 二、config.json 结构

```json
{
  "version": "1.0",
  "project_name": "my-project",
  "platform": "node",
  "test_command": "npm test",
  "test_file_pattern": "src/__tests__/**/*.test.ts",
  "scripts_dir": ".mymat/scripts",
  "skills_dir": ".mymat/skills",
  "openspec_dir": "openspec",
  "gstack_dir": ".gstack",
  "token_tracking": true,
  "auto_workflow_detect": true,
  "installed_at": "2026-06-06T10:00:00Z",
  "mymat_version": "0.1.0"
}
```

**platform 枚举**：`node` / `python` / `java` / `go` / `rust` / `generic`
platform 决定 `test_command` 的默认值和 `test_file_pattern`。

---

## 三、CLAUDE.md 集成方式

安装时追加到 CLAUDE.md 末尾：

```markdown
---

## Mymat 工作流系统

Mymat 整合 OpenSpec + Superpowers + Gstack，管理从产品想法到 PR 创建的全链路流程。

### 加载规则

当用户输入任何 `/mymat` 开头的命令，或描述涉及"功能开发"、"新 feature"、"继续上次"时：

1. 立即读取 `.mymat/skills/mymat-core.md`
2. 按其中的意图识别逻辑路由到对应阶段 skill 文件
3. **禁止**在未执行 guard 脚本校验前声称某阶段已完成

### 强制规则

- 每次阶段推进前必须运行对应 guard 脚本（通过 Bash 工具）
- guard 脚本 exit code 非 0 时，立即停止并展示错误信息，不得继续推进
- HCG 展示后必须等待用户明确确认，不得自行跳过
- state.json 的写入只通过 `mymat-state.sh` 完成，不得直接编辑
- **禁止仿写 Skill**：执行 `/opsx:propose`、`brainstorming` 等外部 Skill 时，必须读取该 Skill 文件真实触发，不得根据描述自行生成格式相似的产物文件。

### 会话恢复规则

新对话开始时，如果用户说"继续"、"resume"或输入 `/mymat`：

1. 运行 `bash .mymat/scripts/mymat-state.sh active` 获取活跃 feature 列表
2. 读取对应 state.json，展示当前进度
3. 从 `current_phase` + `last_task_id` 定位继续点
```

---

## 四、mymat-state.sh 实现规范

### 4.1 命令接口

```bash
# 读取
bash .mymat/scripts/mymat-state.sh read <feature_id> [<json_path>]
# 写入单个字段
bash .mymat/scripts/mymat-state.sh write <feature_id> <json_path> <value>
# 创建新 feature state.json
bash .mymat/scripts/mymat-state.sh init <feature_id> <workflow> <title>
# 列出活跃 feature（status != done && status != aborted）
bash .mymat/scripts/mymat-state.sh active
# 创建 HCG 快照
bash .mymat/scripts/mymat-state.sh snapshot <feature_id> <hcg_num> <question>
# 回滚到某个 HCG 快照
bash .mymat/scripts/mymat-state.sh rollback <feature_id> <hcg_num>
# 追加 completed_tasks 数组
bash .mymat/scripts/mymat-state.sh task-done <feature_id> <task_id>
# 更新 metrics
bash .mymat/scripts/mymat-state.sh metrics <feature_id> <phase> <field> <value>
```

### 4.2 实现伪代码

```bash
#!/usr/bin/env bash
set -euo pipefail

MYMAT_DIR=".mymat"
FEATURES_DIR="$MYMAT_DIR/features"

cmd="$1"
feature_id="${2:-}"

state_file() {
  echo "$FEATURES_DIR/$feature_id/state.json"
}

validate_field() {
  local path="$1"
  local value="$2"
  case "$path" in
    .current_phase)
      echo "$value" | grep -qE '"(product|spec|design|build|verify_tech|verify_product|release)"' \
        || { echo "SCHEMA_ERROR: invalid value $value for .current_phase" >&2; exit 1; }
      ;;
    .current_phase_status)
      echo "$value" | grep -qE '"(not_started|in_progress|done|parked|blocked|aborted|failed)"' \
        || { echo "SCHEMA_ERROR: invalid value $value for .current_phase_status" >&2; exit 1; }
      ;;
    .workflow)
      echo "$value" | grep -qE '"(full|quick|micro|prototype)"' \
        || { echo "SCHEMA_ERROR: invalid value $value for .workflow" >&2; exit 1; }
      ;;
    .isolation.strategy)
      echo "$value" | grep -qE '"(branch|worktree|none)"' \
        || { echo "SCHEMA_ERROR: invalid value $value for .isolation.strategy" >&2; exit 1; }
      ;;
  esac
}

case "$cmd" in
  read)
    json_path="${3:-.}"  # 默认读取整个文件
    file=$(state_file)
    [[ -f "$file" ]] || { echo "ERROR: state.json not found for $feature_id" >&2; exit 1; }
    if command -v jq &>/dev/null; then
      jq "$json_path" "$file"
    else
      # 降级：python3 fallback
      python3 -c "import json,sys; d=json.load(open('$file')); print(json.dumps(d))"
    fi
    ;;

  write)
    json_path="$3"
    value="$4"
    file=$(state_file)
    validate_field "$json_path" "$value"
    # 使用 jq 更新字段，保留其余内容
    tmp=$(mktemp)
    jq "$json_path = $value" "$file" > "$tmp" && mv "$tmp" "$file"
    # 更新 updated_at
    jq ".updated_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$file" > "$tmp" && mv "$tmp" "$file"
    ;;

  init)
    workflow="$3"
    title="$4"
    mkdir -p "$FEATURES_DIR/$feature_id/snapshots"
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    cat > "$FEATURES_DIR/$feature_id/state.json" <<EOF
{
  "version": "1.0",
  "feature_id": "$feature_id",
  "feature_title": "$title",
  "workflow": "$workflow",
  "current_phase": "product",
  "current_phase_status": "not_started",
  "created_at": "$ts",
  "updated_at": "$ts",
  "isolation": null,
  "phases": {
    "product": { "status": "not_started", "outputs": {}, "metrics": null },
    "spec": { "status": "not_started", "outputs": {}, "metrics": null },
    "design": { "status": "not_started", "outputs": {}, "metrics": null },
    "build": {
      "status": "not_started",
      "total_tasks": 0,
      "completed_tasks": [],
      "last_task_id": null,
      "last_task_title": null,
      "failed_task_id": null,
      "metrics": null
    },
    "verify_tech": { "status": "not_started", "outputs": {}, "metrics": null },
    "verify_product": { "status": "not_started", "outputs": {}, "metrics": null },
    "release": { "status": "not_started", "outputs": {}, "metrics": null }
  }
}
EOF
    echo "OK: initialized $feature_id"
    ;;

  active)
    # 遍历所有 feature 目录，过滤 status 不是 done/aborted 的
    find "$FEATURES_DIR" -name "state.json" | while read f; do
      s=$(jq -r '.current_phase_status // "unknown"' "$f")
      id=$(jq -r '.feature_id' "$f")
      phase=$(jq -r '.current_phase' "$f")
      title=$(jq -r '.feature_title' "$f")
      if [[ "$s" != "done" && "$s" != "aborted" ]]; then
        echo "$id | $phase | $s | $title"
      fi
    done
    ;;

  snapshot)
    hcg_num="$3"
    question="$4"
    file=$(state_file)
    snap_file="$FEATURES_DIR/$feature_id/snapshots/hcg-${hcg_num}.json"
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    state_content=$(cat "$file")
    spec_content="null"
    spec_graph="$FEATURES_DIR/$feature_id/spec-graph.json"
    [[ -f "$spec_graph" ]] && spec_content=$(cat "$spec_graph")
    cat > "$snap_file" <<EOF
{
  "snapshot_id": "hcg-$hcg_num",
  "captured_at": "$ts",
  "hcg_question": "$question",
  "state": $state_content,
  "spec_graph": $spec_content
}
EOF
    echo "OK: snapshot hcg-$hcg_num created"
    ;;

  rollback)
    hcg_num="$3"
    snap_file="$FEATURES_DIR/$feature_id/snapshots/hcg-${hcg_num}.json"
    [[ -f "$snap_file" ]] || { echo "ERROR: snapshot hcg-$hcg_num not found" >&2; exit 1; }
    # 从快照还原 state.json 和 spec-graph.json
    jq '.state' "$snap_file" > "$(state_file)"
    spec_content=$(jq '.spec_graph' "$snap_file")
    if [[ "$spec_content" != "null" ]]; then
      echo "$spec_content" > "$FEATURES_DIR/$feature_id/spec-graph.json"
    fi
    echo "OK: rolled back to hcg-$hcg_num"
    ;;

  task-done)
    task_id="$3"
    file=$(state_file)
    tmp=$(mktemp)
    # 追加到 completed_tasks 数组（去重）
    jq ".phases.build.completed_tasks |= (. + [\"$task_id\"] | unique)" "$file" > "$tmp" && mv "$tmp" "$file"
    jq ".phases.build.last_task_id = \"$task_id\"" "$file" > "$tmp" && mv "$tmp" "$file"
    jq ".updated_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$file" > "$tmp" && mv "$tmp" "$file"
    echo "OK: task $task_id marked done"
    ;;

  metrics)
    phase="$3"
    field="$4"
    value="$5"
    file=$(state_file)
    tmp=$(mktemp)
    jq ".phases.$phase.metrics.$field = $value" "$file" > "$tmp" && mv "$tmp" "$file"
    ;;

  validate)
    file=$(state_file)
    [[ -f "$file" ]] || { echo "ERROR: state.json not found for $feature_id" >&2; exit 1; }
    schema_errors=()
    for required_field in ".version" ".feature_id" ".workflow" ".current_phase" ".current_phase_status"; do
      v=$(jq -r "$required_field // empty" "$file" 2>/dev/null)
      [[ -z "$v" ]] && schema_errors+=("MISSING: $required_field")
    done
    if [[ ${#schema_errors[@]} -eq 0 ]]; then
      echo "VALID: state.json schema OK for $feature_id"
    else
      echo "INVALID: ${#schema_errors[@]} schema error(s):"
      for e in "${schema_errors[@]}"; do echo "  - $e"; done
      exit 1
    fi
    ;;

  *)
    echo "ERROR: unknown command $cmd" >&2
    exit 1
    ;;
esac
```

**依赖**：`jq`（必须）+ `python3`（jq 不存在时降级）。安装时 `/mymat:init` 检测依赖，缺失则提示安装。

---

## 五、Guard 脚本实现规范

### 5.1 mymat-guard-product.sh

```bash
#!/usr/bin/env bash
# 校验 P 阶段产物，放行 HCG-1
set -euo pipefail

FEATURE_ID="$1"
FEATURES_DIR=".mymat/features/$FEATURE_ID"

errors=()

# P-01：office-hours 报告存在
OFFICE_HOURS="$FEATURES_DIR/product/office-hours.md"
[[ -f "$OFFICE_HOURS" ]] || errors+=("MISSING: office-hours report at $OFFICE_HOURS")

# 校验 YC 六问均有回答（检测六个关键 heading）
if [[ -f "$OFFICE_HOURS" ]]; then
  for keyword in "问题" "用户" "竞品" "风险" "指标" "下一步"; do
    grep -qi "$keyword" "$OFFICE_HOURS" || errors+=("INCOMPLETE: office-hours missing section '$keyword'")
  done
fi

# P-02：autoplan 报告存在
AUTOPLAN="$FEATURES_DIR/product/autoplan.md"
[[ -f "$AUTOPLAN" ]] || errors+=("MISSING: autoplan report at $AUTOPLAN")

# 输出结果
if [[ ${#errors[@]} -eq 0 ]]; then
  echo "PASS: Product phase artifacts verified. HCG-1 unblocked."
  exit 0
else
  echo "FAIL: Product phase has ${#errors[@]} error(s):"
  for e in "${errors[@]}"; do echo "  - $e"; done
  exit 1
fi
```

### 5.2 mymat-guard-spec.sh

```bash
#!/usr/bin/env bash
# 校验 S 阶段产物，初始化 spec-graph.json，放行 HCG-2
set -euo pipefail

FEATURE_ID="$1"
OPENSPEC_DIR="${2:-openspec}"
FEATURES_DIR=".mymat/features/$FEATURE_ID"

errors=()

# 查找 OpenSpec 最新变更目录（按时间倒序取第一个）
CHANGE_DIR=$(find "$OPENSPEC_DIR/changes" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort -r | head -1)
[[ -n "$CHANGE_DIR" ]] || { echo "FAIL: no changes directory found under $OPENSPEC_DIR/changes"; exit 1; }

# 校验四件套
for artifact in proposal.md specs.md design.md tasks.md; do
  [[ -f "$CHANGE_DIR/$artifact" ]] || errors+=("MISSING: $CHANGE_DIR/$artifact")
done

# 校验 tasks.md 非空（至少包含一个任务行）
if [[ -f "$CHANGE_DIR/tasks.md" ]]; then
  task_count=$(grep -c "^- \[" "$CHANGE_DIR/tasks.md" 2>/dev/null || echo "0")
  [[ "$task_count" -gt 0 ]] || errors+=("EMPTY: tasks.md has no task items (expected lines matching '- [' )")
fi

# 输出结果（先报错再退出）
if [[ ${#errors[@]} -gt 0 ]]; then
  echo "FAIL: Spec phase has ${#errors[@]} error(s):"
  for e in "${errors[@]}"; do echo "  - $e"; done
  exit 1
fi

# 初始化 spec-graph.json（SHA256 锁定）
SPEC_GRAPH="$FEATURES_DIR/spec-graph.json"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

compute_sha256() {
  if command -v sha256sum &>/dev/null; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

cat > "$SPEC_GRAPH" <<EOF
{
  "created_at": "$TS",
  "nodes": {
    "openspec_specs": {
      "path": "$CHANGE_DIR/specs.md",
      "sha256": "$(compute_sha256 "$CHANGE_DIR/specs.md")",
      "role": "requirements_truth",
      "frozen_after_phase": "spec",
      "immutable": true
    },
    "openspec_tasks": {
      "path": "$CHANGE_DIR/tasks.md",
      "sha256": "$(compute_sha256 "$CHANGE_DIR/tasks.md")",
      "role": "task_list",
      "frozen_after_phase": "spec",
      "immutable": true
    },
    "openspec_proposal": {
      "path": "$CHANGE_DIR/proposal.md",
      "sha256": "$(compute_sha256 "$CHANGE_DIR/proposal.md")",
      "role": "product_rationale",
      "frozen_after_phase": "spec",
      "immutable": false
    },
    "openspec_design": {
      "path": "$CHANGE_DIR/design.md",
      "sha256": "$(compute_sha256 "$CHANGE_DIR/design.md")",
      "role": "implementation_approach",
      "frozen_after_phase": "spec",
      "immutable": false
    }
  },
  "integrity_violations": [],
  "last_checked_at": "$TS"
}
EOF

echo "PASS: Spec phase artifacts verified. spec-graph.json initialized. HCG-2 unblocked."

# 校验 Skill 触发标记（层一：产物 frontmatter 声明）
for artifact_path in "$CHANGE_DIR/specs.md" "$CHANGE_DIR/tasks.md"; do
  if [[ -f "$artifact_path" ]] && ! grep -q "generated_by:" "$artifact_path" 2>/dev/null; then
    echo "WARN: MISSING_TRIGGER: $artifact_path lacks 'generated_by' frontmatter. Ensure /opsx:propose was truly triggered."
  fi
done

# 写入 trigger-log.txt（层二：触发日志）
TRIGGER_LOG="$FEATURES_DIR/trigger-log.txt"
echo "[MYMAT-TRIGGER] guard-spec PASS at $(date -u +%Y-%m-%dT%H:%M:%SZ) feature=$FEATURE_ID" >> "$TRIGGER_LOG"

# 生成 design-context.json（Handoff Context）
HANDOFF_DIR="$FEATURES_DIR/handoff"
HANDOFF_FILE="$HANDOFF_DIR/design-context.json"
mkdir -p "$HANDOFF_DIR"
SPECS_SHA=$(compute_sha256 "$CHANGE_DIR/specs.md")
TASKS_SHA=$(compute_sha256 "$CHANGE_DIR/tasks.md")
if command -v sha256sum &>/dev/null; then
  HANDOFF_HASH=$(printf '%s:%s:%s:%s' "$CHANGE_DIR/specs.md" "$SPECS_SHA" "$CHANGE_DIR/tasks.md" "$TASKS_SHA" | sha256sum | awk '{print $1}')
else
  HANDOFF_HASH=$(printf '%s:%s:%s:%s' "$CHANGE_DIR/specs.md" "$SPECS_SHA" "$CHANGE_DIR/tasks.md" "$TASKS_SHA" | shasum -a 256 | awk '{print $1}')
fi
cat > "$HANDOFF_FILE" <<EOF
{
  "generated_at": "$TS",
  "phase": "spec→build",
  "feature_id": "$FEATURE_ID",
  "inputs": {
    "specs": { "path": "$CHANGE_DIR/specs.md", "sha256": "$SPECS_SHA", "role": "requirements_truth" },
    "tasks": { "path": "$CHANGE_DIR/tasks.md", "sha256": "$TASKS_SHA", "role": "task_list" }
  },
  "handoff_hash": "$HANDOFF_HASH"
}
EOF
echo "OK: design-context.json generated at $HANDOFF_FILE"
exit 0
```

### 5.3 mymat-guard-spec-integrity.sh

```bash
#!/usr/bin/env bash
# 全程完整性校验，每次阶段推进前运行
set -euo pipefail

FEATURE_ID="$1"
FEATURES_DIR=".mymat/features/$FEATURE_ID"
SPEC_GRAPH="$FEATURES_DIR/spec-graph.json"

[[ -f "$SPEC_GRAPH" ]] || { echo "SKIP: spec-graph.json not yet initialized (pre-spec phase)"; exit 0; }

violations=()
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

compute_sha256() {
  if command -v sha256sum &>/dev/null; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

# 读取所有 immutable=true 节点
immutable_nodes=$(jq -r '.nodes | to_entries[] | select(.value.immutable == true) | .key' "$SPEC_GRAPH")

while IFS= read -r node_key; do
  path=$(jq -r ".nodes.$node_key.path" "$SPEC_GRAPH")
  expected_sha=$(jq -r ".nodes.$node_key.sha256" "$SPEC_GRAPH")

  if [[ ! -f "$path" ]]; then
    violations+=("{\"node\": \"$node_key\", \"type\": \"file_deleted\", \"path\": \"$path\"}")
    continue
  fi

  actual_sha=$(compute_sha256 "$path")
  if [[ "$actual_sha" != "$expected_sha" ]]; then
    violations+=("{\"node\": \"$node_key\", \"type\": \"sha256_mismatch\", \"path\": \"$path\", \"expected\": \"$expected_sha\", \"actual\": \"$actual_sha\"}")
  fi
done <<< "$immutable_nodes"

# 更新 last_checked_at 和 integrity_violations
tmp=$(mktemp)
if [[ ${#violations[@]} -eq 0 ]]; then
  jq ".last_checked_at = \"$TS\" | .integrity_violations = []" "$SPEC_GRAPH" > "$tmp" && mv "$tmp" "$SPEC_GRAPH"
  echo "PASS: Spec integrity verified (all SHA256 match)."
  exit 0
else
  # 构造 violations JSON 数组
  violations_json="[$(IFS=,; echo "${violations[*]}")]"
  jq ".last_checked_at = \"$TS\" | .integrity_violations = $violations_json" "$SPEC_GRAPH" > "$tmp" && mv "$tmp" "$SPEC_GRAPH"
  echo "FAIL: Spec integrity violated! ${#violations[@]} immutable file(s) were modified after HCG-2:"
  for v in "${violations[@]}"; do
    echo "  - $(echo "$v" | jq -r '"[\(.type)] \(.node): \(.path)"')"
  done
  echo ""
  echo "ACTION REQUIRED: Spec files are frozen after HCG-2. To change requirements:"
  echo "  1. Run /mymat:rollback hcg-2 to revert to pre-spec state"
  echo "  2. Re-run /mymat:spec to regenerate specs"
  echo "  3. Re-confirm HCG-2"
  exit 1
fi
```

### 5.4 mymat-guard-build.sh

```bash
#!/usr/bin/env bash
# 校验单个 Build task 的三件套产物
set -euo pipefail

FEATURE_ID="$1"
TASK_ID="$2"           # 例：B-003
TASK_TITLE="$3"        # 例：重构 TokenService.refresh
MODULE_NAME="$4"       # 例：TokenService（用于定位测试文件）
PLATFORM="${5:-node}"

errors=()
test_files=""
impl_files=""

# 根据 platform 确定测试命令和文件模式
case "$PLATFORM" in
  node)
    TEST_CMD="npm test -- --testPathPattern=${MODULE_NAME}"
    ;;
  python)
    TEST_CMD="python -m pytest tests/test_${MODULE_NAME}"
    ;;
  java)
    TEST_CMD="mvn test -Dtest=${MODULE_NAME}Test"
    ;;
  *)
    TEST_CMD=""
    ;;
esac

# 0. 首任务：检查分支隔离策略已设置
COMPLETED_COUNT=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" \
  ".phases.build.completed_tasks | length" 2>/dev/null | tr -d '"')
if [[ "${COMPLETED_COUNT:-0}" -eq 0 ]]; then
  ISOLATION_STRATEGY=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" \
    ".isolation.strategy" 2>/dev/null | tr -d '"')
  if [[ -z "$ISOLATION_STRATEGY" || "$ISOLATION_STRATEGY" == "null" ]]; then
    echo "HARD STOP: isolation strategy not set. Run /mymat:build to select branch/worktree/none before starting tasks."
    exit 1
  fi
  BRANCH_NAME=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" \
    ".isolation.branch_name" 2>/dev/null | tr -d '"')
  if [[ "$ISOLATION_STRATEGY" == "branch" ]]; then
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    if [[ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]]; then
      echo "INFO: switching to branch $BRANCH_NAME ..."
      git checkout "$BRANCH_NAME" 2>/dev/null || git checkout -b "$BRANCH_NAME"
    fi
  elif [[ "$ISOLATION_STRATEGY" == "none" ]]; then
    CODE_EXTS='\.(ts|js|py|java|go|rs|cpp|c|cs)$'
    changed_code_files=$(git diff --name-only HEAD 2>/dev/null | grep -E "$CODE_EXTS" || true)
    code_changes=$(printf '%s\n' "$changed_code_files" | sed '/^$/d' | wc -l | tr -d ' ')
    if [[ "$code_changes" -gt 0 ]]; then
      echo "HARD STOP: isolation=none but $code_changes code file(s) changed. Use 'branch' or 'worktree' for code changes."
      exit 1
    fi
  fi
fi

# 1. 检查测试文件存在
case "$PLATFORM" in
  node)
    test_files=$(find src/__tests__ -type f \( -name "${MODULE_NAME}*.test.ts" -o -name "${MODULE_NAME}*.test.js" \) 2>/dev/null | head -1)
    ;;
  python)
    test_files=$(find tests -type f -name "test_${MODULE_NAME}*.py" 2>/dev/null | head -1)
    ;;
  java)
    test_files=$(find src/test -type f -name "${MODULE_NAME}Test.java" 2>/dev/null | head -1)
    ;;
esac
if [[ -n "$TEST_CMD" && -z "$test_files" ]]; then
  errors+=("MISSING: test file for module '$MODULE_NAME' and task $TASK_ID ($TASK_TITLE)")
fi

# 2. 运行测试并检查通过
if [[ -n "$TEST_CMD" && ${#errors[@]} -eq 0 ]]; then
  if ! eval "$TEST_CMD" > /tmp/mymat-test-output.txt 2>&1; then
    errors+=("FAILING: tests failed for $TASK_ID. Output:")
    while IFS= read -r line; do errors+=("  $line"); done < /tmp/mymat-test-output.txt
  fi
fi

# 3. 检查实现文件存在
case "$PLATFORM" in
  node)
    impl_files=$(find src -type f \( -name "${MODULE_NAME}*.ts" -o -name "${MODULE_NAME}*.js" \) -not -name "*.test.*" 2>/dev/null | head -1)
    ;;
  python)
    impl_files=$(find . -type f -name "${MODULE_NAME}*.py" -not -path "./tests/*" 2>/dev/null | head -1)
    ;;
  java)
    impl_files=$(find src/main -type f -name "${MODULE_NAME}.java" 2>/dev/null | head -1)
    ;;
esac
if [[ -n "$TEST_CMD" ]]; then
  [[ -n "$impl_files" ]] || errors+=("MISSING: implementation file for module '$MODULE_NAME'")
fi

# 测试描述 AC 关键词对齐检查（warn-only，不阻塞 Build）
HANDOFF_FILE=".mymat/features/$FEATURE_ID/handoff/design-context.json"
if [[ -f "$HANDOFF_FILE" && -n "$test_files" ]]; then
  TASKS_PATH=$(jq -r '.inputs.tasks.path' "$HANDOFF_FILE" 2>/dev/null)
  if [[ -f "$TASKS_PATH" ]]; then
    TASK_KEYWORDS=$(jq -r ".tasks[] | select(.id==\"$TASK_ID\") | .acceptance_criteria[]?" \
      "$TASKS_PATH" 2>/dev/null | tr '[:upper:]' '[:lower:]' | tr -s ' ' '\n' | \
      grep -v '^.\{1,3\}$' | head -10)
    if [[ -n "$TASK_KEYWORDS" ]]; then
      TEST_DESCRIPTIONS=$(grep -hE "^\s*(it|test|describe)\(" "$test_files" 2>/dev/null | \
        tr '[:upper:]' '[:lower:]')
      MATCHED=0
      while IFS= read -r keyword; do
        echo "$TEST_DESCRIPTIONS" | grep -q "$keyword" 2>/dev/null && MATCHED=1 && break
      done <<< "$TASK_KEYWORDS"
      if [[ $MATCHED -eq 0 ]]; then
        echo "WARN: test descriptions in $test_files don't reference AC keywords for $TASK_ID."
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] AC_MISMATCH task=$TASK_ID file=$test_files" \
          >> ".mymat/features/$FEATURE_ID/warn-log.txt"
      fi
    fi
  fi
fi

if [[ ${#errors[@]} -eq 0 ]]; then
  echo "PASS: Build task $TASK_ID ($TASK_TITLE) artifacts verified."
  # 写入 task-done 状态
  bash .mymat/scripts/mymat-state.sh task-done "$FEATURE_ID" "$TASK_ID"
  exit 0
else
  echo "FAIL: Build task $TASK_ID has ${#errors[@]} error(s):"
  for e in "${errors[@]}"; do echo "  $e"; done
  # 写入 failed_task_id
  bash .mymat/scripts/mymat-state.sh write "$FEATURE_ID" ".phases.build.failed_task_id" "\"$TASK_ID\""
  exit 1
fi
```

### 5.5 mymat-guard-verify.sh

```bash
#!/usr/bin/env bash
# 校验 Vt + Vp 阶段全部产物，放行 HCG-3
set -euo pipefail

FEATURE_ID="$1"
FEATURES_DIR=".mymat/features/$FEATURE_ID"

errors=()

# Vt-01：verification report
VT_REPORT="$FEATURES_DIR/verify_tech/verification-report.md"
[[ -f "$VT_REPORT" ]] || errors+=("MISSING: verification report at $VT_REPORT")

# Vt-02：spec alignment report
VT_SPEC="$FEATURES_DIR/verify_tech/spec-alignment-report.md"
[[ -f "$VT_SPEC" ]] || errors+=("MISSING: spec alignment report at $VT_SPEC")
if [[ -f "$VT_SPEC" ]]; then
  grep -qi "PASS\|通过\|aligned" "$VT_SPEC" || errors+=("FAIL_CONTENT: spec alignment report does not contain PASS status")
fi

# Vt-03：review report
VT_REVIEW="$FEATURES_DIR/verify_tech/review-report.md"
[[ -f "$VT_REVIEW" ]] || errors+=("MISSING: review report at $VT_REVIEW")

# Vp-01：security audit（/cso 报告）
VP_SECURITY="$FEATURES_DIR/verify_product/security-audit.md"
[[ -f "$VP_SECURITY" ]] || errors+=("MISSING: security audit report at $VP_SECURITY")
if [[ -f "$VP_SECURITY" ]]; then
  # 检查是否所有 findings 均已标记 handled
  open_issues=$(grep -ciE "^- \[ \]|OPEN|UNRESOLVED" "$VP_SECURITY" 2>/dev/null || echo "0")
  [[ "$open_issues" -eq 0 ]] || errors+=("OPEN_ISSUES: security audit has $open_issues unresolved finding(s)")
fi

# Vp-02：E2E 报告（/qa 报告）
VP_E2E="$FEATURES_DIR/verify_product/e2e-report.md"
[[ -f "$VP_E2E" ]] || errors+=("MISSING: E2E test report at $VP_E2E")
if [[ -f "$VP_E2E" ]]; then
  grep -qi "PASS\|passed\|通过" "$VP_E2E" || errors+=("FAIL_CONTENT: E2E report does not show PASS status")
  grep -qi "FAIL\|failed\|失败" "$VP_E2E" && errors+=("FAIL_CONTENT: E2E report contains failures")
fi

if [[ ${#errors[@]} -eq 0 ]]; then
  echo "PASS: All Vt+Vp artifacts verified. HCG-3 unblocked."
  exit 0
else
  echo "FAIL: Verify phase has ${#errors[@]} error(s):"
  for e in "${errors[@]}"; do echo "  - $e"; done
  exit 1
fi
```

### 5.6 mymat-guard-release.sh

```bash
#!/usr/bin/env bash
# 校验 Release 阶段产物，标记 feature 完成
set -euo pipefail

FEATURE_ID="$1"
FEATURES_DIR=".mymat/features/$FEATURE_ID"

errors=()

# R-01：PR URL 存在（/ship 应将 PR URL 写入 state.json）
PR_URL=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" ".phases.release.outputs.pr_url" 2>/dev/null | tr -d '"')
[[ -n "$PR_URL" && "$PR_URL" != "null" ]] || errors+=("MISSING: PR URL not recorded in state.json. Ensure /ship completed successfully.")

# R-02：CHANGELOG 有更新（检查最近修改时间）
if [[ -f "CHANGELOG.md" ]]; then
  last_modified=$(find CHANGELOG.md -newer "$FEATURES_DIR/state.json" 2>/dev/null | wc -l)
  [[ "$last_modified" -gt 0 ]] || errors+=("STALE: CHANGELOG.md was not updated after feature started")
fi

# R-03：openspec archive 标记
ARCHIVE_PATH=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" ".phases.release.outputs.archive_path" 2>/dev/null | tr -d '"')
[[ -n "$ARCHIVE_PATH" && "$ARCHIVE_PATH" != "null" ]] || errors+=("MISSING: archive path not recorded. Ensure /opsx:archive completed.")

if [[ ${#errors[@]} -eq 0 ]]; then
  # 标记 feature 完成
  bash .mymat/scripts/mymat-state.sh write "$FEATURE_ID" ".current_phase_status" '"done"'
  bash .mymat/scripts/mymat-state.sh write "$FEATURE_ID" ".phases.release.status" '"done"'
  echo "PASS: Release artifacts verified. Feature $FEATURE_ID marked DONE."
  exit 0
else
  echo "FAIL: Release phase has ${#errors[@]} error(s):"
  for e in "${errors[@]}"; do echo "  - $e"; done
  exit 1
fi
```

### 5.7 mymat-workflow-detect.sh

```bash
#!/usr/bin/env bash
# 分析 git diff 范围，推荐工作流类型
set -euo pipefail

BASE_BRANCH="${1:-main}"

# 获取变更文件列表
changed_files=$(git diff --name-only "$BASE_BRANCH"...HEAD 2>/dev/null || git status --short | awk '{print $2}')
file_count=$(printf '%s\n' "$changed_files" | sed '/^$/d' | wc -l | tr -d ' ')

# 判断是否影响核心模块（可按项目定制）
CORE_PATTERNS="src/core|src/auth|src/payment|src/api|package.json|tsconfig"
touches_core=$(printf '%s\n' "$changed_files" | grep -E "$CORE_PATTERNS" 2>/dev/null | wc -l | tr -d ' ')

# 判断是否是原型分支
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
is_proto=$(printf '%s\n' "$current_branch" | grep -E "^(proto|spike)/" 2>/dev/null | wc -l | tr -d ' ')

# 推荐逻辑
if [[ "$is_proto" -gt 0 ]]; then
  recommendation="prototype"
  reason="Branch name matches proto/ or spike/ pattern"
elif [[ "$file_count" -lt 3 ]]; then
  recommendation="micro"
  reason="Small change: $file_count file(s) modified"
elif [[ "$file_count" -lt 6 && "$touches_core" -eq 0 ]]; then
  recommendation="quick"
  reason="Medium change: $file_count file(s), no core modules affected"
else
  recommendation="full"
  reason="Large or core change: $file_count file(s), $touches_core core module(s) affected"
fi

echo "RECOMMENDATION: $recommendation"
echo "REASON: $reason"
echo "STATS: files=$file_count core_touches=$touches_core branch=$current_branch"
```

---

## 六、Skill 文件实现规范

### 6.1 mymat-core.md（主入口）

```markdown
# Mymat 核心入口 Skill

## 角色

你是 Mymat 工作流协调者。负责意图识别、状态读取、阶段路由。

## 激活条件

当用户输入 `/mymat` 或任何 `/mymat:` 命令时加载本文件。

## 五层意图识别漏斗

执行顺序：依次判断，第一个匹配即路由，不继续后续层。

### 层1：显式命令路由

| 用户输入                  | 动作                                             |
| ------------------------- | ------------------------------------------------ |
| `/mymat:init`             | 读取 mymat-install.md，执行初始化                |
| `/mymat:new`              | 引导创建新 feature，收集标题和工作流类型         |
| `/mymat:list`             | 执行 `bash .mymat/scripts/mymat-state.sh active` |
| `/mymat:product`          | 读取 mymat-product.md，执行 P 阶段               |
| `/mymat:spec`             | 读取 mymat-spec.md，执行 S 阶段                  |
| `/mymat:design`           | 读取 mymat-design.md，执行 D 阶段                |
| `/mymat:build`            | 读取 mymat-build.md，执行 B 阶段（从头）         |
| `/mymat:build {TASK_ID}`  | 读取 mymat-build.md，从指定 task 恢复            |
| `/mymat:verify`           | 读取 mymat-verify.md，执行 Vt+Vp 阶段            |
| `/mymat:release`          | 读取 mymat-release.md，执行 R 阶段               |
| `/mymat:status`           | 读取 state.json 并展示格式化状态面板             |
| `/mymat:park`             | 执行停放：写入 parked 状态                       |
| `/mymat:resume`           | 从 parked 恢复，定位到 last_task_id              |
| `/mymat:retry`            | 重试 failed_task_id 的任务                       |
| `/mymat:skip`             | 跳过当前 optional 任务（需用户再次确认）         |
| `/mymat:rollback hcg-{N}` | 执行 `mymat-state.sh rollback`                   |
| `/mymat:full`             | 设置 workflow=full，创建/更新 feature            |
| `/mymat:quick`            | 设置 workflow=quick                              |
| `/mymat:micro`            | 设置 workflow=micro                              |
| `/mymat:prototype`        | 设置 workflow=prototype                          |

### 层2：活跃 feature 定位

执行 `bash .mymat/scripts/mymat-state.sh active`：

- 0 个 → 提示用户 `/mymat:new` 创建新 feature
- 1 个 → 自动选中，进入层3
- N 个 → 展示列表，格式如下，等待用户选择：
  当前有 {N} 个进行中的 feature：
  1. feat-20260606-login-refactor | build | in_progress
  2. feat-20260606-payment-v2 | spec | parked
     请输入编号选择，或输入 feature_id：

### 层3：状态读取与展示

读取 state.json 的 `current_phase` 和 `current_phase_status`：

- `in_progress` → 展示进度，询问"继续 [当前阶段]？"
- `parked` → "上次停放于 [phase] [task]，是否恢复？"
- `blocked` → 展示 failed task，提示 `/mymat:retry` 或 `/mymat:skip`
- `not_started` → 直接推进到对应阶段 skill

### 层4：工作流推荐

若是全新 feature（state.json 刚初始化）：
执行 `bash .mymat/scripts/mymat-workflow-detect.sh`
展示推荐结果，询问"使用 [recommendation] 工作流？(Y/n)"
n → 展示四种选项等待选择

### 层5：阶段自动推进

无歧义时直接推进；有多个可能路径时阻塞等待用户确认。

## HCG 展示格式

每次 HCG 使用以下格式：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 HCG-{N} {门禁名称}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Feature: {feature_title}
阶段: {current_phase} → {next_phase}

已完成：
✅ {P-01 产物名称}
✅ {P-02 产物名称}

确认问题：{hcg_question}

⚠️ 此操作不可逆。确认后将锁定 {被冻结的内容}。

确认请回复 YES，拒绝请回复 NO（将保持当前阶段）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## /mymat:status 展示格式

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mymat Status: {feature_title}
Feature ID: {feature_id}
Workflow: {workflow}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P Product ✅ done (28 min | out: 8.2K chars)
S Spec ✅ done (35 min | out: 11.5K chars)
D Design ✅ done (15 min | out: 6.8K chars)
B Build 🔄 3/8 done (running | out: 24.6K chars so far)
└─ last: B-003 重构 TokenService.refresh
Vt VerifyTech ⏳ pending
Vp VerifyProduct ⏳ pending
R Release ⏳ pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next: /mymat:build B-004 to continue
```

### 6.2 mymat-build.md（B 阶段 skill 关键片段）

```markdown
# Mymat Build Phase Skill

## 执行前置条件

0. **读取交接包**：读取 `.mymat/features/{FEATURE_ID}/handoff/design-context.json`
   - 从 `inputs.specs.path` 读取 specs.md（**不得**使用对话记忆中的内容）
   - 从 `inputs.tasks.path` 读取 tasks.md（**不得**使用对话记忆中的内容）
   - 如果文件不存在 → HARD STOP：需重新执行 /mymat:spec
1. 运行 `bash .mymat/scripts/mymat-guard-spec-integrity.sh {FEATURE_ID}`
   - exit 1 则立即停止，展示 spec 违规信息
2. 读取 state.json 获取 `phases.build`：
   - `completed_tasks`：已完成的 task ID 列表
   - `last_task_id`：上次断点
   - `total_tasks`：总任务数（从 tasks.md 计数）

## Build 前置：隔离策略确认

读取 state.json `.isolation.strategy`：

- `null` → **HARD STOP**，展示选择菜单：
```

请选择代码隔离方式：

1. branch — 创建独立分支（推荐：标准开发）
2. worktree — 创建独立工作目录（多 feature 并发）
3. none — 无代码变更（仅文档/配置，guard 将校验无代码文件变更）

```
用户选择后执行对应 git 操作，写入 `.isolation` 字段。

- 已设置 → 确认当前在正确分支，输出 `INFO: isolation = {strategy}:{branch_name}`

## Build 循环逻辑

对每个 task T in tasks.md（按顺序）：
IF T.id in completed*tasks → 跳过（打印 "⏩ skip B-00N [title] (already done)"）
ELSE：
**[强制 AC 锚定 — 每 task 必做]**：从 tasks.md（经由 design-context.json）定位当前 task，提取 `acceptance_criteria` 列表，粘贴到响应顶部作为上下文锚点。后续 B-01 写测试时，`describe()`/`it()` 描述必须直接引用验收条件语言。降级：design-context.json 不存在或 tasks.md 非 JSON 时，跳过锚点并在 warn-log 记录 `NO_AC task={id}`。
执行 B-01（TDD）：- 提示"写单元测试 for [task_title]" - 要求 Superpowers test-driven-development skill 的完整流程：
* 先写测试，命名为 {Module}.test.ts
\_ 测试必须先失败（Red）\* 不得提前写实现代码
执行 B-02（实现）：- 写最小实现使测试通过 - 遵循 Superpowers subagent-driven-development 规范
执行 B-03（验证）：- 调用 `bash .mymat/scripts/mymat-guard-build.sh {FEATURE_ID} {TASK_ID} "{TITLE}" {MODULE} {PLATFORM}` - exit 1：停止，展示错误，等待用户 /mymat:retry 或 /mymat:park - exit 0：继续下一个 task

## 任务断点展示

每个 task 完成时，展示：
✅ B-{N} {title} — done (tests passing)
Progress: {N}/{total} tasks
Snapshot: last_task_id = B-{N}

## 全部完成时

展示：
🎉 All {N} Build tasks completed.
Next step: /mymat:verify

自动调用 `mymat-state.sh write {FEATURE_ID} ".phases.build.status" '"done"'`
```

### 6.3 mymat-product.md（P 阶段 skill）

````markdown
# Mymat Product Phase Skill

## 角色

你是 Mymat Product 阶段协调者。负责引导用户完成产品方向验证，产出可被 HCG-1 校验的两份报告。

## 激活条件

由 mymat-core.md 路由到本文件。加载前 mymat-core.md 已完成 feature 定位和 state.json 读取。

## 前置检查

1. 读取 state.json：`current_phase` 应为 `product`，`current_phase_status` 应为 `not_started` 或 `in_progress`
2. 写入 `phases.product.metrics.started_at`（若尚未写入）：
   `bash .mymat/scripts/mymat-state.sh metrics {FEATURE_ID} product started_at "\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\""`
3. 写入状态 `in_progress`：
   `bash .mymat/scripts/mymat-state.sh write {FEATURE_ID} .current_phase_status '"in_progress"'`

## 执行步骤

### P-01：/office-hours

触发 Gstack `/office-hours`（**必须真实触发 skill，不得仿写**）。

产物保存路径：`.mymat/features/{FEATURE_ID}/product/office-hours.md`

产物必须包含 YC 六问的完整回答章节（问题、用户、竞品、风险、指标、下一步），否则 guard 将报告 INCOMPLETE。

### P-02：/autoplan

触发 Gstack `/autoplan`（**必须真实触发 skill，不得仿写**）。

产物保存路径：`.mymat/features/{FEATURE_ID}/product/autoplan.md`

产物应包含 CEO 视角、工程视角、设计视角三个评审维度。

### Guard 执行

```bash
bash .mymat/scripts/mymat-guard-product.sh {FEATURE_ID}
```
````

- exit 0 → 展示 HCG-1，等待用户确认
- exit 1 → 展示错误，等待修复

### HCG-1 展示

运行 `mymat-state.sh snapshot {FEATURE_ID} 1 "产品方向已验证，进入需求规约阶段？"`，然后展示标准 HCG 面板。

用户 YES → 写入 `phases.product.status = done`，`current_phase = spec`，`current_phase_status = not_started`；推进到 mymat-spec.md
用户 NO → 保持 product 阶段，询问需要修改哪个报告

````

### 6.4 mymat-spec.md（S 阶段 skill）

```markdown
# Mymat Spec Phase Skill

## 角色

你是 Mymat Spec 阶段协调者。负责协调 OpenSpec 工具生成四件套规约，并在 HCG-2 前校验并锁定规约完整性。

## 激活条件

由 mymat-core.md 路由到本文件。当前 `current_phase = spec`。

## 前置检查

1. 运行 `bash .mymat/scripts/mymat-guard-spec-integrity.sh {FEATURE_ID}`（若 spec-graph.json 已存在，防重复修改）
2. 写入 `phases.spec.metrics.started_at`（若尚未写入）
3. 写入状态 `in_progress`

## 执行步骤

### S-01（可选）：/opsx:explore

若用户需要需求讨论或技术预研，触发 OpenSpec `/opsx:explore`（**必须真实触发 skill**）。

用户明确跳过时，直接进入 S-02。

### S-02（核心）：/opsx:propose

触发 OpenSpec `/opsx:propose`（**必须真实触发 skill，不得根据描述仿写四件套文件**）。

产物路径由 OpenSpec 管理（`openspec/changes/{timestamp}/`）。生成 `proposal.md`、`specs.md`、`design.md`、`tasks.md` 四件套。

### Guard 执行

```bash
bash .mymat/scripts/mymat-guard-spec.sh {FEATURE_ID} openspec
````

- exit 0 → guard 已自动完成：
  - 生成 `spec-graph.json`（SHA256 锁定四件套）
  - 生成 `handoff/design-context.json`
  - 写入 `trigger-log.txt`
  - 展示 HCG-2
- exit 1 → 展示错误，等待修复（常见：四件套缺失、tasks.md 无任务行、frontmatter 缺 `generated_by`）

### HCG-2 展示

运行 `mymat-state.sh snapshot {FEATURE_ID} 2 "需求范围确认，开始设计？（确认后 specs 将冻结，不可直接修改）"`，展示 HCG 面板，特别说明：**确认后 specs.md 和 tasks.md 进入冻结状态，后续修改需回滚到 HCG-1。**

用户 YES → 写入 `phases.spec.status = done`，`current_phase = design`，`current_phase_status = not_started`；推进到 mymat-design.md
用户 NO → 询问是需要重新运行 `/opsx:propose` 还是回滚到 HCG-1

````

### 6.5 mymat-design.md（D 阶段 skill）

```markdown
# Mymat Design Phase Skill

## 角色

你是 Mymat Design 阶段协调者。负责协调 Superpowers 工具精炼需求，生成可执行的非冻结设计计划，并验证设计计划与 specs.md / tasks.md 的一致性。

## 激活条件

由 mymat-core.md 路由到本文件。当前 `current_phase = design`。

## 前置检查

1. 运行 `bash .mymat/scripts/mymat-guard-spec-integrity.sh {FEATURE_ID}` — 确保 specs 未被篡改
   exit 1 立即停止，展示 integrity 违规信息
2. 从 `handoff/design-context.json` 读取 `inputs.specs.path`，提示 AI 加载 specs.md 作为本阶段输入
3. 写入 `phases.design.metrics.started_at`（若尚未写入）
4. 写入状态 `in_progress`

## 执行步骤

### D-01：/brainstorming

触发 Superpowers `brainstorming` skill（**必须真实触发 skill，不得仿写**）。

输入：specs.md（从 design-context.json 读取路径，从磁盘加载）
产物：边界分析文档 + 方案选型 + 风险清单

**约束**：brainstorming 产物只描述实现方案和风险，不得增加或修改需求——需求唯一真相源是 specs.md（单向事实链）。

### D-02：/writing-plans

触发 Superpowers `writing-plans` skill（**必须真实触发 skill，不得仿写**）。

输入：specs.md + D-01 产物
产物：2–5 分钟粒度的微任务计划（每个 task 含 id、title、acceptance_criteria 数组），作为非冻结设计计划留存。

产物默认写入 `docs/plan-{feature_id}.md` 或 `.mymat/features/{feature_id}/handoff/build-plan.json`，**不得直接更新 `openspec/changes/{timestamp}/tasks.md`**。

**重要**：tasks.md 在 HCG-2 时 `immutable=true` 被锁定。D 阶段如果发现 tasks.md 粒度不足，必须停止推进并回滚到 HCG-1 重新走 S 阶段，由 OpenSpec 重新生成 tasks 后再进入 HCG-2。

> 设计建议：D 阶段的 writing-plans 输出用于指导 Build 执行和断点恢复；D-02 只需将设计计划留存，不触碰 frozen OpenSpec 产物。

### Guard 执行（进入 B 阶段前）

```bash
bash .mymat/scripts/mymat-guard-spec-integrity.sh {FEATURE_ID}
````

PASS → 展示摘要，更新 state 推进到 Build

### 阶段完成

写入 `phases.design.status = done`，`current_phase = build`，`current_phase_status = not_started`

展示：
✅ Design phase complete.

- D-01: brainstorming 产物已生成
- D-02: 微任务计划已生成（{N} tasks）
- Spec integrity: PASS

Next step: /mymat:build

````

### 6.6 mymat-verify.md（Vt+Vp 阶段 skill）

```markdown
# Mymat Verify Phase Skill

## 角色

你是 Mymat Verify 阶段协调者。负责协调 Vt（技术验证）和 Vp（产品验收）两个子阶段，在 HCG-3 前完成三层技术验收和端到端产品验收。

## 激活条件

由 mymat-core.md 路由到本文件。当前 `current_phase = verify_tech` 或 `verify_product`。

## 前置检查

1. 运行 `bash .mymat/scripts/mymat-guard-spec-integrity.sh {FEATURE_ID}` — 确保 specs 未被篡改
2. 确认 `phases.build.status == done`，否则提示先完成 Build 阶段
3. 写入 `phases.verify_tech.metrics.started_at`（若尚未写入）

---

## Vt：技术验证（三层验收）

### Vt-01：/verification-before-completion

触发 Superpowers `verification-before-completion` skill（**必须真实触发**）。

产物：技术完成度证据文档（所有 tasks 通过证明）
保存路径：`.mymat/features/{FEATURE_ID}/verify_tech/verification-report.md`

### Vt-02：/opsx:verify

触发 OpenSpec `/opsx:verify`（**必须真实触发 skill**）。

作用：逐条对照 specs.md 验证实现是否符合规约定义；读取 `warn-log.txt`，对含 `AC_MISMATCH` 记录的 task 做精确语义校验。
产物：规约对齐验证报告
保存路径：`.mymat/features/{FEATURE_ID}/verify_tech/spec-alignment-report.md`

报告末尾必须包含整体状态行（`PASS` / `FAIL`）。

### Vt-03：/review

触发 Gstack `/review`（**必须真实触发 skill**）。

作用：code review，发现 CI 能通过但生产可能爆炸的 bug。
产物：code review 报告
保存路径：`.mymat/features/{FEATURE_ID}/verify_tech/review-report.md`

---

## Vp：产品验收

### Vp-01：/cso

触发 Gstack `/cso`（**必须真实触发 skill**）。

作用：OWASP Top 10 + STRIDE 安全审计。
产物：安全审计报告
保存路径：`.mymat/features/{FEATURE_ID}/verify_product/security-audit.md`

所有 findings 必须被标记 handled，否则 guard 会检测到 OPEN_ISSUES。

### Vp-02：/qa

触发 Gstack `/qa`（**必须真实触发 skill**）。

作用：Playwright Chromium 真实浏览器 E2E 测试。
产物：E2E 测试报告
保存路径：`.mymat/features/{FEATURE_ID}/verify_product/e2e-report.md`

报告必须包含 PASS 状态标记，不得含有 FAIL / failed 字样。

---

## Guard 执行

```bash
bash .mymat/scripts/mymat-guard-verify.sh {FEATURE_ID}
````

- exit 0 → 展示 HCG-3，等待用户确认
- exit 1 → 展示错误，等待修复

## HCG-3 展示

运行 `mymat-state.sh snapshot {FEATURE_ID} 3 "验收通过，准备发布？"`，展示 HCG 面板，列出已通过的 6 项验收清单。

用户 YES → 写入 `phases.verify_tech.status = done`，`phases.verify_product.status = done`，`current_phase = release`，`current_phase_status = not_started`；推进到 mymat-release.md
用户 NO → 询问哪项验收结果有疑问，保持当前阶段

````

### 6.7 mymat-release.md（R 阶段 skill）

```markdown
# Mymat Release Phase Skill

## 角色

你是 Mymat Release 阶段协调者。负责执行 HCG-4（发布不可逆确认）、协调 Gstack `/ship` 和 OpenSpec `/opsx:archive`，完成 feature 完整生命周期。

## 激活条件

由 mymat-core.md 路由到本文件。当前 `current_phase = release`。

## 前置检查

1. 确认 `phases.verify_tech.status == done` 且 `phases.verify_product.status == done`，否则提示先完成 Verify 阶段
2. 写入 `phases.release.metrics.started_at`（若尚未写入）

## HCG-4（发布确认 — 优先展示）

**在执行任何发布操作前**，必须先展示 HCG-4。

运行 `mymat-state.sh snapshot {FEATURE_ID} 4 "发布是不可逆操作，确认执行？"`，展示 HCG 面板，特别说明：

> ⚠️ 此操作不可逆。/ship 将推送 PR 到远端仓库，/opsx:archive 将合入主规范。请确认所有验收报告均已通过后再继续。

用户 NO → 保持 release 阶段，返回 Verify 阶段确认单
用户 YES → 依次执行 R-01 和 R-02

## 执行步骤

### R-01：/ship

触发 Gstack `/ship`（**必须真实触发 skill，不得仿写**）。

作用：版本号升级 + CHANGELOG 更新 + git commit + PR 创建推送
产物：PR URL

PR URL 写入 state.json：
`bash .mymat/scripts/mymat-state.sh write {FEATURE_ID} ".phases.release.outputs.pr_url" "\"$PR_URL\""`

### R-02：/opsx:archive

触发 OpenSpec `/opsx:archive`（**必须真实触发 skill，不得仿写**）。

作用：将本 feature 的 delta spec 合入主规范，feature 生命周期结束。
产物：archive 路径

archive 路径写入 state.json：
`bash .mymat/scripts/mymat-state.sh write {FEATURE_ID} ".phases.release.outputs.archive_path" "\"$ARCHIVE_PATH\""`

## Guard 执行

```bash
bash .mymat/scripts/mymat-guard-release.sh {FEATURE_ID}
````

- exit 0 → feature 标记 DONE，展示完成摘要
- exit 1 → 展示错误（常见：PR URL 未记录、CHANGELOG 未更新、archive 路径未记录）

## 完成展示

🎉 Feature {FEATURE_ID} RELEASED

PR: {pr_url}
Archive: {archive_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total elapsed:
P {elapsed} min
S {elapsed} min
D {elapsed} min
B {elapsed} min
Vt {elapsed} min
Vp {elapsed} min
R {elapsed} min
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next: PR awaits human code review and merge approval.

**Mymat 边界止于此。** PR 合并、CI/CD 流水线、Staging/Production 部署由团队协作和自动化流程接管。

```

---

## 七、metrics 字段设计与可测量性

### 7.1 可测量性分类

| 字段              | 可测性      | 实现方式                                             | 说明                                         |
| ----------------- | ----------- | ---------------------------------------------------- | -------------------------------------------- |
| `started_at`      | ✅ 精确     | `date -u` 在阶段开始时写入                           | guard 脚本调用时                             |
| `completed_at`    | ✅ 精确     | `date -u` 在 guard PASS 分支写入                     | 完全可靠                                     |
| `elapsed_seconds` | ✅ 精确     | `completed_at - started_at`                          | **最接近真实成本的可测指标**                 |
| `output_chars`    | ✅ 可测     | `wc -c` 计算本阶段生成的所有产物文件                 | 代表 AI 输出了多少内容                       |
| `input_chars`     | ⚠️ 不完整   | `wc -c` 计算本阶段输入文件（specs/tasks/skill 文件） | 只是静态文件大小，不包含对话历史和系统提示词 |
| `api_usage`       | ❌ 不可获取 | 预留字段，当前设为 `null`                            | Claude Code 不暴露 token 消耗给 shell        |

### 7.2 无法获取的部分

Claude Code 的实际 token 消耗由四部分组成，全部在 shell 层面**不可见**：

```

实际 token 消耗 = 系统 prompt + CLAUDE.md 注入 + 对话历史（每轮累积）+ 思考/推理 token（extended thinking） ← 完全不透明 + 工具调用往返（Bash/Read file）+ 生成的产物文件内容（输出部分） ← 唯一可测

````

`input_chars` 的局限性：即便把本阶段所有输入文件累加，也只是实际输入 token 的一小部分。真实输入还包含对话历史和系统 prompt，这些在 shell 层**完全不可见**。

**Build 阶段的上下文隔离例外**：Superpowers `subagent-driven-development` 每个 Build task 在**独立 subagent** 中执行，B-001 的对话历史不会累积进 B-002。主编排会话只积累每个 task 返回的摘要（轻量），而非完整过程。因此 Build 阶段实际上下文增长远低于上述单 session 模型，`elapsed_seconds` 仍是最合理的复杂度代理指标。

### 7.3 metrics 字段定义（最终版）

```json
"metrics": {
  "started_at": "2026-06-06T11:30:00Z",    // ✅ 精确
  "completed_at": "2026-06-06T11:58:00Z",  // ✅ 精确
  "elapsed_seconds": 1680,                  // ✅ 精确，复杂度代理指标
  "output_chars": 8240,                     // ✅ 可测，本阶段生成的产物文件字符数
  "input_chars": 24600,                     // ⚠️ 可测但不完整，仅为输入文件静态大小
  "api_usage": null                         // 预留：等待 Anthropic 开放 usage API
}
````

> **不设置 `token_estimate`**：移除该字段，不做无意义的估算。`elapsed_seconds` 是目前最接近真实成本的可测指标——复杂阶段（Build、VerifyTech）耗时长，本质上就是 token 消耗多。

### 7.4 guard 脚本写入 metrics 的方式

```bash
# guard PASS 分支末尾，统一写入五个字段

COMPLETED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# 计算 output_chars：本阶段生成的所有产物文件大小之和
OUTPUT_CHARS=$(cat "$OFFICE_HOURS" "$AUTOPLAN" | wc -c)

# 计算 input_chars：本阶段读取的输入文件大小（不完整，仅供参考）
INPUT_CHARS=$(cat ".mymat/skills/mymat-product.md" "CLAUDE.md" 2>/dev/null | wc -c)

# 计算 elapsed_seconds
STARTED_AT=$(bash .mymat/scripts/mymat-state.sh read "$FEATURE_ID" ".phases.product.metrics.started_at" | tr -d '"')
if [[ -n "$STARTED_AT" && "$STARTED_AT" != "null" ]]; then
  START_TS=$(date -d "$STARTED_AT" +%s 2>/dev/null || \
    python3 -c "from datetime import datetime; print(int(datetime.fromisoformat('$STARTED_AT'.replace('Z','+00:00')).timestamp()))")
  END_TS=$(date -u +%s)
  ELAPSED=$(( END_TS - START_TS ))
else
  ELAPSED=0
fi

bash .mymat/scripts/mymat-state.sh metrics "$FEATURE_ID" "product" "completed_at"    "\"$COMPLETED_AT\""
bash .mymat/scripts/mymat-state.sh metrics "$FEATURE_ID" "product" "elapsed_seconds"  "$ELAPSED"
bash .mymat/scripts/mymat-state.sh metrics "$FEATURE_ID" "product" "output_chars"     "$OUTPUT_CHARS"
bash .mymat/scripts/mymat-state.sh metrics "$FEATURE_ID" "product" "input_chars"      "$INPUT_CHARS"
bash .mymat/scripts/mymat-state.sh metrics "$FEATURE_ID" "product" "api_usage"        "null"
```

### 7.5 /mymat:status 展示调整

删除原展示中的「~8.2K tokens」，改为展示实际可测数据：

```
✅ P  Product     done   (28 min | out: 8.2K chars)
✅ S  Spec        done   (35 min | out: 11.5K chars)
✅ D  Design      done   (15 min | out: 6.8K chars)
🔄 B  Build    3/8      (running | out: 24.6K chars so far)
```

`elapsed_seconds` 以「X min」形式展示，不再展示 token 数字。

---

## 八、关键序列图

### 8.1 新 Feature 全流程（/mymat:full）

```
用户              mymat-core.md       mymat-product.md     mymat-state.sh      guard scripts
  │                    │                    │                   │                   │
  │  /mymat:new        │                    │                   │                   │
  │──────────────────>│                    │                   │                   │
  │  [收集 title]      │                    │                   │                   │
  │<──────────────────│                    │                   │                   │
  │  feat-xxx-login    │                    │                   │                   │
  │──────────────────>│                    │                   │                   │
  │                   │── init feat-xxx ──>│                   │                   │
  │                   │                   │── write ──────────>│                   │
  │                   │                   │   (state.json init)│                   │
  │                   │── read product.md →│                   │                   │
  │                   │   │                │                   │                   │
  │                   │   │ [执行 P-01 /office-hours]          │                   │
  │                   │   │ [执行 P-02 /autoplan]              │                   │
  │                   │   │                │                   │                   │
  │                   │   │── guard-product.sh ───────────────>│                   │
  │                   │   │                │                   │<── PASS           │
  │                   │   │── snapshot hcg-1 ─────────────────>│                   │
  │                   │   │                │                   │                   │
  │  [HCG-1 展示]     │   │                │                   │                   │
  │<──────────────────│   │                │                   │                   │
  │  YES              │   │                │                   │                   │
  │──────────────────>│   │                │                   │                   │
  │                   │── write product.status=done ──────────>│                   │
  │                   │── 推进到 /mymat:spec ──────────────────>...
```

### 8.2 Build 断点恢复流程

```
新会话开始
  │
  │  /mymat
  │
  ├── mymat-state.sh active
  │   └── 返回：feat-xxx-login | build | in_progress
  │
  ├── 读取 state.json
  │   └── completed_tasks: [B-001, B-002, B-003]
  │       last_task_id: B-003
  │       total_tasks: 8
  │
  ├── 展示状态面板
  │   └── 3/8 tasks done, last: B-003
  │
  ├── 询问"继续 Build？"
  │
  ├── 用户确认
  │
  ├── mymat-guard-spec-integrity.sh（校验 spec 未被改动）
  │   └── PASS
  │
  ├── 读取 tasks.md，遍历任务列表
  │   ├── B-001 → skip（in completed_tasks）
  │   ├── B-002 → skip
  │   ├── B-003 → skip
  │   └── B-004 → 开始执行
```

### 8.3 HCG 拒绝回滚流程

```
用户在 HCG-2 回复 NO
  │
  ├── mymat-core.md 保持 current_phase=spec，不推进
  │
  ├── 询问"需要修改 spec 内容还是重新运行 /mymat:spec？"
  │
  │  用户选择"重新运行 spec"
  │
  ├── 注意：此时 spec-graph.json 已初始化（SHA256 已记录）
  │   但状态仍在 spec 阶段，可直接重新运行
  │
  │  若用户改动了 specs.md 并想重新确认：
  │
  ├── /mymat:rollback hcg-1
  │   └── mymat-state.sh rollback feat-xxx hcg-1
  │       └── 还原 state.json 到 HCG-1 前状态
  │       └── 清除 spec-graph.json（因为 spec 未完成）
  │
  └── 重新运行 /mymat:spec
```

---

## 九、/mymat:init 安装脚本逻辑

```bash
#!/usr/bin/env bash
# mymat-install.sh — /mymat:init 时由 AI 通过 Bash 工具执行

set -euo pipefail

echo "=== Mymat Installer ==="

# 1. 检测依赖
check_dep() {
  command -v "$1" &>/dev/null || { echo "MISSING: $1 is required. Install: $2"; exit 1; }
}
check_dep jq      "brew install jq  or  apt-get install jq"
check_dep git     "install git"
if ! command -v sha256sum &>/dev/null && ! command -v shasum &>/dev/null; then
  echo "MISSING: sha256sum or shasum is required. Install coreutils (Linux/macOS) or ensure shasum is available."
  exit 1
fi

echo "✅ Dependencies OK"

# 2. 创建目录结构
mkdir -p .mymat/{skills,scripts,features}

# 3. 检测平台
detect_platform() {
  [[ -f "package.json" ]] && echo "node" && return
  [[ -f "requirements.txt" || -f "pyproject.toml" ]] && echo "python" && return
  [[ -f "pom.xml" || -f "build.gradle" ]] && echo "java" && return
  [[ -f "go.mod" ]] && echo "go" && return
  echo "generic"
}
PLATFORM=$(detect_platform)

# 4. 生成 config.json
cat > .mymat/config.json <<EOF
{
  "version": "1.0",
  "project_name": "$(basename "$PWD")",
  "platform": "$PLATFORM",
  "test_command": "$(case $PLATFORM in node) echo "npm test";; python) echo "python -m pytest";; java) echo "mvn test";; *) echo "make test";; esac)",
  "scripts_dir": ".mymat/scripts",
  "skills_dir": ".mymat/skills",
  "openspec_dir": "openspec",
  "token_tracking": true,
  "auto_workflow_detect": true,
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "mymat_version": "0.1.0"
}
EOF

# 5. 下载/复制 skill 文件和脚本文件
# （实际实现：从 GitHub release 或本地模板目录复制）
echo "✅ config.json created (platform: $PLATFORM)"

# 6. 检测 CLAUDE.md 是否已有 Mymat 配置
if grep -q "Mymat 工作流系统" CLAUDE.md 2>/dev/null; then
  echo "ℹ️  CLAUDE.md already contains Mymat config. Skipping."
else
  cat >> CLAUDE.md << 'MYMAT_CONFIG'

---

## Mymat 工作流系统

当用户输入 `/mymat` 开头的命令时，立即读取 `.mymat/skills/mymat-core.md` 并按其路由逻辑执行。
**禁止**在未执行 guard 脚本前声称阶段已完成。HCG 必须等待用户明确确认。
MYMAT_CONFIG
  echo "✅ CLAUDE.md updated"
fi

echo ""
echo "=== Mymat installed successfully ==="
echo "Run /mymat:new to start your first feature."
```

---

## 十、错误处理规范

### 10.1 Guard 错误消息格式

```
FAIL: {Phase} phase has {N} error(s):
  - {ERROR_TYPE}: {human-readable description}
  - {ERROR_TYPE}: {human-readable description}

[ACTION HINT]: {具体的修复建议}
```

ERROR_TYPE 枚举：
| 类型 | 含义 |
|---|---|
| `MISSING` | 文件不存在 |
| `EMPTY` | 文件存在但内容不符合要求 |
| `INCOMPLETE` | 文件存在但关键章节缺失 |
| `FAILING` | 测试文件存在但测试不通过 |
| `OPEN_ISSUES` | 报告存在未解决的 issue |
| `FAIL_CONTENT` | 报告内容不含预期通过标记 |
| `SHA256_MISMATCH` | 冻结文件被篡改 |
| `FILE_DELETED` | 冻结文件被删除 |

### 10.2 AI 响应规则

guard 脚本 exit 1 时，AI 必须：

1. 展示完整错误信息（不得截断）
2. 停止当前阶段推进
3. 给出可操作的修复建议
4. 等待用户指令（`/mymat:retry`、`/mymat:park` 或直接修复后重试）
5. **不得**绕过 guard 继续执行后续任务

---

## 十一、多 Feature 并发边界规则

1. **state.json 隔离**：每个 feature 有独立目录，互不影响
2. **spec-graph 隔离**：每个 feature 的 SHA256 记录独立，不会跨 feature 误判
3. **并发冲突检测**（开发阶段暂不实现，预留接口）：
   - 两个 feature 同时修改同一文件时，guard 应检测 git merge conflict 标记
   - 检测命令：`git status --short | grep -c "^UU"`
4. **任务命名前缀规则**：同一会话内，feature_id 会被写入所有产物文件的 frontmatter，避免混淆

---

## 十二、待实现清单（MVP 范围外）

以下功能在设计中已预留接口，但 MVP 不实现：

| 功能                 | 预留位置                      | 备注                                    |
| -------------------- | ----------------------------- | --------------------------------------- |
| 并发冲突检测         | mymat-guard-spec-integrity.sh | 预留注释占位                            |
| 工作流历史 analytics | state.json metrics            | 累积后续版本分析                        |
| Web UI 状态面板      | —                             | 读取 state.json 生成                    |
| `/mymat:doctor`      | —                             | 依赖检查 + 目录完整性 + state.json 校验 |
| `/mymat:version`     | —                             | 显示当前版本，提示可用更新              |
| 可分发安装           | —                             | npm 包分发、自更新命令（路线图）        |

---

## 关联连接

- [[mymat-design]] — 系统设计方案（本文档的上级文档）
- [[OpenSpec]] — S 阶段核心工具
- [[Superpowers]] — D/B/Vt 阶段核心工具
- [[Gstack]] — P/Vp/R 阶段核心工具
- [[AtomicTDDWorkflow]] — Build 阶段 TDD 循环底层原理
