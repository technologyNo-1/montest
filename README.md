# MontExam

**Markdown 习题 → 可部署的交互式 Web 练习平台，一键完成。**

```
你的习题.md ──→ MontExam ──→ 单HTML文件 + 部署链接
```

## 解决什么问题

1. **老师/培训者**有 Markdown 格式的习题集，想快速变成在线练习平台
2. **学习者**想在浏览器里直接写代码、运行测试、查看答案
3. **传统方案**需要搭建服务器、写前端、配置部署——MontExam 一行命令搞定

## 功能

- 选择题：点击选项即时判分，附详细解析
- 简答题：参考答案折叠展示，含代码高亮
- 编程题：内置 Python 编辑器（CodeMirror）+ 浏览器端 Python 运行时（Skulpt），支持自动补全和实时测试
- **本地 Python 模式**（`--mode local`）：浏览器编辑器通过 WebSocket 连接本地真实 Python 解释器，支持标准库和第三方包；每次执行自动保存 `.py` 文件，可直接在 PyCharm 中打开调试
- 明暗主题自动切换
- 进度条 + localStorage 持久化
- 通过测试时随机庆祝动画
- **完全自包含**：单个 HTML 文件，无服务器依赖，任意打开即用
- 响应式设计，移动端可用

## 快速开始

### 作为 Claude Code Skill 使用（推荐）

```bash
# 最简单：只给习题文件，Claude 自动生成答案
/montest path/to/你的习题.md

# 有现成答案：同时传入答案文件（答案质量更高）
/montest path/to/你的习题.md path/to/答案.md
```

Claude 会自动解析 → 生成答案（含 code-review 校验）→ 构建 HTML → 给你部署链接。

### 手动使用

```bash
# 1. 解析习题 Markdown 为 JSON
node scripts/parse-exam.js 习题.md 答案.md exam-data.json

# 2. 构建单 HTML 文件（浏览器模式，Skulpt）
node scripts/build.js exam-data.json --output 练习平台.html --title "我的练习"

# 或：构建本地模式（连接真实 Python，支持标准库）
node scripts/build.js exam-data.json --output 练习平台.html --mode local

# 3. 浏览器直接打开（浏览器模式）
open 练习平台.html

# 或：启动本地服务器（本地模式）
python scripts/montest-serve.py --html 练习平台.html
# 浏览器访问 http://localhost:8234
```

## 项目结构

```
montest/
├── scripts/
│   ├── parse-exam.js      # Markdown 解析器（习题 → JSON）
│   ├── build.js           # 构建脚本（JSON + 模板 → HTML）
│   ├── deploy.js          # 部署脚本（Netlify / 本地预览）
│   └── montest-serve.py   # 本地 Python 桥接服务器（零依赖）
├── templates/
│   ├── styles.css         # UI 设计系统（Capsule + Soft Editorial）
│   ├── body.html          # HTML 骨架模板
│   └── ws-client.js       # 本地模式 WebSocket 客户端
├── vendor/                # 第三方库（已内联到最终 HTML）
│   ├── codemirror.min.js
│   ├── skulpt.min.js
│   ├── skulpt-stdlib.js
│   ├── canvas-confetti.browser.js
│   └── ...（共 10 个文件）
└── README.md
```

## 习题 Markdown 格式

支持以下格式，解析器会自动识别题型：

```markdown
## 一、选择题（10题，每题 3 分）

1. 以下哪个是合法变量名？（ ）
A. 2var
B. var-1
C. _var1
D. var@1

## 二、简答题（5题）

1. 简述 Python 中 for 循环和 while 循环的区别。

## 三、编程题（5题）

1. 编写一个函数，返回列表中所有偶数的和。

def sum_even(nums):
    pass
```

## 技术栈

| 组件 | 用途 | 大小 |
|------|------|------|
| [CodeMirror 5](https://codemirror.net/) | 代码编辑器 + Python 语法高亮 | ~200KB |
| [Skulpt](https://skulpt.org/) | 浏览器端 Python 运行时 | ~1.1MB |
| [canvas-confetti](https://github.com/catdad/canvas-confetti) | 庆祝动画 | ~25KB |

## License

MIT
