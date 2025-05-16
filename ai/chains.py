from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from ai.prompts import CHARACTER_PROMPT, MEMORY_ANALYSIS_PROMPT


class MemoryAnalysis(BaseModel):
    is_important: bool = Field(
        ...,
        description="Whether the message is important enough to be stored as a memory",
    )
    formatted_memory: Optional[str] = Field(
        ..., description="The formatted memory to be stored"
    )

def get_memory_chain():
    model = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(MemoryAnalysis)
    prompt = ChatPromptTemplate.from_template(MEMORY_ANALYSIS_PROMPT)
    return prompt | model


def get_character_chain():
    model = ChatOpenAI(model="gpt-4o", temperature=0.5)
    system_message = CHARACTER_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    return prompt | model