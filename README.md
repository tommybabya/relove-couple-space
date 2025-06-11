# ReLove 情侣空间

一个现代化的情侣空间应用，帮助情侣记录和分享美好时光。

## 功能特点

### 用户端功能
- 📸 相册管理：上传和分享照片，创建专属相册
- 📅 情侣日历：记录重要日期和纪念日
- 💬 留言板：发送文字、表情和图片消息
- ✅ 100件事清单：共同规划和完成愿望清单
- 👤 个人资料：自定义个人信息和偏好设置

### 管理端功能
- 👥 用户管理：查看和管理用户信息
- 📁 内容管理：管理相册、消息和任务
- 📊 数据统计：查看系统使用情况和统计数据
- ⚙️ 系统设置：配置系统参数和功能选项

## 技术栈

### 前端
- Next.js 13 (App Router)
- TypeScript
- Tailwind CSS
- Shadcn/ui 组件库
- Lucide Icons

### 后端
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT 认证
- Python 3.11

## 项目结构

```
.
├── src/                  # 前端源代码
│   ├── app/             # Next.js 页面
│   ├── components/      # React 组件
│   ├── lib/            # 工具函数
│   └── hooks/          # React Hooks
├── backend/             # 后端源代码
│   ├── app/            # FastAPI 应用
│   │   ├── main.py     # 主应用入口
│   │   ├── models.py   # 数据模型
│   │   ├── schemas.py  # Pydantic 模型
│   │   └── auth.py     # 认证模块
│   └── requirements.txt # Python 依赖
└── docker/             # Docker 配置文件
```

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/yourusername/relove-app.git
cd relove-app
```

2. 使用 Docker Compose 启动项目
```bash
docker-compose up -d
```

3. 访问应用
- 用户端: http://localhost:8000
- 管理端: http://localhost:8000/admin
- API 文档: http://localhost:8080/docs

## 开发环境设置

### 前端开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 后端开发
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
cd backend
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --port 8080
```

## 部署

项目使用 Docker Compose 进行部署，包含以下服务：
- Frontend: Next.js 应用
- Backend: FastAPI 应用
- Database: PostgreSQL 数据库

### 部署步骤
1. 确保服务器已安装 Docker 和 Docker Compose
2. 配置环境变量
3. 运行 `docker-compose up -d`
4. 配置 Nginx 反向代理（可选）

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
