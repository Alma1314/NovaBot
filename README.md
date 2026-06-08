# NovaBot

多平台 LLM 聊天机器人框架，支持接入主流即时通讯平台，提供插件扩展、知识库 RAG、Computer Use 等功能。

> 此项目为 [astrbot](https://github.com/astrbotdevs/astrbot) 的 Fork 版本。

## 环境要求

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)（Python 包管理器）

## 快速开始

```bash
git clone https://github.com/Alma1314/NovaBot.git
cd NovaBot
uv sync
uv run python main.py
```

启动后访问 `http://localhost:6185` 进入 WebUI 管理面板。

> 所有配置保存在 `data/cmd_config.json`，首次启动自动生成默认配置。你也可以通过 WebUI 可视化修改配置。

---

## 配置教程

只需完成两步即可让机器人正常工作：**接入消息平台** → **配置 LLM 提供商**。

### 第一步：接入消息平台

编辑 `data/cmd_config.json`，在 `"platform"` 数组中添加平台配置。以下是常见平台的配置方法。

#### OneBot v11（推荐，支持 QQ/NapCat/LLOneBot）

OneBot v11 是最简单的接入方式。先用 [NapCat](https://github.com/NapNeko/NapCatQQ) 或 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 在本地启动一个 OneBot 服务，然后配置 NovaBot 连接：

```json
{
  "platform": [
    {
      "id": "qq",
      "type": "aiocqhttp",
      "enable": true,
      "ws_reverse_host": "0.0.0.0",
      "ws_reverse_port": 6199,
      "ws_reverse_token": ""
    }
  ]
}
```

| 参数 | 说明 |
|---|---|
| `ws_reverse_host` | 监听地址，`0.0.0.0` 表示接收所有来源 |
| `ws_reverse_port` | 监听端口，需与 OneBot 客户端配置一致 |
| `ws_reverse_token` | 可选，与 OneBot 客户端设置相同的 Token 以启用验证 |

#### Telegram

1. 在 Telegram 找 [@BotFather](https://t.me/BotFather) 创建机器人，获取 Token
2. 配置如下：

```json
{
  "platform": [
    {
      "id": "tg",
      "type": "telegram",
      "enable": true,
      "telegram_token": "你的Bot Token"
    }
  ]
}
```

> 国内网络环境可能需要在 `"http_proxy"` 中配置代理。

#### Discord

1. 在 [Discord Developer Portal](https://discord.com/developers/applications) 创建应用，获取 Bot Token
2. 配置如下：

```json
{
  "platform": [
    {
      "id": "dc",
      "type": "discord",
      "enable": true,
      "discord_token": "你的Bot Token"
    }
  ]
}
```

#### 更多平台

| 平台 | type 值 | 关键参数 |
|---|---|---|
| QQ 官方机器人 | `qq_official` | `appid`, `secret` |
| QQ 官方机器人(Webhook) | `qq_official_webhook` | `appid`, `secret` |
| 飞书 | `lark` | `app_id`, `app_secret` |
| 钉钉 | `dingtalk` | `client_id`, `client_secret` |
| 企业微信 | `wecom` | `corpid`, `secret` |
| 企业微信智能机器人 | `wecom_ai_bot` | `wecomaibot_ws_bot_id`, `wecomaibot_ws_secret` |
| 微信公众平台 | `weixin_official_account` | `appid`, `secret`, `token`, `encoding_aes_key` |
| 个人微信 | `weixin_oc` | `weixin_oc_base_url`, `weixin_oc_token` |
| Slack | `slack` | `bot_token`, `app_token` |
| LINE | `line` | `channel_access_token`, `channel_secret` |
| KOOK | `kook` | `kook_bot_token` |
| Satori | `satori` | `satori_endpoint`, `satori_token` |
| Mattermost | `mattermost` | `mattermost_url`, `mattermost_bot_token` |
| Misskey | `misskey` | `misskey_instance_url`, `misskey_token` |

> 每个平台配置都需要包含 `"id"`（标识名）、`"type"`（平台类型）、`"enable": true` 这三个字段。

### 第二步：配置 LLM 提供商

编辑 `data/cmd_config.json`，在 `"provider_sources"` 数组中添加 LLM 服务商。以下是最常用的配置示例。

#### DeepSeek（推荐）

1. 注册 [DeepSeek](https://platform.deepseek.com/)，获取 API Key
2. 配置如下：

```json
{
  "provider_sources": [
    {
      "id": "deepseek",
      "provider": "deepseek",
      "type": "openai_chat_completion",
      "provider_type": "chat_completion",
      "enable": true,
      "key": ["你的API Key"],
      "api_base": "https://api.deepseek.com/v1",
      "timeout": 120
    }
  ]
}
```

#### OpenAI

```json
{
  "provider_sources": [
    {
      "id": "openai",
      "provider": "openai",
      "type": "openai_chat_completion",
      "provider_type": "chat_completion",
      "enable": true,
      "key": ["你的OpenAI API Key"],
      "api_base": "https://api.openai.com/v1",
      "timeout": 120
    }
  ]
}
```

#### Anthropic Claude

```json
{
  "provider_sources": [
    {
      "id": "anthropic",
      "provider": "anthropic",
      "type": "anthropic_chat_completion",
      "provider_type": "chat_completion",
      "enable": true,
      "key": ["你的Anthropic API Key"],
      "api_base": "https://api.anthropic.com/v1",
      "timeout": 120
    }
  ]
}
```

#### Google Gemini

```json
{
  "provider_sources": [
    {
      "id": "gemini",
      "provider": "google",
      "type": "googlegenai_chat_completion",
      "provider_type": "chat_completion",
      "enable": true,
      "key": ["你的Gemini API Key"],
      "api_base": "https://generativelanguage.googleapis.com/",
      "timeout": 120
    }
  ]
}
```

#### 其他 OpenAI 兼容服务

任何兼容 OpenAI API 格式的服务都可以通过 `"type": "openai_chat_completion"` 接入，只需修改 `"api_base"` 即可：

| 服务 | `api_base` |
|---|---|
| 智谱 (Zhipu) | `https://open.bigmodel.cn/api/paas/v4/` |
| Moonshot | `https://api.moonshot.cn/v1` |
| MiniMax | `https://api.minimaxi.com/v1` |
| xAI (Grok) | `https://api.x.ai/v1` |

#### 设置默认提供商

添加 provider 后，需要指定一个默认使用的提供商。编辑 `"provider_settings"` 中的 `"default_provider_id"`：

```json
{
  "provider_settings": {
    "default_provider_id": "deepseek"
  }
}
```

> 将值改为你在 `provider_sources` 中设置的 `"id"` 名称。

### 第三步：选择模型

在 WebUI 管理面板 `http://localhost:6185` 中，进入「模型」页面，选择你刚配置的提供商，然后手动输入模型名称并保存。

**常用模型名称速查：**

| 提供商 | 推荐模型 |
|---|---|
| DeepSeek | `deepseek-chat` |
| OpenAI | `gpt-4o-mini` |
| Anthropic | `claude-sonnet-4-6` |
| Google Gemini | `gemini-2.5-flash` |
| 智谱 | `glm-4-flash` |

> 也可以在 `provider` 数组中直接配置模型列表（格式参考下方高级配置），但通过 WebUI 操作更直观。

### 第四步：启动并测试

```bash
uv run python main.py
```

在接入的消息平台上发送 `/help`，如果机器人回复，说明配置成功。

---

## 常用功能配置

### 唤醒前缀

默认消息以 `/` 开头才会触发机器人响应。可在全局配置中修改：

```json
{
  "wake_prefix": ["/", "!", "bot "]
}
```

- 私聊默认不需要唤醒前缀。如需私聊也使用前缀，设置 `"platform_settings.friend_message_needs_wake_prefix": true`

### 分段回复（模拟流式输出）

对于不支持流式输出的平台，可以开启分段回复：

```json
{
  "platform_settings": {
    "segmented_reply": {
      "enable": true,
      "split_mode": "words",
      "interval": "1.5,3.5"
    }
  }
}
```

### 联网搜索

```json
{
  "provider_settings": {
    "web_search": true,
    "websearch_provider": "tavily",
    "websearch_tavily_key": ["你的Tavily API Key"]
  }
}
```

### 内容安全

```json
{
  "content_safety": {
    "internal_keywords": {
      "enable": true,
      "extra_keywords": ["违规词1", "违规词2"]
    }
  }
}
```

### 代理配置

```json
{
  "http_proxy": "http://127.0.0.1:7890"
}
```

---

## 环境变量

| 变量名 | 说明 |
|---|---|
| `NOVABOT_ROOT` | 覆盖根目录（默认当前目录） |
| `DEMO_MODE` | 设置为 `True` 启用演示模式 |

> API Key 支持在 `"key"` 字段中使用 `$ENV_VAR` 语法引用环境变量。例如 `"key": ["$OPENAI_API_KEY"]`

---

## CLI 命令

```bash
novabot run                          # 启动
novabot run --reload                 # 启动并启用插件热重载
novabot plug install <name>          # 安装插件
novabot plug uninstall <name>        # 卸载插件
novabot plug list                    # 列出插件
```

---

## 配置参考

### 平台通用设置 (`platform_settings`)

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `unique_session` | `false` | 将所有会话视为独立会话 |
| `reply_with_mention` | `false` | 回复时总是 @ 发送者 |
| `reply_with_quote` | `false` | 回复时总是引用原消息 |
| `friend_message_needs_wake_prefix` | `false` | 私聊消息需要唤醒前缀 |
| `enable_id_white_list` | `true` | 启用 ID 白名单 |
| `id_whitelist` | `[]` | 白名单 ID 列表（用 `/sid` 指令获取会话 ID） |
| `wl_ignore_admin_on_group` | `true` | 管理员在群聊中绕过白名单 |
| `wl_ignore_admin_on_friend` | `true` | 管理员在私聊中绕过白名单 |
| `rate_limit.time` | `60` | 限速窗口（秒） |
| `rate_limit.count` | `30` | 窗口内最大消息数 |
| `rate_limit.strategy` | `"stall"` | 超限策略：`"stall"`（延迟）/ `"discard"`（丢弃） |
| `forward_threshold` | `1500` | 超过此字数后折叠为转发消息（仅 QQ 平台） |

### 提供商全局设置 (`provider_settings`)

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `default_provider_id` | `""` | 默认提供商 ID |
| `fallback_chat_models` | `[]` | 降级模型列表 |
| `max_context_length` | `50` | 最大上下文对话轮数 |
| `context_limit_reached_strategy` | `"llm_compress"` | 上限策略：`"llm_compress"` / `"truncate_by_turns"` |
| `streaming_response` | `false` | 启用流式回复 |
| `max_agent_step` | `30` | Agent 最大推理步数 |
| `tool_call_timeout` | `120` | 工具调用超时（秒） |
| `agent_runner_type` | `"local"` | Agent 运行器：`"local"` / `"dify"` / `"coze"` |

### 分段回复 (`platform_settings.segmented_reply`)

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `enable` | `false` | 启用分段回复 |
| `interval_method` | `"random"` | 间隔方式：`"random"` / `"log"` |
| `interval` | `"1.5,3.5"` | 间隔范围（秒） |
| `words_count_threshold` | `150` | 触发分段的最小字数 |
| `split_mode` | `"regex"` | 切分方式：`"regex"` / `"words"` |

### Web Search

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `provider_settings.web_search` | `false` | 启用联网搜索 |
| `provider_settings.websearch_provider` | `"tavily"` | 搜索提供商：`"tavily"` / `"bocha"` / `"brave"` / `"firecrawl"` |

### TTS / STT

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `provider_tts_settings.enable` | `false` | 启用 TTS |
| `provider_tts_settings.provider_id` | `""` | TTS 提供商 ID |
| `provider_stt_settings.enable` | `false` | 启用 STT |
| `provider_stt_settings.provider_id` | `""` | STT 提供商 ID |

### Computer Use

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `provider_settings.computer_use_runtime` | `"none"` | 运行时：`"none"` / `"cua"` / `"local"` / `"shipyard"` / `"shipyard_neo"` |
| `provider_settings.computer_use_require_admin` | `true` | 仅管理员可用 |

### 知识库 (Knowledge Base)

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `kb_names` | `[]` | 启用的知识库名称列表 |
| `kb_final_top_k` | `5` | 检索返回结果数量 |
| `kb_agentic_mode` | `false` | 启用 Agentic 知识库模式 |

### 插件

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `plugin_set` | `["*"]` | 启用的插件列表，`"*"` 为全部，`[]` 为禁用所有 |
| `disable_builtin_commands` | `false` | 禁用内置命令 |

---

## 许可证

AGPL-3.0-or-later
