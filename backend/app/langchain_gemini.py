import os
from typing import List

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field, BaseModel, SecretStr

GOOGLE_API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY
)

class Tags(BaseModel):
    tags: List[str] = Field(description="The tags generated for the content.")

parser = PydanticOutputParser(pydantic_object=Tags)

def auto_generate_tags(
        article: str,
        no_of_tags: int,
):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Generate {no_of_tags} tags related to the content for the following article that depicts the summary or about the content."
                "Note: Provide a json dictionary with the tags as key and the generated tags in a list as value.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    no_of_tags = no_of_tags
    response: AIMessage = chain.invoke(
        {
            "no_of_tags": no_of_tags,
            "input": article,
        }
    )
    output: Tags = parser.invoke(response.content)
    return output.tags
