# ESL门店演示系统（M1）

M1目标：**可运行 + 登录**。

## 技术栈
- Python 3.11+
- FastAPI
- SQLite
- Jinja2 模板
- Session Cookie（Starlette `SessionMiddleware`）
- 密码哈希（`passlib[bcrypt]`）

## 项目结构

```text
pzd/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── security.py
│   └── templates/
│       ├── dashboard.html
│       └── login.html
├── scripts/
│   └── init_admin.py
├── requirements.txt
└── README.md
```

## 功能清单（M1）
1. `/login` 登录页（表单）
2. 登录成功后跳转 `/dashboard`
3. 未登录访问 `/dashboard` 自动重定向 `/login`
4. SQLite 用户表：`id, username, password_hash, created_at`
5. 提供初始化管理员脚本：`scripts/init_admin.py`

## 安装与运行

### 1) 创建虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) 安装依赖
```bash
pip install -r requirements.txt
```

### 3) 初始化管理员用户
默认账号密码：`admin/admin123`

```bash
python scripts/init_admin.py
```

> 也可使用模块方式运行（更稳妥）：`python -m scripts.init_admin`

可通过参数自定义管理员用户名和密码：
```bash
python scripts/init_admin.py --username your_admin --password "your_password"
```

### 4) 启动服务
```bash
uvicorn app.main:app --reload
```

打开浏览器访问：`http://127.0.0.1:8000/login`

## 最小自检

### 手工验证
1. 访问 `http://127.0.0.1:8000/dashboard`，应重定向到 `/login`。
2. 用错误密码登录，应提示“用户名或密码错误”。
3. 用 `admin/admin123` 登录成功，进入 `/dashboard`。
4. 点击退出后再次访问 `/dashboard`，应再次被重定向到 `/login`。

### curl 示例
未登录访问 `/dashboard` 的重定向检查：
```bash
curl -i http://127.0.0.1:8000/dashboard
```

预期响应头包含：
- `HTTP/1.1 302 Found`
- `location: /login`

## 安全说明
- 用户密码不会明文存储，使用 `passlib[bcrypt]` 进行哈希。
- 会话由 `SessionMiddleware` 管理，登录后以签名 session cookie 标识登录态。

> 生产环境建议：
> - 设置强随机环境变量 `ESL_SECRET_KEY`
> - 部署在 HTTPS 下并启用 `https_only=True`

## M2 预留（本版本不实现）
后续将支持 CSV 导入，格式固定：
- 列：`sku,name,cost,price`
- 编码：UTF-8
- `price` 可为空

