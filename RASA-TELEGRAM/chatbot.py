from langchain.llms import OpenAI

from langchain import LLMChain

from langchain.prompts.prompt import PromptTemplate

from langchain.memory import ConversationBufferMemory

template = """
You are an AI chatbot with a sense of humor.
Your mission is to turn the user's input into funny jokes.

{chat_history}
Human: {human_input}
Chatbot:"""

new_prompt = PromptTemplate(
input_variables=["chat_history", "human_input"],
template=template
)
new_memory = ConversationBufferMemory(memory_key="chat_history")
llm_chatbot = LLMChain(
llm=OpenAI(temperature=0),
prompt=new_prompt,
verbose=True,
memory=new_memory
)

def chatbot():
    print(llm_chatbot.predict(human_input="What's the difference between a fruit and a vegetable?"))

