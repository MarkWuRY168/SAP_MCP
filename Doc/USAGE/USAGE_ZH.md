# SAP MCP 操作指南

本文档提供了 SAP MCP 项目的详细安装、配置和使用步骤。

## 目录

1. [前置条件](#前置条件)
2. [SAP Http接口服务激活](#sap-http接口服务激活)
3. [手动部署](#手动部署)
4. [使用指南](#使用指南)
5. [常见问题](#常见问题)

---

## 前置条件

- Python 3.8 或更高版本
- Git（可选，用于克隆仓库）
- 网络连接（用于安装依赖）
- 拥有SAP系统管理员权限

---

## SAP Http接口服务激活

在安装本项目前，需要在SAP系统中激活Http接口服务。请按照以下步骤操作：

### 步骤1：SAP系统程序代码导入

查看 SAP 请求导入程序文档，地址：`Request\SAP Request\Y_UPLOAD_TRANSPORT_REQUEST.md`

### 步骤2：执行SAP请求导入程序

执行SAP请求导入程序，导入开发包。

![SAP请求导入](/Doc/Picture/image-1.png)

### 步骤3：SICF激活ZMCP服务

使用事务码 SICF 激活 ZMCP 服务，并测试服务正常使用。

![SICF服务激活](/Doc/Picture/image-2.png)

### 步骤4：事务码ZMCP_CONFIG配置SAP工具列表

使用事务码 ZMCP_CONFIG 配置 SAP 工具列表。

![工具配置](/Doc/Picture/image-3.png)

SAP工具示例数据：
|MCP工具ID|启用标识|MCP名称|工具描述|版本号|超时时间（秒）|重发次数|优先级|种类|标签|类型|名称|指示器|指示器|创建人员|创建日期|创建时间|修改人员|修改日期|修改时间|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|CHECK_MATNR|X|检查物料号|Enter the material number and return the|0|10|0|2|MM|MM|FUNC|BAPI_MATERIAL_EXISTENCECHECK|||||0:00:00|||0:00:00|
|GET_MATNR_DETAILS|X|取得物料明细|Enter the material number to obtain the|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_DETAILS|||||0:00:00|||0:00:00|
|GET_MATNR_FROM_DES|X|取得物料编号|Enter material description and language|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_LIST|X|取得工厂下物料清单|Enter the factory number to obtain all m|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_MATNR_LIST|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_STOC|X|取得工厂下仓库清单|Enter the material number and factory nu|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_WERKS_STOCK|||||0:00:00|||0:00:00|
|GET_PERNR_FROM_DES|X|取得员工号|Enter name to obtain employee ID|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_PERNR_ORG|X|取得组织信息|Enter the employee ID and query date to|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_ORG|||||0:00:00|||0:00:00|
|GET_PERNR_WORK_PLAN|X|取得工作计划|Enter the employee ID and year/month to|0|10|0|2|PT|PT|FUNC|ZMCP_GET_PERNR_WORK_PLAN|||||0:00:00|||0:00:00|
|GET_WERKS_FROM_DES|X|取得工厂号|Enter factory description to obtain fact|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_FROM_DES|||||0:00:00|||0:00:00|
|REVERSE_MATERIAL|X|冲销物料凭证|Enter material voucher information to re|0|10|0|2|MM|MM|FUNC|BAPI_GOODSMVT_CANCEL|||||0:00:00|||0:00:00|
|TOOL_DETAIL|X|工具明细|Tool detail|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_DETAIL|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_LIST|X|工具清单|Tool list|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_LIST|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_USED|X|工具使用|Use tool|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_USED|X|X|ADMIN||0:00:00|||0:00:00|

---

## 手动部署

### 1.1 获取项目代码

**方法 1：从 Git 仓库克隆**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**方法 2：直接复制文件**
- 将整个项目文件夹复制到您的服务器

### 1.2 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 1.3 安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 1.4 配置项目

```bash
# 复制配置示例文件
cp utils/config.example.py utils/config.py

# 编辑配置文件（根据您的环境修改）
# 您可以使用任何文本编辑器，例如
# notepad config.py      # Windows
# vim config.py          # Linux/Mac
```

**配置文件示例：**
```python
# SAP 接口配置
SAP_CONFIG = {
    "base_url": "http://your-sap-server:port/sap/zmcp",
    "client_id": "your-client-id",
    "sap-user": "your-sap-username",
    "sap-password": "your-sap-password",
    "timeout": 30
}

# MCP 服务器配置
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6688,
    "path": "/mcp"
}

# WEB 服务器配置
WEB_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6680,
    "reload": False
}
```

**环境变量配置：**

项目支持通过环境变量配置敏感信息，避免硬编码。以下是支持的环境变量：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| MCP_HOST | MCP服务器主机 | 0.0.0.0 |
| MCP_PORT | MCP服务器端口 | 6688 |
| MCP_PATH | MCP服务器路径 | /mcp |
| WEB_HOST | Web服务器主机 | 0.0.0.0 |
| WEB_PORT | Web服务器端口 | 6680 | 
| WEB_RELOAD | Web服务器自动重载（开发环境） | True |
| SAP_BASE_URL | SAP接口基础URL | - |
| SAP_CLIENT_ID | SAP客户端ID | - |
| SAP_SAP_USER | SAP用户名 | - |
| SAP_SAP_PASSWORD | SAP密码 | - |
| SAP_TIMEOUT | SAP请求超时时间（秒） | 30 |

您可以在启动服务前设置这些环境变量，或者创建一个 `.env` 文件来存储它们。

### 1.5 启动服务

#### 方法 1：仅启动 MCP 服务器

```bash
# 启动 MCP 服务器
python server/sap_mcp_server.py
```

#### 方法 2：启动 Web 管理界面

```bash
# 启动 Web 管理界面
python web/main.py
```

或者使用 uvicorn 直接启动：

```bash
# 启动 Web 管理界面
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

---

## 使用指南

### 访问 Web 管理界面

启动服务后，在浏览器中打开：`http://localhost:6680`

### 服务管理页面

1. **查看服务状态**：显示 MCP 服务的当前运行状态
2. **启动服务**：点击"启动服务"按钮启动 MCP 服务器
3. **停止服务**：点击"停止服务"按钮停止 MCP 服务器
4. **查看日志**：实时查看服务运行日志

### 工具管理页面

1. **查看工具列表**：左侧显示所有可用的 SAP 工具
2. **搜索工具**：使用搜索框快速查找工具
3. **查看工具详情**：点击工具列表中的工具，右侧显示工具详情和参数
4. **执行工具**：
   - 在参数表单中填写参数值
   - 点击"执行工具"按钮
   - 查看执行结果

### 服务器配置页面

1. **SAP接口配置**：
   - 基础 URL
   - 客户端 ID
   - SAP 用户名
   - SAP 密码
   - 超时时间

2. **MCP服务器配置**：
   - 主机地址
   - 端口
   - 路径

3. **接口测试**：点击"接口测试"按钮验证 SAP 接口连接

4. **保存配置**：点击"保存配置"按钮保存所有配置

### 日志查看页面

1. **刷新日志**：点击"刷新日志"按钮查看最新日志
2. **日志级别过滤**：选择日志级别进行过滤
3. **清空日志**：点击"清空日志"按钮清空所有日志

---

## 配置 AI 工具

### 支持的 AI 工具类型

本服务可以集成到多种 AI 工具中，包括：
- **聊天工具**：如 ChatGPT、Cherry Studio
- **编程工具**：如 Cursor、Claude Code
- **平台工具**：如 LangChain、Dify

### 配置 MCP 服务地址

在您的 AI 工具中配置 MCP 服务地址为：

```json 
{
  "SAP_MCP": {
    "transport": "streamable_http",
    "url": "http://localhost:6688/mcp"
  }
}
```

---

## 常见问题

### MCP 服务无法访问

**问题**：通过 Web 管理界面启动 MCP 服务后，无法从外部访问。

**解决方案**：

1. 确保 MCP 服务器配置的 host 为 `0.0.0.0`（而不是 `127.0.0.1`）
2. 确保端口映射正确配置
3. 检查防火墙设置

### 配置文件修改后不生效

**问题**：修改配置文件后，服务没有使用新配置。

**解决方案**：

1. 重启 Web 管理界面服务
2. 停止并重新启动 MCP 服务

---

## 技术支持

如有问题，请联系：

- **产品设计**: Mark (Wu Rangyu)
- **开发者**: Mark (Wu Rangyu)
- **电话**: 18685095797
- **QQ**: 121980331
- **邮箱**: 121980331@qq.com
