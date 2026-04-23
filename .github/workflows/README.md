# GitHub Actions CI/CD 部署指南

## 项目概览

| 项目 | 详情 |
|------|------|
| 名称 | exchange-rate |
| 版本 | 0.0.1-SNAPSHOT |
| 框架 | Spring Boot 2.1.1 |
| Java 版本 | 1.8 |
| 构建工具 | Maven |
| 测试框架 | JUnit + Spring Boot Test |

---

## 工作流概览

| 工作流 | 触发条件 | 功能 |
|--------|----------|------|
| **CI/CD Pipeline** | push/PR | 自动构建、测试、打包、发布、生成报告 |

### 工作流阶段

```
ci.yml
├── ci          (Build & Test)     ← Maven 编译 + JUnit 测试 + 生成报告
├── build       (Build Package)    ← 打包 JAR
├── release     (Release)          ← main/master 推送时自动发版
└── docker      (Build Docker)     ← 推送到 GHCR (可选)
```

---

## 报告生成

### 自动生成的报告

| 报告类型 | 路径 | 说明 |
|----------|------|------|
| **CI 聚合报告** | `ci-reports/ci-report-latest.html` | 完整的构建、测试、覆盖率报告 |
| **JUnit 测试报告** | `target/surefire-reports/` | Maven Surefire 测试结果 |
| **覆盖率报告** | `target/site/jacoco/index.html` | JaCoCo 代码覆盖率详情 |

### 报告内容

CI 报告包含以下章节：

1. **构建阶段** - 编译、依赖下载、打包状态
2. **测试阶段**
   - 单元测试结果（OceanRatesTest, ReptileCMCTest, ConvertFXHTest, DataCacheTest）
   - 接口自动化测试结果（Mock数据，8个API端点，50个用例）
3. **静态代码分析** - 代码问题检测
4. **代码覆盖率分析** - JaCoCo 覆盖率统计
5. **问题修复记录** - 历史问题修复追踪
6. **测试用例统计** - 正常/边界/异常场景分布

---

## 快速开始

### 1. 推送代码到 GitHub

```bash
cd D:\trae_project\exchange-rate-master
git init
git add .
git commit -m "Add GitHub Actions CI/CD"
git remote add origin https://github.com/YOUR_USERNAME/exchange-rate.git
git push -u origin main
```

### 2. 查看 Actions

在 GitHub 仓库页面 → **Actions** 标签页可查看：
- 构建历史
- 测试结果
- 下载构建产物
- 查看 CI 报告

### 3. 下载报告

GitHub Actions 运行完成后，可下载：
- `ci-reports` - CI 聚合报告
- `test-reports` - JUnit 测试报告
- `exchange-rate-jar` - 打包产物

---

## Mock 测试数据

接口自动化测试使用 Mock 数据，包含以下 API：

| 接口 | 路径 | 用例数 |
|------|------|--------|
| 获取币种价格 | `/api/price` | 10 |
| 获取汇率 | `/api/exchange-rate` | 8 |
| 获取历史价格 | `/api/history` | 7 |
| 币种列表 | `/api/coins` | 5 |
| 市场概览 | `/api/market` | 6 |
| 价格转换 | `/api/convert` | 8 |
| 批量查询 | `/api/batch` | 4 |
| 错误处理 | `/api/error` | 2 |

---

## Docker 部署

### 本地运行

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 服务器部署

```bash
# 拉取镜像
docker pull ghcr.io/YOUR_USERNAME/exchange-rate:latest

# 运行容器
docker run -d -p 8080:8080 \
  --name exchange-rate \
  -e SPRING_PROFILES_ACTIVE=prod \
  ghcr.io/YOUR_USERNAME/exchange-rate:latest
```

---

## 本地运行报告生成

```bash
# 安装 Python 依赖
pip install -r requirements.txt  # 如有需要

# 生成报告
python scripts/generate-ci-report.py

# 查看报告
open ci-reports/ci-report-latest.html
```

---

## 自定义配置

### 修改 Java 版本

编辑 `.github/workflows/ci.yml`：

```yaml
env:
  JAVA_VERSION: '11'  # 修改为 8/11/17/21
```

### 修改测试数据

编辑 `src/test/resources/mock-data.json` 或 `scripts/generate-ci-report.py` 中的常量。

---

## 常见问题

### Q: Maven 构建失败？

检查 pom.xml 中的依赖是否可访问，或添加 Maven Mirror 配置。

### Q: 测试跳过？

确保测试类命名符合规范：`*Test.java` 或 `*Tests.java`

### Q: Docker 构建失败？

确保 pom.xml 配置了 Spring Boot Maven Plugin 用于打包 fat jar。

### Q: 报告未生成？

检查 GitHub Actions 日志中 Python 环境设置步骤是否成功。
