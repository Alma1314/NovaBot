# NovaBot

多平台 LLM 聊天机器人框架，支持接入主流即时通讯平台，提供插件扩展、知识库 RAG、Computer Use 等功能。

> 此项目为 [astrbot](https://github.com/astrbotdevs/astrbot) 的 Fork 版本。

## 环境要求

- Python >= 3.13
- 包管理器：[uv](https://docs.astral.sh/uv/)（推荐）

## 安装


需要安装uv。
```bash
# 克隆仓库
git clone https://github.com/NovaBotDevs/NovaBot.git
cd NovaBot

# 安装依赖
uv sync

# 启动
uv run python main.py
```

首次启动后，会在 `data/` 目录下自动生成默认配置文件 `data/cmd_config.json`。

## 配置说明

NovaBot 的主配置文件为 `data/cmd_config.json`，首次运行时会自动生成默认配置。以下按功能分类说明所有配置项。

---

### 基础配置

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `config_version` | int | `2` | 配置文件版本号，用于兼容升级 |
| `timezone` | string | `"Asia/Shanghai"` | 服务器时区 |
| `log_level` | string | `"INFO"` | 日志级别，可选 `DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL` |
| `log_file_enable` | bool | `false` | 是否启用文件日志 |
| `log_file_path` | string | `"logs/novabot.log"` | 日志文件路径 |
| `log_file_max_mb` | int | `20` | 日志文件最大大小（MB） |
| `trace_enable` | bool | `false` | 是否启用 Trace 级别日志 |
| `trace_log_enable` | bool | `false` | 是否启用 Trace 日志文件 |
| `trace_log_path` | string | `"logs/novabot.trace.log"` | Trace 日志文件路径 |
| `trace_log_max_mb` | int | `20` | Trace 日志文件最大大小（MB） |
| `temp_dir_max_size` | int | `1024` | 临时目录最大大小（MB） |
| `wake_prefix` | list | `["/"]` | 唤醒前缀，消息以此开头时触发机器人响应 |
| `admins_id` | list | `["novabot"]` | 管理员 ID 列表 |
| `callback_api_base` | string | `""` | 回调 API 基础地址 |

### 网络代理

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `http_proxy` | string | `""` | HTTP/HTTPS 代理地址，例如 `http://127.0.0.1:7890` |
| `no_proxy` | list | `["localhost", "127.0.0.1", "::1", "10.*", "192.168.*"]` | 不走代理的地址列表，支持通配符 |
| `pip_install_arg` | string | `""` | pip 安装时的额外参数，例如 `--proxy http://127.0.0.1:7890` |
| `pypi_index_url` | string | `"https://mirrors.aliyun.com/pypi/simple/"` | PyPI 镜像源地址 |

---

### 平台配置 (`platform`)

`platform` 是一个列表，每个元素代表一个消息平台适配器。每个适配器需包含：

- `id`: 适配器标识名称
- `type`: 适配器类型（见下表）
- `enable`: 是否启用（`true`/`false`）
- 平台特定的认证参数

#### 支持的消息平台

| 平台 | type 值 | 连接方式 | 关键参数 |
|---|---|---|---|
| QQ 官方机器人 | `qq_official` | WebSocket | `appid`, `secret`, `enable_group_c2c`, `enable_guild_direct_message` |
| QQ 官方机器人(Webhook) | `qq_official_webhook` | Webhook | `appid`, `secret`, `is_sandbox`, `webhook_uuid` |
| OneBot v11 | `aiocqhttp` | 反向 WebSocket | `ws_reverse_host`, `ws_reverse_port`, `ws_reverse_token` |
| 微信公众平台 | `weixin_official_account` | Webhook | `appid`, `secret`, `token`, `encoding_aes_key` |
| 企业微信 | `wecom` | Webhook | `corpid`, `secret`, `token`, `encoding_aes_key` |
| 企业微信智能机器人 | `wecom_ai_bot` | 长连接/Webhook | `wecomaibot_ws_bot_id`/`wecomaibot_ws_secret` (长连接) 或 `wecomaibot_token`/`wecomaibot_encoding_aes_key` (Webhook) |
| 个人微信 | `weixin_oc` | iLinkka 协议 | `weixin_oc_base_url`, `weixin_oc_bot_type`, `weixin_oc_token` |
| 飞书(Lark) | `lark` | 长连接/Webhook | `app_id`, `app_secret`, `lark_connection_mode` |
| 钉钉(DingTalk) | `dingtalk` | Stream 模式 | `client_id`, `client_secret`, `card_template_id` |
| Telegram | `telegram` | 长轮询 | `telegram_token`, `telegram_api_base_url` |
| Discord | `discord` | Gateway | `discord_token`, `discord_proxy` |
| Slack | `slack` | Socket/Webhook | `bot_token`, `app_token`, `slack_connection_mode` |
| LINE | `line` | Webhook | `channel_access_token`, `channel_secret` |
| KOOK | `kook` | WebSocket | `kook_bot_token` |
| Satori | `satori` | WebSocket | `satori_endpoint`, `satori_token` |
| Mattermost | `mattermost` | WebSocket | `mattermost_url`, `mattermost_bot_token` |
| Misskey | `misskey` | WebSocket + REST | `misskey_instance_url`, `misskey_token` |

#### 平台配置示例

```json
{
  "platform": [
    {
      "id": "my-qq-bot",
      "type": "aiocqhttp",
      "enable": true,
      "ws_reverse_host": "0.0.0.0",
      "ws_reverse_port": 6199,
      "ws_reverse_token": ""
    },
    {
      "id": "my-telegram",
      "type": "telegram",
      "enable": true,
      "telegram_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    }
  ]
}
```

---

### 平台通用设置 (`platform_settings`)

#### 消息处理

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `unique_session` | bool | `false` | 将所有会话视为独立会话 |
| `wake_prefix` | string | `""` | 平台级额外唤醒前缀（与全局前缀叠加） |
| `reply_prefix` | string | `""` | 机器人回复前缀 |
| `reply_with_mention` | bool | `false` | 回复时总是 @ 发送者 |
| `reply_with_quote` | bool | `false` | 回复时总是引用原消息 |
| `friend_message_needs_wake_prefix` | bool | `false` | 私聊消息需要唤醒前缀 |
| `ignore_bot_self_message` | bool | `false` | 忽略机器人自己的消息 |
| `ignore_at_all` | bool | `false` | 忽略 @全体成员 消息 |
| `empty_mention_waiting` | bool | `true` | 仅 @机器人 时进入等待状态，后续消息触发响应 |
| `empty_mention_waiting_need_reply` | bool | `true` | 等待状态下机器人回复确认 |
| `no_permission_reply` | bool | `true` | 权限不足时回复提示 |

#### 白名单

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable_id_white_list` | bool | `true` | 启用 ID 白名单 |
| `id_whitelist` | list | `[]` | 白名单 ID 列表，为空则不限制。使用 `/sid` 指令获取会话 ID |
| `id_whitelist_log` | bool | `true` | 白名单拒绝时输出日志 |
| `wl_ignore_admin_on_group` | bool | `true` | 管理员在群聊中绕过白名单 |
| `wl_ignore_admin_on_friend` | bool | `true` | 管理员在私聊中绕过白名单 |

#### 分段回复 (`segmented_reply`)

将长消息拆分为多个消息片段的"流式输出"模拟。

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `segmented_reply.enable` | bool | `false` | 启用分段回复 |
| `segmented_reply.only_llm_result` | bool | `true` | 仅对 LLM 结果分段 |
| `segmented_reply.interval_method` | string | `"random"` | 分段间隔方式，`random` 或 `log` |
| `segmented_reply.interval` | string | `"1.5,3.5"` | random 模式下的间隔范围（秒），逗号分隔 |
| `segmented_reply.log_base` | float | `2.6` | log 模式下的对数基数 |
| `segmented_reply.words_count_threshold` | int | `150` | 超过此字数触发分段 |
| `segmented_reply.split_mode` | string | `"regex"` | 切分方式，`regex` 或 `words` |
| `segmented_reply.regex` | string | `".*?[。？！~…]+\|.+$"` | regex 模式下的切分正则 |
| `segmented_reply.split_words` | list | `["。","？","！","~","…"]` | words 模式下的切分字符 |
| `segmented_reply.content_cleanup_rule` | string | `""` | 内容清理规则 |

#### 限速与折叠

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rate_limit.time` | int | `60` | 限速窗口（秒） |
| `rate_limit.count` | int | `30` | 窗口内最大消息数 |
| `rate_limit.strategy` | string | `"stall"` | 限速策略，`stall`（延迟处理）或 `discard`（丢弃） |
| `forward_threshold` | int | `1500` | 超过此字数后消息折叠为"转发消息"（仅 QQ 平台） |
| `path_mapping` | list | `[]` | 文件路径映射，格式 `"<原路径>:<映射路径>"` |

---

### LLM 提供商配置

#### `provider_sources` — 提供商源

定义 LLM API 源，每个源包含以下通用字段：

| 参数 | 类型 | 说明 |
|---|---|---|
| `id` | string | 提供商标识名称 |
| `provider` | string | 提供商标签 |
| `type` | string | 适配器类型（见下方支持列表） |
| `provider_type` | string | 提供商种类：`chat_completion` / `tts` / `stt` / `embedding` / `rerank` |
| `enable` | bool | 是否启用 |
| `key` | list | API Key 列表，支持 `$ENV_VAR` 语法引用环境变量 |
| `api_base` | string | API 端点地址 |
| `timeout` | int | 请求超时时间（秒），默认 120 |
| `proxy` | string | 代理地址 |
| `custom_headers` | object | 自定义请求头 |

#### 支持的 Chat Completion 提供商

| 提供商 | type 值 | 默认 API Base |
|---|---|---|
| OpenAI 兼容 | `openai_chat_completion` | `https://api.openai.com/v1` |
| Anthropic | `anthropic_chat_completion` | `https://api.anthropic.com/v1` |
| Google Gemini | `googlegenai_chat_completion` | `https://generativelanguage.googleapis.com/` |
| Zhipu (智谱) | `zhipu_chat_completion` | `https://open.bigmodel.cn/api/paas/v4/` |
| xAI | `xai_chat_completion` | `https://api.x.ai/v1` |
| Moonshot | 使用 `openai_chat_completion` | `https://api.moonshot.cn/v1` |
| DeepSeek | 使用 `openai_chat_completion` | `https://api.deepseek.com/v1` |
| MiniMax | 使用 `openai_chat_completion` | `https://api.minimaxi.com/v1` |
| Kimi Coding Plan | `kimi_code_chat_completion` | `https://api.kimi.com/coding` |
| MiniMax Token Plan | `minimax_token_plan` | `https://api.minimaxi.com/anthropic` |
| Xiaomi (Mimo) | `xiaomi_chat_completion` | `https://api.xiaomimimo.com/v1` |
| Xiaomi Token Plan | `xiaomi_token_plan` | `https://token-plan-cn.xiaomimimo.com/anthropic` |

> 任何提供 OpenAI 兼容 API 的服务都可以通过 `openai_chat_completion` 接入。

#### 提供商配置示例

```json
{
  "provider_sources": [
    {
      "id": "deepseek",
      "provider": "deepseek",
      "type": "openai_chat_completion",
      "provider_type": "chat_completion",
      "enable": true,
      "key": ["$DEEPSEEK_API_KEY"],
      "api_base": "https://api.deepseek.com/v1",
      "timeout": 120,
      "proxy": "",
      "custom_headers": {}
    }
  ]
}
```

#### `provider_settings` — 提供商全局设置

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable` | bool | `true` | 启用 LLM 提供商系统 |
| `default_provider_id` | string | `""` | 默认使用的提供商 ID |
| `fallback_chat_models` | list | `[]` | 降级模型列表，当前模型不可用时依次尝试 |
| `default_image_caption_provider_id` | string | `""` | 默认图片描述提供商 ID |
| `image_caption_prompt` | string | `"Please describe the image using Chinese."` | 图片描述提示词 |
| `provider_pool` | list | `["*"]` | 启用的提供商池，`["*"]` 表示全部 |
| `reachability_check` | bool | `false` | 检查模型可达性 |

---

### 对话与上下文

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `prompt_prefix` | string | `"{{prompt}}"` | 提示词模板前缀 |
| `default_personality` | string | `"default"` | 默认人设/人格标识 |
| `persona_pool` | list | `["*"]` | 启用的人格池，`["*"]` 为全部 |
| `datetime_system_prompt` | bool | `true` | 在 system prompt 中注入当前时间 |
| `display_reasoning_text` | bool | `false` | 显示模型推理文字 |
| `identifier` | bool | `false` | 在回复中显示提供商标识 |
| `group_name_display` | bool | `false` | 在上下文中显示群名 |
| `max_context_length` | int | `50` | 最大上下文对话轮数 |
| `dequeue_context_length` | int | `10` | 超出上下文时移除的轮数 |
| `context_limit_reached_strategy` | string | `"llm_compress"` | 上下文上限策略：`llm_compress`（LLM 压缩）或 `truncate_by_turns`（按轮截断） |
| `llm_compress_instruction` | string | (内置) | LLM 上下文压缩指令 |
| `llm_compress_keep_recent_ratio` | float | `0.15` | 压缩后保留的最近历史比例 |
| `llm_compress_provider_id` | string | `""` | 压缩用的提供商 ID（空则使用聊天同一提供商） |

#### 流式与工具

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `streaming_response` | bool | `false` | 启用流式回复 |
| `unsupported_streaming_strategy` | string | `"realtime_segmenting"` | 不支持流式的模型采用的策略 |
| `show_tool_use_status` | bool | `false` | 显示工具调用状态 |
| `show_tool_call_result` | bool | `false` | 显示工具调用结果 |
| `buffer_intermediate_messages` | bool | `false` | 缓冲中间消息 |
| `max_agent_step` | int | `30` | Agent 最大推理步数 |
| `tool_call_timeout` | int | `120` | 工具调用超时（秒） |
| `tool_schema_mode` | string | `"full"` | 工具 Schema 模式 |
| `sanitize_context_by_modalities` | bool | `false` | 按内容类型清理上下文 |
| `max_quoted_fallback_images` | int | `20` | 最大引用回退图片数 |

#### 引用消息解析 (`quoted_message_parser`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `max_component_chain_depth` | int | `4` | 最大组件链深度 |
| `max_forward_node_depth` | int | `6` | 最大转发节点深度 |
| `max_forward_fetch` | int | `32` | 最大转发抓取数 |
| `warn_on_action_failure` | bool | `false` | 操作失败时发出警告 |

#### 安全

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `llm_safety_mode` | bool | `true` | 启用 LLM 安全过滤 |
| `safety_mode_strategy` | string | `"system_prompt"` | 安全模式策略类型 |
| `image_compress_enabled` | bool | `true` | 启用图片压缩 |
| `image_compress_options.max_size` | int | `1280` | 图片压缩最大边长 |
| `image_compress_options.quality` | int | `95` | JPEG 压缩质量 |

---

### Web Search（联网搜索）

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `web_search` | bool | `false` | 启用联网搜索 |
| `websearch_provider` | string | `"tavily"` | 搜索提供商：`tavily` / `bocha` / `brave` / `firecrawl` |
| `websearch_tavily_key` | list | `[]` | Tavily API Key 列表 |
| `websearch_bocha_key` | list | `[]` | Bocha API Key 列表 |
| `websearch_brave_key` | list | `[]` | Brave API Key 列表 |
| `websearch_firecrawl_key` | list | `[]` | Firecrawl API Key 列表 |
| `websearch_baidu_app_builder_key` | string | `""` | Baidu App Builder API Key |
| `web_search_link` | bool | `false` | 显示搜索结果链接 |

---

### Agent Runner

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `agent_runner_type` | string | `"local"` | Agent 运行器类型：`local` / `dify` / `coze` / `dashscope` / `deerflow` |
| `dify_agent_runner_provider_id` | string | `""` | Dify 运行器提供商 ID |
| `coze_agent_runner_provider_id` | string | `""` | Coze 运行器提供商 ID |
| `dashscope_agent_runner_provider_id` | string | `""` | DashScope 运行器提供商 ID |
| `deerflow_agent_runner_provider_id` | string | `""` | DeerFlow 运行器提供商 ID |

---

### Computer Use（计算机使用）

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `computer_use_runtime` | string | `"none"` | Computer Use 运行时：`none` / `cua` / `local` / `shipyard` / `shipyard_neo` / `boxlite` |
| `computer_use_require_admin` | bool | `true` | 仅管理员可使用 Computer Use |

#### Sandbox 沙箱配置 (`sandbox`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `booter` | string | `"shipyard_neo"` | 沙箱启动器类型 |
| `shipyard_endpoint` | string | `""` | Shipyard API 端点 |
| `shipyard_access_token` | string | `""` | Shipyard 访问令牌 |
| `shipyard_ttl` | int | `3600` | Shipyard 会话 TTL（秒） |
| `shipyard_max_sessions` | int | `10` | Shipyard 最大并发会话数 |
| `shipyard_neo_endpoint` | string | `""` | Shipyard Neo API 端点 |
| `shipyard_neo_access_token` | string | `""` | Shipyard Neo 访问令牌 |
| `shipyard_neo_profile` | string | `"python-default"` | Shipyard Neo 配置档 |
| `shipyard_neo_ttl` | int | `3600` | Shipyard Neo 会话 TTL（秒） |

---

### TTS / STT（语音合成与识别）

#### TTS 设置 (`provider_tts_settings`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable` | bool | `false` | 启用 TTS |
| `provider_id` | string | `""` | TTS 提供商 ID |
| `dual_output` | bool | `false` | 同时输出文本和语音 |
| `use_file_service` | bool | `false` | 使用文件服务发送语音 |
| `trigger_probability` | float | `1.0` | TTS 触发概率（0-1） |

支持的 TTS 提供商：`azure_tts`、`edge_tts`、`dashscope_tts`、`fishaudio_tts_api`、`gemini_tts`、`genie_tts`、`gsvi_tts`、`mimo_tts_api`、`minimax_tts_api`、`openai_tts_api`、`volcengine_tts`

#### STT 设置 (`provider_stt_settings`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable` | bool | `false` | 启用 STT |
| `provider_id` | string | `""` | STT 提供商 ID |

支持的 STT 提供商：`whisper_api`、`whisper_selfhosted`、`mimo_stt_api`、`xinference_stt`

---

### 文件提取 (`file_extract`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable` | bool | `false` | 启用文件内容提取 |
| `provider` | string | `"moonshotai"` | 提取提供商 |
| `moonshotai_api_key` | string | `""` | Moonshot AI API Key |

---

### 知识库 (Knowledge Base)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `kb_names` | list | `[]` | 启用的知识库名称列表 |
| `kb_fusion_top_k` | int | `20` | 融合阶段检索返回数量 |
| `kb_final_top_k` | int | `5` | 最终返回结果数量 |
| `kb_agentic_mode` | bool | `false` | 启用 Agentic 知识库模式 |

#### LTM（长期记忆）设置 (`provider_ltm_settings`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `group_icl_enable` | bool | `false` | 启用群聊上下文学习 |
| `group_message_max_cnt` | int | `300` | 群聊消息最大缓存数 |
| `image_caption` | bool | `false` | 是否为图片生成描述 |
| `image_caption_provider_id` | string | `""` | 图片描述提供商 ID |
| `active_reply.enable` | bool | `false` | 启用主动回复 |
| `active_reply.method` | string | `"possibility_reply"` | 主动回复方法 |
| `active_reply.possibility_reply` | float | `0.1` | 主动回复概率 |
| `active_reply.whitelist` | list | `[]` | 主动回复白名单 |

---

### 内容安全 (`content_safety`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `also_use_in_response` | bool | `false` | 也对机器人回复进行内容审核 |
| `internal_keywords.enable` | bool | `true` | 启用关键词过滤 |
| `internal_keywords.extra_keywords` | list | `[]` | 额外屏蔽关键词，支持正则 |
| `baidu_aip.enable` | bool | `false` | 启用百度 AIP 内容审核 |
| `baidu_aip.app_id` | string | `""` | 百度 AIP App ID |
| `baidu_aip.api_key` | string | `""` | 百度 AIP API Key |
| `baidu_aip.secret_key` | string | `""` | 百度 AIP Secret Key |

> 使用百度 AIP 审核需手动安装：`pip3 install baidu-aip`

---

### T2I（Text-to-Image 文本转图片）

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `t2i` | bool | `false` | 启用 T2I 渲染 |
| `t2i_word_threshold` | int | `150` | 触发 T2I 的最小字数 |
| `t2i_strategy` | string | `"remote"` | 渲染策略：`remote` 或 `local` |
| `t2i_endpoint` | string | `""` | T2I 端点 URL |
| `t2i_use_file_service` | bool | `false` | 使用文件服务发送渲染结果 |
| `t2i_active_template` | string | `"base"` | 活跃 T2I 模板名称 |

---

### SubAgent Orchestrator（子代理编排）

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `main_enable` | bool | `false` | 启用子代理编排（任务委派模式） |
| `remove_main_duplicate_tools` | bool | `false` | 移除主代理中与子代理重复的工具 |
| `router_system_prompt` | string | (内置) | 路由器 system prompt |
| `agents` | list | `[]` | 子代理定义列表 |

---

### 插件 (`plugin_set`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `plugin_set` | list | `["*"]` | 启用的插件列表，`["*"]` 为全部，`[]` 为禁用所有插件 |
| `disable_builtin_commands` | bool | `false` | 禁用所有内置命令 |
| `disable_metrics` | bool | `false` | 禁用匿名使用统计 |

---

### 平台特异配置 (`platform_specific`)

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `lark.pre_ack_emoji` | object | `{enable: false, emojis: ["Typing"]}` | 飞书预确认 Emoji |
| `telegram.pre_ack_emoji` | object | `{enable: false, emojis: ["✍️"]}` | Telegram 预确认 Emoji |
| `discord.pre_ack_emoji` | object | `{enable: false, emojis: ["🤔"]}` | Discord 预确认 Emoji |

---

### SubAgent 配置 (`subagent_orchestrator.agents`)

每个子代理支持以下字段：

| 参数 | 类型 | 说明 |
|---|---|---|
| `name` | string | 子代理名称 |
| `description` | string | 子代理描述（用于路由器判断） |
| `system_prompt` | string | 子代理的 system prompt |
| `provider_id` | string | 子代理使用的提供商 ID |
| `tools` | list | 子代理可用的工具列表 |
| `model` | string | 子代理使用的模型名称 |

---

## 环境变量

NovaBot 支持以下环境变量：

| 变量名 | 说明 |
|---|---|
| `NOVABOT_ROOT` | 覆盖根目录（默认为当前工作目录） |
| `NOVABOT_CLI` | CLI 模式标识（通过 `novabot run` 启动时自动设置） |
| `NOVABOT_RELOAD` | 设置为 `1` 启用插件热重载（需安装 `watchfiles`） |
| `NOVABOT_DESKTOP_CLIENT` | 桌面客户端模式标识 |
| `NOVABOT_WEBUI_DIR` | WebUI 目录路径 |
| `NOVABOT_DASHBOARD_SSL_ENABLE` | 启用 Dashboard SSL |
| `NOVABOT_DISABLE_METRICS` | 禁用匿名指标收集 |
| `DEMO_MODE` | 设置为 `True` 启用演示模式 |

> API Key 支持在 `key` 字段中使用 `$ENV_VAR` 或 `${ENV_VAR}` 语法引用环境变量。

---

## CLI 命令

NovaBot 提供命令行工具：

```bash
# 启动 NovaBot
novabot run

# 启动并启用插件热重载
novabot run --reload

# 插件管理
novabot plug install <plugin_name>
novabot plug uninstall <plugin_name>
novabot plug list
```

---

## 许可证

AGPL-3.0-or-later
