# WorkBuddy 开发上下文

## 项目：麦门抽签 - McDonald's Fortune-Telling Ordering

### 开发工具

- **开发平台**：WorkBuddy AI
- **MCP 集成**：麦当劳 MCP Server (mcd-mcp)
- **开发语言**：Python 3 + Markdown

### 开发过程

#### 阶段 1：比赛分析与 MCP 配置验证

1. 分析麦当劳程序员创意开发大赛的规则和要求
2. 读取 `~/.workbuddy-ai/mcp.json` 确认 MCP 配置
3. 调用 `mcp__mcd-mcp__now-time-info` 验证 MCP 连通性
4. 调用 `mcp__mcd-mcp__query-nearby-stores` 获取门店数据结构
5. 调用 `mcp__mcd-mcp__query-meals` 获取餐品列表数据结构
6. 调用 `mcp__mcd-mcp__available-coupons` 获取优惠券数据

#### 阶段 2：创意构思与方向选择

进行了头脑风暴，产生 6 大方向 12 个创意：
- 省钱实用（省钱计算器、优惠券猎人）
- 趣味社交（今日运势、盲盒点餐）
- 健康饮食（卡路里管家、Cheat Meal 规划）
- 游戏化（成就系统、积分农场）
- 生活场景（深夜食堂、团餐AA制）
- 数据洞察（消费年报、跨城市价格对比）

最终选定 **"麦门抽签"** 方向，理由：
- "麦门"是中文互联网已有梗文化，传播基础好
- 抽签 + 点餐的组合天然有趣
- 每日可用，可复用性强
- MCP 工具调用链路完整（5 个工具）
- 运势文案有创意空间

#### 阶段 3：数据采集与分析

通过 MCP 工具获取真实数据：
- 北京建外 SOHO 门店 (storeCode: 1950564) 的完整餐品列表
- 40+ 餐品的 code、name、currentPrice 数据
- 可用优惠券列表（中薯条买一送一、人气麦旋风买一送一等）

分析了麦当劳官方搭配规则：
- <20元：小食
- 20-30元：汉堡+小食 或 汉堡+饮料
- 30-40元：汉堡+薯条/小食+饮料
- 40-50元：汉堡+薯条+小食+饮料
- 50元+：丰富组合

#### 阶段 4：核心引擎开发

开发了 `fortune_engine.py` 运势引擎：
- `FortuneEngine` 类：核心抽签逻辑
- `FortuneResult` 数据类：抽签结果结构
- `draw(budget)` 方法：根据预算抽签
- `_match_meals(budget)` 方法：按预算匹配餐品
- `format_result(result)` 方法：格式化输出

编写了 40+ 餐品的运势模板（fortune_templates.json）：
- 每个汉堡/小食/饮料/甜品/套餐都有独特的签名、宜忌、星级、幸运色、幸运数字、签文解语
- 额外 10 条随机运势短句

#### 阶段 5：Skill 定义与文档编写

- 编写 SKILL.md：定义 WorkBuddy Skill 的完整执行流程
- 编写 README.md：项目介绍和使用说明
- 编写 MCP_INTEGRATION.md：5 个 MCP Tool 的调用说明
- 编写 mcp-config.example.json：脱敏配置（仅环境变量占位符）
- 使用官方 CONTEST_DECLARATION.md：参赛声明（内容不可修改）

#### 阶段 6：测试与验证

使用不同预算测试引擎：
- 15 元：抽到"玉米杯"财运满堂签
- 30 元：抽到"麦香鸡套餐"返璞归真签
- 45 元：抽到"麦香鸡+芝士条+可乐"组合
- 60 元：抽到"双层吉士汉堡套餐+锡兰红茶+麦乐鸡"好事成双签

所有测试通过，搭配不超支，运势文案有趣且每次不同。

### 使用的麦当劳 MCP Tool

| # | Tool 名称 | 用途 |
|---|----------|------|
| 1 | `query-nearby-stores` | 查询附近门店，获取 storeCode |
| 2 | `query-meals` | 查询餐品列表，获取 code/name/price |
| 3 | `available-coupons` | 查询可用优惠券 |
| 4 | `calculate-price` | 计算选中餐品价格 |
| 5 | `now-time-info` | 获取服务器时间（签号生成） |

### 开发环境

- 操作系统：macOS (Darwin)
- Python 版本：3.13
- 开发工具：WorkBuddy AI
- MCP 配置：~/.workbuddy-ai/mcp.json

### 开发者声明

本项目使用 WorkBuddy AI 完成全部开发，包括：
- MCP 数据采集与分析
- 创意构思与方向选择
- 核心引擎代码编写
- 运势文案创作
- 参赛文档编写
- 测试与验证
