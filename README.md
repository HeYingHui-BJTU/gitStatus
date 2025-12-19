# 禾盈慧 (HeYingHui) - 多仓库协作统计展示

本仓库用于展示**禾盈慧项目**三个核心子仓库（frontend、backend、dataCenter）的协作统计数据，支持通过 GitHub Pages 公网访问。

## 🎯 项目简介

**禾盈慧**是一个综合性项目，包含三个主要模块：
- **前端模块 (Frontend)**: 用户界面与交互设计
- **后端模块 (Backend)**: 服务端架构与业务逻辑
- **数据中心 (DataCenter)**: 数据采集、分析与智能预测

## 👥 团队成员

- **蒲显科** (Nahjs)
- **曹棪** (QICY520)
- **宁苏颜** (YDUTSEVOLDN)
- **黄光景** (Jared-1019)
- **张琪** (Camelli-a)

## 📊 统计功能

本系统提供以下深度分析：

✅ **贡献者排行榜**: 统计各成员提交次数、代码行数变更、修改文件数等  
✅ **提交历史时间线**: 可视化展示项目演进过程  
✅ **活跃时段分析**: 按小时/星期统计团队工作节奏  
✅ **文件类型分布**: Top 10 文件类型统计  
✅ **月度提交趋势**: 最近12个月的活跃度变化

## 🚀 快速开始

### 生成统计报告

```bash
# 克隆本仓库
git clone git@github.com:HeYingHui-BJTU/gitStatus.git
cd gitStatus

# 生成统计（需要 Python3）
python3 generate_stats.py /path/to/backend project-reports/backend_stats "后端模块 (Backend)"
python3 generate_stats.py /path/to/frontend project-reports/frontend_stats "前端模块 (Frontend)"
python3 generate_stats.py /path/to/dataCenter project-reports/dataCenter_stats "数据中心 (DataCenter)"
```

### 部署到 GitHub Pages

1. 推送到 GitHub:
```bash
git add .
git commit -m "docs: 更新协作统计报告"
git push origin main
```

2. 配置 GitHub Pages:
   - 进入仓库 **Settings** → **Pages**
   - Source 选择 `main` 分支 / `root` 目录
   - 点击 Save

3. 访问地址（部署完成后约1-2分钟）:
```
https://heyinghui-bjtu.github.io/gitStatus/project-reports/
```

## 📁 目录结构

```
gitStatus/
├── README.md                      # 项目说明
├── generate_stats.py              # 统计生成脚本
├── project-reports/               # 统计报告输出目录
│   ├── index.html                 # 总门户页面
│   ├── backend_stats/
│   │   └── index.html             # 后端统计
│   ├── frontend_stats/
│   │   └── index.html             # 前端统计
│   └── dataCenter_stats/
│       └── index.html             # 数据中心统计
└── tools/                         # 工具目录（可选）
```

## 🎨 特性亮点

### 💎 心流式用户体验
- 渐进式动画加载，提供沉浸式浏览体验
- 响应式设计，支持移动端与桌面端
- 平滑滚动与交互反馈

### 🔍 数据可视化
- 直观的条形图展示活跃度分布
- 时间线可视化提交历史
- 颜色编码的数据标签

### 👤 智能姓名映射
- 自动将 Git 用户名映射到真实姓名
- 保留原始用户名以便追溯

## 📝 汇报模版（给老师）

```
[课程作业] 禾盈慧项目协作深度分析报告

我们团队开发的禾盈慧项目涉及 3 个核心仓库，通过对 Git 提交日志的聚合分析，
全方位展示了成员贡献、活跃时段及协作趋势：

🔗 在线访问地址：
https://heyinghui-bjtu.github.io/gitStatus/project-reports/

报告包含：
✓ 贡献者排行榜: 统计各成员提交次数与代码行数（贡献比）
✓ 提交历史时间线: 可视化展示项目演进过程  
✓ 活跃时段分析: 展示团队协作的活跃时段（工作节奏）
✓ 文件类型分布: 分析核心代码文件的类型组成
✓ 月度提交趋势: 观察项目活跃度的时间变化

团队成员：蒲显科、曹棪、宁苏颜、黄光景、张琪
```

## 🔧 维护说明

每次需要更新统计数据时：

1. 在本地重新运行 `generate_stats.py`
2. 提交并推送到 main 分支
3. GitHub Pages 将自动部署更新（约1-2分钟）

## 📄 License

本项目仅用于学术展示，禁止商业用途。

---

**禾盈慧项目组** © 2025
