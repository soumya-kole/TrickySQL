from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Initialize your GPT-4o model
llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key="YOUR_API_KEY",
    temperature=0.3
)

# Create the prompt
prompt = ChatPromptTemplate.from_template("""
You are a legal document analyst.

Given the following contract text:

{document_text}

Your task:
- Identify important sections of the contract.
- For each section, create a short title.
- Summarize each section in 2-4 sentences.
- Return the output strictly as a JSON object where:
    - key = section title
    - value = concise summary.

Only include meaningful, important sections. Ignore repetitive legal boilerplate.

Respond only with a valid JSON.
""")

# Create the chain
chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# Run the chain
def summarize_contract(document_text):
    response = chain.invoke({"document_text": document_text})
    return response["text"]

# Example usage
text = open('your_extracted_contract.txt').read()
result_json = summarize_contract(text)
print(result_json)
