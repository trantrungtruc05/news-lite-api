from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from datetime import datetime

def summary_content(content: str):

    print("Summary content start at: ", datetime.now())

    # 1. Connect to model LLaMA via Ollama
    llm = Ollama(model="llama3.1:8b", system="You are an AI assistant specialized in summarization. Only return a concise and accurate summary of the input. Do not add comments, analysis, or explanations.")

    # 2. Create Prompt in instruction format
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in a short and easy to understand way:\n\n{text}"
    )

    # 3. Create chain to summarize
    summarize_chain = LLMChain(llm=llm, prompt=prompt)

    # 4. Execute summary
    summary = summarize_chain.run(content)
    print("Summary done at: ", datetime.now())
    return summary