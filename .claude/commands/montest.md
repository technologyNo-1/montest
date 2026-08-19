# MontExam — 一键生成交互式练习平台

将 Markdown 习题文件转换为可部署的交互式 Web 练习平台。

## 输入

用户提供习题 Markdown 文件路径（$ARGUMENTS）。

## 执行流程

### Phase 1: 解析习题（解析器自动完成）

运行内置 markdown 解析器提取结构化数据：

```bash
node /Users/wyf/Desktop/code/document/06-workflows/exam-platform/scripts/parse-exam.js \
  "<习题.md>" "<答案.md>" "/tmp/montest-exam-data.json"
```

解析器自动识别三种题型：
- **选择题**：含 A/B/C/D 选项的题目
- **简答题**：需要文字回答的题目
- **编程题**：含代码块或要求编写函数的题目

如果解析器无法完美处理（常见于非标准格式），手动调整 `/tmp/montest-exam-data.json`。

### Phase 2: 生成参考答案（如无答案文件）

如果用户没有提供答案文件，Claude 需要：

1. 逐题分析，生成正确答案和解析
2. 编程题需提供：参考代码 + 至少 2-3 个测试用例（输入 + 期望输出）
3. 将答案写入 JSON 数据文件的对应字段

**答案 code-review 校验**：
生成全部答案后，逐题自审：
- 选择题：逐一验证每个选项是否符合题目要求，确认正确选项无争议
- 编程题：在脑中执行参考代码，走一遍每个测试用例的输入→输出，确认无逻辑错误
- 简答题：检查答案是否覆盖核心知识点，有无明显遗漏
- 发现错误立即修正后再进入 Phase 3

答案 JSON 格式：
```json
{
  "CH": [{"id":1, "q":"题目", "o":["A","B","C","D"], "a":0, "e":"解析"}],
  "SH": [{"id":1, "q":"题目", "a":"<h4>答案HTML</h4><p>详细解析...</p>"}],
  "CD": [{"id":1, "q":"题目", "s":"def func():\n    pass", "a":"def func():\n    return ...", "t":[{"c":"func(1)", "e":2}]}],
  "meta": {"title":"标题", "choiceCount":10, "shortCount":5, "codeCount":5, "total":20}
}
```

### Phase 3: 构建 HTML 平台

判断模式：如果用户参数含 `--local`，使用 `--mode local` 构建本地 Python 模式。

```bash
# 浏览器模式（默认，Skulpt）
node /Users/wyf/Desktop/code/document/06-workflows/exam-platform/scripts/build.js \
  /tmp/montest-exam-data.json \
  --output "<输出目录>/<标题>.html" \
  --title "练习标题"

# 本地模式（真实 Python + WebSocket + PyCharm 联动）
node /Users/wyf/Desktop/code/document/06-workflows/exam-platform/scripts/build.js \
  /tmp/montest-exam-data.json \
  --output "<输出目录>/<标题>.html" \
  --title "练习标题" \
  --mode local
```

构建脚本自动完成：
- 注入题目数据到应用模板
- 组装 CSS 设计系统 + HTML 骨架 + JS 逻辑
- 内联所有第三方库（CodeMirror、canvas-confetti）
- **浏览器模式**：内联 Skulpt（~1.3MB），纯静态可用
- **本地模式**：WebSocket 客户端（~0.4MB），需启动本地服务器
- 输出完全自包含的单 HTML 文件

### Phase 4: 验证与部署

1. **本地验证**：用浏览器打开 HTML 文件检查渲染
2. **本地 Python 模式启动**（`--mode local` 时）：
   ```bash
   python /Users/wyf/Desktop/code/document/06-workflows/exam-platform/scripts/montest-serve.py \
     --html "<输出目录>/<标题>.html"
   # 浏览器访问 http://localhost:8234
   # .py 文件自动保存到 ./montest-submissions/，PyCharm 可直接打开调试
   ```
3. **部署到 Netlify**（用户要求时）：
   ```bash
   # 方式一：拖拽上传到 app.netlify.com/drop
   # 方式二：CLI 部署
   netlify deploy --dir="<目录>" --prod --site="<站点名>"
   ```

## 关键技术栈

| 组件 | 技术 | 作用 |
|------|------|------|
| 代码编辑器 | CodeMirror 5 | Python 语法高亮 + 自动补全 |
| Python 运行时（浏览器） | Skulpt | 浏览器端执行 Python（不支持标准库） |
| Python 运行时（本地） | subprocess + WebSocket | 连接本地真实 Python 解释器 |
| 庆祝效果 | canvas-confetti | 通过测试时的动画反馈 |
| UI 设计 | Capsule + Soft Editorial | pill 按钮 + hard shadow + 渐变色 |
| 构建 | Node.js | 单文件打包（零依赖） |
| 本地服务器 | Python stdlib | HTTP + WebSocket 桥接，零依赖 |

## 注意事项

- 习题 markdown 格式越规范，解析越准确。推荐格式见 `Python阶段考试样例题.md`
- 编程题的测试用例需要手动设计或让 Claude 生成，不能纯自动推断
- Skulpt 是 Python 的 JS 实现，不支持所有标准库（如 numpy/pandas）
- 单 HTML 文件约 1.2-1.5MB（含所有 vendor 库），这是功能完整性的代价
- 部署到 Netlify 需要先 `netlify login`
