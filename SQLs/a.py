prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are analyzing a multi-page scanned document. Your goal is to extract only the main content body from the image.\n"
        "- Ignore any headers and footers.\n"
        "- Replace any tables with inline JSON arrays (one object per row).\n"
        "- Preserve text as it appears, but enhance structure using context from the previous page.\n"
        "- Insert table JSON inline where it appears in the flow of text.\n"
    )),
    ("user", (
        "Previous page context:\n"
        "{previous_text}\n\n"
        "Now analyze the current image and extract:\n"
        "- Main body text only\n"
        "- Replace any table with inline JSON\n\n"
        "{format_instructions}"
    ))
])
from pydantic import BaseModel
from typing import Optional
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage
import base64

class PageText(BaseModel):
    text: str

parser = PydanticOutputParser(pydantic_object=PageText)

def encode_image_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

image_paths = ["page1.png", "page2.png", "page3.png"]
previous_text = ""

for path in image_paths:
    image_base64 = encode_image_base64(path)

    formatted_prompt = prompt.format_messages(
        previous_text=previous_text,
        format_instructions=parser.get_format_instructions()
    )

    response = llm.invoke([
        *formatted_prompt,
        HumanMessage(content=[
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ])
    ])

    parsed = parser.parse(response.content)
    print(f"\n📄 Extracted from {path}:\n{parsed.text}\n")

    # Update context for next page
    previous_text = parsed.text
