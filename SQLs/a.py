I can help you improve your prompt for extracting text and tables from images with the OpenAI 4o model. Looking at your current code, you've started with a good foundation, but we can make it more specific and structured.

Here's an improved version that focuses on your requirements:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", {
        "role": "system",
        "content": """You are analyzing a multi-page scanned document. Your goal is to extract the main content body from the image with perfect accuracy, maintaining original structure while properly handling tables.

EXTRACTION RULES:
1. Extract all text content exactly as it appears in the image, preserving formatting and structure.
2. Convert any tables into properly formatted JSON arrays (one object per row with named fields).
3. Preserve table names when available and include them with the table data.
4. For multi-page documents, check if content continues from previous pages.
5. Handle tables that span multiple pages by combining them appropriately.

OUTPUT FORMAT:
Provide your extraction in JSON with two main sections:
{
  "text": "FULL TEXT INCLUDING TABLE PLACEHOLDERS",
  "tables": [
    {
      "name": "Table Name",
      "data": [{"column1": "value", "column2": "value"}, {...}]
    }
  ]
}

Important notes:
- Insert table placeholders in the text like: [[TABLE: Table Name]]
- Include ALL text content in the main text field
- Place every table's structured data in the tables array
- Ensure table names match between placeholders and the tables array
"""
    }),
    ("user", {
        "content": """Previous page context:
{previous_text}

Now analyze the current image and extract:
- Main body text with precise formatting
- All tables converted to structured JSON
- Include table names both in text and metadata
"""
    })
])
```

Key improvements:

1. Added clearer instructions about preserving the original text structure
2. Specified exactly how tables should be formatted in JSON (as arrays of objects)
3. Created a more defined output structure with separate text and tables sections
4. Added the table placeholder format `[[TABLE: Table Name]]` to indicate where tables appear in the text
5. Emphasized that table names should be included both in the main text and in the metadata

This improved prompt should help the OpenAI 4o model better understand exactly how you want the text and tables extracted and structured in the response.
