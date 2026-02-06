# Tushare Stock Service

基于Tushare的股票数据服务，提供股票列表自动同步和RESTful API查询功能。

## 功能特性

- 每天凌晨1点自动同步A股股票列表数据
- RESTful API支持股票名称模糊搜索
- 支持Docker容器化部署
- 提供Helm Charts用于Kubernetes部署

## 技术栈

- Python 3.11 + Flask
- MySQL 8.4
- APScheduler (定时任务)
- SQLAlchemy (ORM)
- Docker + Kubernetes + Helm

## 快速开始

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `TUSHARE_TOKEN` | Tushare API Token | - |
| `DB_HOST` | MySQL主机地址 | localhost |
| `DB_PORT` | MySQL端口 | 3306 |
| `DB_NAME` | 数据库名 | tushare |
| `DB_USER` | 数据库用户 | root |
| `DB_PASSWORD` | 数据库密码 | - |
| `SYNC_HOUR` | 同步任务执行小时 | 1 |
| `SYNC_MINUTE` | 同步任务执行分钟 | 0 |

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export TUSHARE_TOKEN=your_token
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=tushare

# 启动服务
python run.py
```

### Docker部署

```bash
# 构建镜像
docker build -t tushare:latest .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -e TUSHARE_TOKEN=your_token \
  -e DB_HOST=mysql_host \
  -e DB_USER=tushare \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=tushare \
  tushare:latest
```

### Kubernetes部署 (Helm)

```bash
# 添加Helm仓库
helm repo add tushare https://<username>.github.io/tushare
helm repo update

# 安装
helm install tushare tushare/tushare \
  --set image.repository=<username>/tushare \
  --set tushareToken=your_token \
  --set mysql.rootPassword=your_root_password \
  --set mysql.password=your_password
```

## API接口

### 健康检查

```
GET /health
```

响应:
```json
{"status": "ok"}
```

### 模糊搜索股票

```
GET /api/stocks/search?q=关键词&limit=20
```

参数:
- `q` (必填): 搜索关键词
- `limit` (可选): 返回数量限制，默认20，最大100

响应:
```json
{
  "data": [
    {
      "ts_code": "000001.SZ",
      "symbol": "000001",
      "name": "平安银行",
      "area": "深圳",
      "industry": "银行",
      "market": "主板",
      "list_date": "1991-04-03"
    }
  ],
  "count": 1
}
```

### 按代码查询

```
GET /api/stocks/<ts_code>
```

响应:
```json
{
  "data": {
    "ts_code": "000001.SZ",
    "symbol": "000001",
    "name": "平安银行",
    "area": "深圳",
    "industry": "银行",
    "market": "主板",
    "list_date": "1991-04-03"
  }
}
```

## CI/CD配置

### GitHub Secrets

在GitHub仓库Settings中配置以下secrets:

- `DOCKERHUB_USERNAME`: Docker Hub用户名
- `DOCKERHUB_TOKEN`: Docker Hub Access Token

### GitHub Pages

启用GitHub Pages，源分支选择`gh-pages`，用于托管Helm Charts。

## 项目结构

```
tushare/
├── app/
│   ├── __init__.py          # Flask应用初始化
│   ├── config.py            # 配置管理
│   ├── models/
│   │   └── stock.py         # 数据模型
│   ├── services/
│   │   ├── tushare_service.py  # Tushare API封装
│   │   └── stock_service.py    # 业务逻辑
│   ├── routes/
│   │   └── stock_routes.py     # API路由
│   └── scheduler/
│       └── jobs.py             # 定时任务
├── helm/
│   └── tushare/             # Helm Charts
├── .github/
│   └── workflows/           # GitHub Actions
├── Dockerfile
├── requirements.txt
└── run.py                   # 应用入口
```

## License

MIT
