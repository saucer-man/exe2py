
from llama_index.llms.deepseek import DeepSeek
from llama_index.core.llms import ChatMessage, MessageRole
# 替换为你的 DeepSeek API Key
DEEPSEEK_API_KEY = ""

# 初始化 DeepSeek 聊天模型
llm = DeepSeek(
    model="deepseek-reasoner",
    api_key=DEEPSEEK_API_KEY,
)

# System 提示（定义助手角色）
SYSTEM_PROMPT = (
    "你是一位擅长 Python 反编译的专家。"
    "你将收到由 dis 模块反汇编后的 Python 字节码，来源于pyc文件"
    "你的任务是准确还原该函数的源码，保持格式正确，包括缩进和逻辑。"
    "输出时只返回直接的 Python 代码，不要添加任何说明或注释。也不用添加反引号之类的无关字符"
)

def query_ai(func_name:str, bytecode_str: str) -> str:
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=SYSTEM_PROMPT),
        ChatMessage(
            role=MessageRole.USER,
            content=f"函数名称是:`{func_name}`\n请根据以下字节码还原 Python 函数源码：\n```\n{bytecode_str}\n```"
        ),
    ]

    try:
        response = llm.chat(messages)
        return response.message.content.strip()
    except Exception as e:
        print(f"[!] DeepSeek Chat 调用失败: {e}")
        return f"# AI 生成失败：{e}"