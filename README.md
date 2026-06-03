# LangChain Agent 教学仓库

这是一个面向 LangChain 初学者的教学向仓库，基于 didilili 的仓库进行二次开发。

本仓库在原有内容基础上补充了更多基础知识解释、步骤分隔输出、教学目录说明和适合新手阅读的中文注释。目标是让刚接触 LangChain、大模型 API、OpenAI 兼容接口的同学，也能更容易看懂每个示例在做什么、为什么这么写、运行后应该重点观察什么。

## 关于本仓库

很多 LangChain 示例代码默认读者已经熟悉 Python、OpenAI SDK、环境变量、模型 provider、消息结构等概念。对小白来说，代码虽然能跑，但常常不知道每一行到底承担什么职责。

所以这个仓库的二开方向是：

- 把示例拆成更清晰的步骤。
- 用中文注释解释基础概念。
- 用 `print("========== 内容 ==========")` 标记每个运行阶段。
- 在每个子目录中补充 `目录.md`，说明每个文件的教学目标。
- 尽量把“能跑”和“能理解”放在同等重要的位置。

## 适合谁

- 刚开始学习 LangChain 的同学
- 想理解 LangChain 0.3 和 LangChain 1.x 写法差异的同学
- 想学习如何接入 DeepSeek、通义千问等模型的同学
- 想理解原生 OpenAI SDK 和 LangChain 封装区别的同学
- 想从“能跑示例”逐步过渡到“能写工程化代码”的同学

## 项目特点

- 教学向：不是追求最短代码，而是追求每一步都能看懂。
- 新手友好：保留较多中文注释，解释参数、返回值和常见概念。
- 对比清晰：同时展示原生 SDK、LangChain 0.3、LangChain 1.x、厂商专用集成。
- 运行可读：脚本运行时会输出步骤分隔标题，方便对照代码学习。
- 结构简单：按章节目录组织，适合按顺序学习。

## 目录结构

```text
LangChain_Agent/
├── 01_LangChain上手/
│   ├── 01_LangChain_v_0.3.py
│   ├── 02_LangChain_v_1.0.py
│   ├── 03_LangChain_v_1.0.py
│   ├── 04_LangChain_engineering.py
│   └── 目录.md
├── 02-models_io/
│   ├── 01_ModelIO_Params.py
│   ├── 02_ModelIO_OpenAI.py
│   ├── 03_ModelIO_0.3_ChatOpenAI.py
│   ├── 04_ModelIO_1.0_Init_chat_model.py
│   ├── ModelIO_DeepSeek.py
│   ├── ModelIO_Qwen.py
│   └── 目录.md
├── .env
├── .gitignore
└── README.md
```

| 目录 | 内容 |
| --- | --- |
| `01_LangChain上手` | LangChain 入门示例，重点理解 0.3 写法、1.x 写法、多模型接入和工程化封装。 |
| `02-models_io` | Model I/O 示例，重点理解模型参数、输入消息、返回对象、原生 SDK 和 LangChain 封装的区别。 |

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:Undernoone/LangChain_Agent.git
cd LangChain_Agent
```

如果你已经在本地打开了这个项目，可以直接进入下一步。

### 2. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖库

本仓库示例会用到以下库：

```bash
pip install python-dotenv openai langchain langchain-openai langchain-community langchain-deepseek dashscope
```

如果安装 `ChatTongyi` 相关依赖时遇到 `cffi` 问题，可以尝试：

```bash
pip install --upgrade --force-reinstall cffi
```

### 4. 配置 `.env`

在项目根目录创建或修改 `.env` 文件，填入自己的 API Key：

```env
QWEN_API_KEY=你的阿里百炼_API_Key
aliQwen-api=你的阿里百炼_API_Key
deepseek-api=你的_DeepSeek_API_Key

LOG_LEVEL=INFO
```

说明：

- `QWEN_API_KEY`：部分阿里百炼 OpenAI 兼容接口示例使用。
- `aliQwen-api`：部分通义千问原生集成示例使用。
- `deepseek-api`：DeepSeek 相关示例使用。
- `.env` 已被 `.gitignore` 忽略，请不要把真实密钥提交到 Git。

### 5. 运行示例

从最基础的示例开始：

```bash
python "01_LangChain上手/01_LangChain_v_0.3.py"
```

继续学习 LangChain 1.x 统一入口：

```bash
python "01_LangChain上手/02_LangChain_v_1.0.py"
```

查看 Model I/O 参数示例：

```bash
python "02-models_io/01_ModelIO_Params.py"
```

查看原生 OpenAI SDK 调用方式：

```bash
python "02-models_io/02_ModelIO_OpenAI.py"
```

运行时可以重点观察终端中的分节标题：

```text
========== 1. 初始化模型 ==========
========== 2. 调用大模型结果 ==========
========== 3. 打印结果 ==========
```

这些标题可以帮助你把“代码执行顺序”和“学习目标”对应起来。

## 使用教程

建议按照下面的顺序学习。

### 第一阶段：先把 LangChain 跑起来

阅读并运行：

- `01_LangChain上手/01_LangChain_v_0.3.py`
- `01_LangChain上手/02_LangChain_v_1.0.py`

重点理解：

- 什么是模型客户端
- `ChatOpenAI` 是什么
- `init_chat_model` 是什么
- `model`、`api_key`、`base_url`、`model_provider` 分别负责什么
- 为什么 OpenAI 兼容接口可以调用非 OpenAI 模型

### 第二阶段：理解多个模型怎么接入

阅读并运行：

- `01_LangChain上手/03_LangChain_v_1.0.py`
- `02-models_io/ModelIO_DeepSeek.py`
- `02-models_io/ModelIO_Qwen.py`

重点理解：

- OpenAI 兼容接口和厂商原生集成的区别
- DeepSeek 和通义千问在 LangChain 中的接入方式
- 为什么不同 provider 最后都能用类似的 `invoke` / `stream` 调用

### 第三阶段：理解 Model I/O

阅读并运行：

- `02-models_io/01_ModelIO_Params.py`
- `02-models_io/02_ModelIO_OpenAI.py`
- `02-models_io/03_ModelIO_0.3_ChatOpenAI.py`
- `02-models_io/04_ModelIO_1.0_Init_chat_model.py`

重点理解：

- `temperature` 如何影响输出随机性
- `max_tokens` 为什么和输出长度、成本有关
- 原生 OpenAI SDK 的返回结构是什么样
- LangChain 的 `AIMessage` 为什么更适合后续接 Prompt、Parser、Agent
- 字符串输入和多角色消息输入有什么区别

### 第四阶段：学习工程化写法

阅读并运行：

- `01_LangChain上手/04_LangChain_engineering.py`

重点理解：

- 为什么要把 API Key 放到 `.env`
- 为什么要封装 `init_llm_client()`
- 为什么用 `logging` 替代到处 `print`
- 为什么要写 `try...except`
- `if __name__ == "__main__"` 有什么作用

## 常用依赖说明

| 依赖库 | 作用 |
| --- | --- |
| `python-dotenv` | 从 `.env` 文件读取环境变量。 |
| `openai` | 使用 OpenAI SDK 调用 OpenAI 兼容接口。 |
| `langchain` | LangChain 核心入口，例如 `init_chat_model`。 |
| `langchain-openai` | 提供 `ChatOpenAI` 等 OpenAI 兼容模型封装。 |
| `langchain-community` | 提供社区集成，例如 `ChatTongyi`。 |
| `langchain-deepseek` | 提供 DeepSeek 的 LangChain 原生集成。 |
| `dashscope` | 通义千问 / 阿里百炼相关调用依赖。 |

## 环境变量说明

| 变量名 | 用途 |
| --- | --- |
| `QWEN_API_KEY` | 阿里百炼 OpenAI 兼容接口示例使用。 |
| `aliQwen-api` | 通义千问原生集成示例使用。 |
| `deepseek-api` | DeepSeek 官方接口或 DeepSeek provider 示例使用。 |
| `LOG_LEVEL` | 控制日志输出级别，默认可用 `INFO`。 |

## 注意事项

- 运行脚本会真实调用大模型 API，可能产生费用。
- 请确认 `.env` 中的 API Key 有效，并且对应平台余额充足。
- 不同模型平台的模型名称可能会变化，运行失败时优先检查模型名、API Key 和 `base_url`。
- 本仓库偏教学演示，部分写法会故意写得详细一些，方便理解。
- 不要把 `.env`、API Key、访问令牌等敏感信息提交到 Git。

## 参考资料

- LangChain Provider 集成总览：<https://docs.langchain.com/oss/python/integrations/providers/overview>
- LangChain Python 文档：<https://docs.langchain.com/oss/python/langchain/overview>

## 致谢

本仓库基于 didilili 的仓库进行二次开发，在原有学习内容基础上增加了更详细的中文解释、基础知识补充和教学目录说明。感谢原作者的内容基础。
