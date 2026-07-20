# OpenDesign MCP 连接器配置指南

## 环境要求

- macOS（本指南基于 macOS）
- 已安装 OpenDesign.app（本案例为 v0.15.0，路径 `/Applications/Open Design.app`）
- WorkBuddy 客户端

---

## 工作原理

OpenDesign 在本地运行一个 daemon 进程，MCP server 通过 **Unix Domain Socket (IPC)** 与该 daemon 通信。关键点：

- **daemon 端口是动态分配的**，每次启动可能不同
- **不要硬编码 `OD_DAEMON_URL`**（如 `http://127.0.0.1:58606`），端口会变
- 正确方式是设置 `OD_SIDECAR_IPC_PATH` 环境变量，让 MCP server 通过 IPC socket 自动发现 daemon

```
┌─────────────┐    IPC Socket     ┌──────────────┐
│  WorkBuddy  │ ←───────────────→ │  OpenDesign  │
│  MCP Client │   daemon.sock     │    Daemon    │
└─────────────┘                   └──────────────┘
```

---

## 配置步骤

### 1. 确认 IPC socket 路径

OpenDesign daemon 的 IPC socket 固定路径为：

```
/tmp/open-design/ipc/release-stable/daemon.sock
```

确保 OpenDesign.app 已启动并运行，socket 文件才会存在。

### 2. 编辑 MCP 配置文件

编辑 `~/.workbuddy/mcp.json`，添加以下配置：

```json
{
  "mcpServers": {
    "open-design": {
      "command": "/Applications/Open Design.app/Contents/Frameworks/Open Design Helper.app/Contents/MacOS/Open Design Helper",
      "args": [
        "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs",
        "mcp"
      ],
      "env": {
        "OD_DATA_DIR": "/Users/<你的用户名>/Library/Application Support/Open Design/namespaces/release-stable/data",
        "OD_SIDECAR_IPC_PATH": "/tmp/open-design/ipc/release-stable/daemon.sock",
        "ELECTRON_RUN_AS_NODE": "1"
      },
      "disabled": false
    }
  }
}
```

**各字段说明：**

| 字段 | 说明 |
|------|------|
| `command` | OpenDesign Helper 可执行文件路径（Electron 子进程入口） |
| `args[0]` | daemon-cli.mjs 脚本路径，MCP server 的实现 |
| `args[1]` | 固定参数 `"mcp"`，告诉 daemon-cli 以 MCP 模式运行 |
| `OD_DATA_DIR` | OpenDesign 数据目录，按实际用户名替换 |
| `OD_SIDECAR_IPC_PATH` | **最关键**：daemon 的 IPC socket 路径 |
| `ELECTRON_RUN_AS_NODE` | 让 Electron Helper 以 Node.js 模式运行 |

> **注意**：如果 mcp.json 中已有其他 MCP server 配置，请将 `open-design` 合并到 `mcpServers` 中，不要覆盖已有配置。

### 3. 重启 MCP 进程

修改 `mcp.json` 后，**必须**杀掉旧的 MCP helper 进程，否则配置不生效：

```bash
pkill -f "daemon-cli.mjs.*mcp"
```

### 4. 在 WorkBuddy 中信任连接器

1. 打开 WorkBuddy 的**连接器管理**页面
2. 找到 `open-design` 连接器
3. 点击 **Trust**（信任）按钮

---

## 可用能力

连接成功后，OpenDesign MCP 提供以下工具和能力：

| 工具 | 功能 |
|------|------|
| `capture_screenshot` | 截取设计稿 |
| `capture_layout` | 捕获布局信息 |
| `fetch_file_info` | 获取文件信息 |
| `export_nodes` | 导出设计节点 |
| `scan_exportable_resources` | 扫描可导出资源 |
| `build_style_guide` | 生成设计风格指南 |
| `search_style_guide` | 搜索设计风格 |
| `create_design` | 创建新设计 |
| `open_design` | 打开已有设计 |
| `apply_variables` | 应用设计变量 |
| `batch_read` / `batch_edit` | 批量读写 |
| `upload_images` | 上传图片资源 |
| `fetch_component_lib` | 获取组件库 |

---

## 常见问题

### Q: 配置后显示 disconnected

检查 OpenDesign.app 是否正在运行。IPC socket 只有在 app 运行时才存在。

### Q: 报 `fetch failed` 或连接拒绝

很可能是 `mcp.json` 改了但没有杀旧进程。运行：

```bash
pkill -f "daemon-cli.mjs.*mcp"
```

然后重新 Trust 连接器。

### Q: 端口变化导致连接失败

**不要**在 `mcp.json` 中设置 `OD_DAEMON_URL`。依赖 `OD_SIDECAR_IPC_PATH`（socket 路径）即可，MCP server 会通过 socket 自动获取当前 daemon 的端口。

### Q: 如何确认 OpenDesign 版本

```bash
ls /Applications/ | grep -i "open"
# 或查看 app 包信息
/Applications/Open\ Design.app/Contents/Info.plist
```

路径中的 `release-stable` 对应发布通道，一般不需要修改。

---

## 参考

- OpenDesign 安装路径：`/Applications/Open Design.app`
- MCP 脚本：`/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs`
- 配置日期：2026-07-16，验证通过
