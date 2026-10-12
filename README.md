# 麦门抽签 McDonald's Fortune-Telling Ordering

[![GitHub stars](https://img.shields.io/github/stars/zouweivivian723-stack/mcd-fortune-ordering?style=social)](https://github.com/zouweivivian723-stack/mcd-fortune-ordering)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![McDonald's MCP](https://img.shields.io/badge/McDonald's-MCP-red.svg)](https://github.com/M-China/mcd-mcp-server)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-green.svg)](https://www.workbuddy.cn)

> 输入预算，抽取今日麦运。一份套餐，一段签文，一种命运。

**如果觉得有趣，点个 Star 支持一下！** :star:

---

## 这是什么？

**麦门抽签** 是一个基于麦当劳 MCP（Model Context Protocol）能力开发的创意 Skill，将麦当劳点餐与中国传统抽签文化巧妙结合。

用户输入一个预算金额（如"30 元"），系统会：

1. 自动查询麦当劳餐品和价格
2. 在预算范围内随机搭配套餐
3. 为搭配结果生成一份有趣的"运势解读"——签号、宜忌、财运/桃花运/事业运星级、幸运色、幸运数字、签文解语
4. 检查可用优惠券，给出省钱建议

每一次抽签都是独一无二的。不同的预算、不同的搭配、不同的运势——吃个麦当劳，也能吃出命运的仪式感。

## 效果演示

```
====================================================
        麦门今日运势 · 抽签结果
====================================================

  麦签号: 上签 第481号
  签名套餐: 双层吉士汉堡套餐 + 锡兰红茶 + 麦乐鸡

  --- 套餐明细 ---
    双层吉士汉堡套餐          34.0
    锡兰红茶                  11.5
    麦乐鸡                    14.0
                          ------
    合计                      59.5
  预算: 60.0 元
  实付: 59.5 元 (省 0.5 元)

  --- 运势解读 ---
  今日宜: 谈合作  买一送一  双倍下注
  今日忌: 单打独斗  独食
  财运指数: ****.
  桃花运:   ****.
  事业运:   ****.
  幸运色:   双层橙色
  幸运数字: 6

  --- 麦签解语 ---
  双层吉士，好事成双。今日一切与"双"有关的事物都自带buff。
  宜与人合作，宜分享食物，宜接受那个第二次邀请。

  [此签大吉。但吉不吉，看你吃完有没有擦嘴。]

====================================================
```

## 安装与使用

### 前置条件

1. 申请麦当劳 MCP Token（参考[麦当劳 MCP Server GitHub 使用指南](https://github.com/M-China/mcd-mcp-server)）
2. 安装 Python 3.8+（仅使用标准库，无需额外依赖）

### 方式一：WorkBuddy 中使用（推荐）

1. 打开 WorkBuddy，在左侧边栏【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】
2. 填入以下配置（替换 `YOUR_MCP_TOKEN` 为实际 Token）：
   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": {
           "Authorization": "Bearer YOUR_MCP_TOKEN"
         }
       }
     }
   }
   ```
3. 启用 mcd-mcp 连接器
4. 在对话框中说："帮我抽个麦签，预算 30 元"

### 方式二：本地运行

```bash
git clone https://github.com/zouweivivian723-stack/mcd-fortune-ordering.git
cd mcd-fortune-ordering
python3 src/fortune_engine.py 30
```

> 试不同预算：`python3 src/fortune_engine.py 15` / `30` / `50` / `100`

## 可视化抽签卡片

除了命令行输出，我们还提供了一个**可视化抽签卡片**（`fortune_card.html`），让抽签体验更具仪式感：

- **麦当劳红黄配色**：经典品牌视觉，金色签筒 + 红色卡片 + 黄色点缀
- **竹筒摇签动画**：模拟传统抽签的竹筒晃动，签条从筒中滑出
- **金光爆发特效**：签条落地瞬间，金色光晕向外扩散
- **卡片翻转揭示**：运势卡片以 3D 翻转效果登场
- **星级弹出动画**：财运/桃花运/事业运星级依次弹入
- **Web Audio API 音效**：
  - 摇签音效（白噪声模拟竹筒晃动声）
  - 揭示音效（C-E-G-C 上行琶音）
  - 星级弹出音效（高频清脆叮声）
- **一键下载图片**：使用 html2canvas 将运势卡片导出为 PNG 图片，可分享到朋友圈

### 在线体验

直接用浏览器打开 `fortune_card.html` 即可体验：

```bash
# 克隆后直接打开
open fortune_card.html        # macOS
start fortune_card.html        # Windows
xdg-open fortune_card.html     # Linux
```

选择预算金额（15/30/50/100 元），点击「抽签」按钮，享受完整的视听抽签体验！

## 项目结构

```
mcd-fortune-ordering/
├── README.md                    # 项目介绍
├── CONTEST_DECLARATION.md       # 参赛声明（官方文件，不可修改）
├── MCP_INTEGRATION.md            # MCP 集成说明
├── mcp-config.example.json       # 脱敏 MCP 配置示例
├── workbuddy.md                  # WorkBuddy 开发上下文
├── SKILL.md                      # WorkBuddy Skill 定义文件
├── fortune_card.html             # 可视化抽签卡片（动画+音效+图片下载）
├── src/
│   └── fortune_engine.py         # 运势引擎核心代码
└── data/
    ├── fortune_templates.json    # 运势文案模板（40+ 餐品运势）
    └── meal_catalog.json         # 餐品目录与价格
```

## 搭配规则

遵循麦当劳官方套餐搭配建议：

| 预算范围 | 搭配策略 |
|---------|---------|
| < 20 元 | 小食为主（薯条/麦乐鸡/玉米杯等） |
| 20-30 元 | 汉堡 + 小食 或 汉堡 + 饮料 |
| 30-40 元 | 汉堡 + 薯条/小食 + 饮料 |
| 40-50 元 | 汉堡 + 薯条 + 小食 + 饮料 |
| 50 元+ | 丰富组合（优先选套餐 + 额外小食/甜品） |

## 运势系统

每个餐品都有对应的运势属性：

- **汉堡/套餐** → 事业运、财运（力量与决断）
- **小食** → 财运（小确幸与积累）
- **饮品类** → 灵感、人际运（情绪与流动）
- **甜品** → 桃花运（甜蜜与惊喜）

运势解读包含：签号、签名、今日宜/忌、财运/桃花运/事业运星级（1-5星）、幸运色、幸运数字、签文解语、附加运势短句。

## 技术亮点

- **MCP 全链路调用**：门店查询 → 餐品列表 → 优惠券 → 价格计算，真实使用 5 个麦当劳 MCP 工具
- **预算感知搭配算法**：根据预算智能选择搭配策略，保证不超支
- **40+ 餐品运势模板**：每个餐品都有独特的运势文案，组合生成千变万化的签文
- **WorkBuddy Skill 集成**：支持在 WorkBuddy 中直接对话使用
- **可视化抽签卡片**：纯前端实现（HTML/CSS/JS），麦当劳红黄品牌配色，竹筒摇签动画 + 金光特效 + Web Audio API 音效 + html2canvas 图片导出，零依赖开箱即用

## 目标用户

- 麦当劳爱好者（"麦门信徒"）
- 每天纠结吃什么的人
- 喜欢抽签/运势/星座等趣味内容的人
- 想要省钱又想吃好的人

## 参赛信息

本项目为 **麦当劳程序员创意开发大赛** 参赛作品。

- 比赛仓库：[M-China/mcd-developer-innovation-challenge](https://github.com/M-China/mcd-developer-innovation-challenge)
- 使用 WorkBuddy 开发

## License

MIT
