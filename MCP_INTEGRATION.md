# MCP Integration - 麦当劳 MCP 集成说明

## 使用的 MCP Server

| 项目 | 内容 |
|------|------|
| Server 名称 | mcd-mcp |
| Server URL | https://mcp.mcd.cn |
| 传输类型 | streamablehttp |
| 认证方式 | Bearer Token（通过 Authorization Header 传递） |
| Token 获取 | [麦当劳 MCP Server](https://github.com/M-China/mcd-mcp-server) 控制台申请 |

## 使用的 MCP Tool 清单

本项目实际使用了以下 5 个麦当劳 MCP Tool：

### 1. `query-nearby-stores` — 查询附近门店

**用途**：根据用户所在城市和位置，查询附近可点餐的麦当劳门店，获取 storeCode。

**调用参数**：
```json
{
  "beType": 1,
  "searchType": 2,
  "city": "北京",
  "keyword": "国贸"
}
```

**返回数据**：门店列表，包含 storeCode、storeName、address、distance、businessStatus 等。

**调用时机**：Step 2，获取门店编码供后续餐品查询使用。

### 2. `query-meals` — 查询餐品列表

**用途**：查询指定门店的完整餐品列表，获取餐品编码、名称、价格等信息。

**调用参数**：
```json
{
  "storeCode": "1950564",
  "orderType": 1,
  "beType": 1
}
```

**返回数据**：分类的餐品列表，每个餐品包含 code、name、image、currentPrice、originalPrice 等。

**调用时机**：Step 3，获取餐品数据用于随机搭配。

### 3. `available-coupons` — 查询可用优惠券

**用途**：查询用户当前可领取的优惠券列表，用于省钱提示。

**调用参数**：
```json
{}
```

**返回数据**：优惠券列表，包含券名称、图片、状态、促销标签等。

**调用时机**：Step 4，获取优惠券信息展示给用户。

### 4. `calculate-price` — 计算价格

**用途**：计算选中餐品的实际价格（含优惠），确认最终金额。

**调用参数**：
```json
{
  "storeCode": "1950564",
  "orderType": 1,
  "beType": 1,
  "items": [
    {"productCode": "9900005456", "quantity": 1},
    {"productCode": "9900008751", "quantity": 1}
  ]
}
```

**返回数据**：价格信息（单位为分，需除以100转为元）。

**调用时机**：Step 6，计算最终价格确认不超预算。

### 5. `now-time-info` — 获取服务器时间

**用途**：获取麦当劳服务器当前时间，用于签号生成的时间戳和营业状态判断。

**调用参数**：
```json
{}
```

**返回数据**：包含 timestamp、datetime、timezone 等时间信息。

**调用时机**：Step 1（可选），获取当前时间用于签号生成。

## 调用流程图

```
用户输入预算
    │
    ▼
[query-nearby-stores] ──→ 获取 storeCode
    │
    ▼
[query-meals] ──────────→ 获取餐品列表 (code, name, price)
    │
    ▼
[available-coupons] ─────→ 获取优惠券列表
    │
    ▼
随机搭配算法 ────────────→ 在预算内选择餐品组合
    │
    ▼
[calculate-price] ───────→ 确认最终价格
    │
    ▼
运势生成引擎 ────────────→ 生成签文/运势解读
    │
    ▼
输出签文卡片
```

## 业务价值

1. **提升点餐体验**：将枯燥的点餐决策转化为有趣的抽签体验
2. **降低决策成本**：用户只需给预算，系统自动搭配，解决"吃什么"难题
3. **促进优惠券使用**：自动展示可用优惠券，引导用户领券下单
4. **增强用户粘性**：每日可抽签，签文结果独特，具有分享传播性
5. **品牌互动**：将麦当劳品牌与中国抽签文化结合，创造独特的品牌记忆点

## 配置示例

脱敏后的 MCP 配置（仅使用环境变量占位符）：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer ${MCD_MCP_TOKEN}"
      }
    }
  }
}
```

实际使用时，将 `${MCD_MCP_TOKEN}` 替换为从麦当劳 MCP 控制台获取的真实 Token。
