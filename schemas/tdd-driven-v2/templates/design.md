# Design: {{change_name}}

## File Structure

```
src/
  [source file]           # 生产代码
  [source file].test.ts   # 对应测试文件（紧邻源文件）
```

## Test Strategy

| 文件               | 测试类型 | 覆盖场景           |
| ------------------ | -------- | ------------------ |
| `[test file path]` | unit     | Scenario 1, 2, ... |

Test runner: `npm test`

## Implementation Notes

<!-- 实现要点：关键算法、边界处理、不实现哪些 -->
