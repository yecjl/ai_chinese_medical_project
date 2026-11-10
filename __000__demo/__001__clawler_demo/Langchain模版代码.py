from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from typing import Literal


# --------- LLM 全局初始化（只创建一次） ---------
llm = ChatOpenAI(
    api_key="xxx",
    model="qwen3.8-27b",
    base_url="https://ws-w1jnk2o2tnvet109.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    streaming=True
)

# --------- 结构化数据模型 ---------
class WordPair(BaseModel):
    word: str = Field(description="英文单词")
    translate: str = Field(description="中文翻译")
    part_of_speech: Literal[
    "n",
    "v",
    "adj",
    "adv",
    "prep",
    "conj",
    "interj",
    "pron",
    "num",
    "art",
    "excl",
    "other"
    ]  = Field(description="词性")

class WordListOutput(BaseModel):
    word_list: List[WordPair] = Field(description="单词翻译列表")

parser = JsonOutputParser(pydantic_object=WordListOutput)


def translate_words_stream(text: str) -> WordListOutput:
    prompt = f"""
请将以下英文单词翻译成中文，并以 JSON 格式返回。
请只输出 JSON，不要包含任何解释性文字。
返回格式要求如下：
{parser.get_format_instructions()}

单词：{text}
"""

    full_content = ""

    for chunk in llm.stream(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            full_content += chunk.content

    print()
    return parser.parse(full_content)


if __name__ == '__main__':
    result = translate_words_stream("hello, work, english, transformer")
    print("*" * 100)
    print(result)