
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a savage assistant."),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{input_user_message}"),
    ]
)
chain = prompt | chat | parser

print(prompt.invoke(
    {"history_messages": [],
    "input_user_message": "whats my name"},
    
))
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
    
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input_user_message",
    history_messages_key="history_messages",
)
response = chain_with_message_history.invoke(
    {"input_user_message": "whats my name"},
    {"configurable": {"session_id": "1234"}},
)

print(response)
# I don’t know your name, but I’m sure it’s as fabulous as you are! Want to share it, or are you going for the mysterious vibe?
# store
# {'1234': InMemoryChatMessageHistory(messages=[HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='I don’t know your name, but I’m sure it’s as fabulous as you are! Want to share it, or are you going for the mysterious vibe?', additional_kwargs={}, response_metadata={})])}
response = chain_with_message_history.invoke(
    {"input_user_message": "my name is yash"},
    {"configurable": {"session_id": "1234"}},
)

print(response)
# Nice to meet you, Yash! Now that we’re on a first-name basis, what can I do for you today?
# store
# {'1234': InMemoryChatMessageHistory(messages=[HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='I don’t know your name, but I’m sure it’s as fabulous as you are! Want to share it, or are you going for the mysterious vibe?', additional_kwargs={}, response_metadata={}), HumanMessage(content='my name is yash', additional_kwargs={}, response_metadata={}), AIMessage(content='Nice to meet you, Yash! Now that we’re on a first-name basis, what can I do for you today?', additional_kwargs={}, response_metadata={})])}
response = chain_with_message_history.invoke(
    {"input_user_message": "whats my name"},
    {"configurable": {"session_id": "1234"}},
)

print(response)
# Your name is Yash. Keeping up, are we?
# store
# {'1234': InMemoryChatMessageHistory(messages=[HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='I don’t know your name, but I’m sure it’s as fabulous as you are! Want to share it, or are you going for the mysterious vibe?', additional_kwargs={}, response_metadata={}), HumanMessage(content='my name is yash', additional_kwargs={}, response_metadata={}), AIMessage(content='Nice to meet you, Yash! Now that we’re on a first-name basis, what can I do for you today?', additional_kwargs={}, response_metadata={}), HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='Your name is Yash. Keeping up, are we?', additional_kwargs={}, response_metadata={})])}
response = chain_with_message_history.invoke(
    {"input_user_message": "whats my name"},
    {"configurable": {"session_id": "123"}},
)

print(response)
# I don’t know your name, but I’m sure it’s something special—like “The Enigma” or “Mystery Master.” Want to share it, or should I just keep guessing?
# store
# {'1234': InMemoryChatMessageHistory(messages=[HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='I don’t know your name, but I’m sure it’s as fabulous as you are! Want to share it, or are you going for the mysterious vibe?', additional_kwargs={}, response_metadata={}), HumanMessage(content='my name is yash', additional_kwargs={}, response_metadata={}), AIMessage(content='Nice to meet you, Yash! Now that we’re on a first-name basis, what can I do for you today?', additional_kwargs={}, response_metadata={}), HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='Your name is Yash. Keeping up, are we?', additional_kwargs={}, response_metadata={})]),
#  '123': InMemoryChatMessageHistory(messages=[HumanMessage(content='whats my name', additional_kwargs={}, response_metadata={}), AIMessage(content='I don’t know your name, but I’m sure it’s something special—like “The Enigma” or “Mystery Master.” Want to share it, or should I just keep guessing?', additional_kwargs={}, response_metadata={})])}
 
ecommerce_system_message = """
You are a savage assistant chatbot for our ecommerce platform - ABC Inc.

We sell the following products:

Shirts:
1. Urban Explorer Shirt (abc.com/urban-shirt.jpg)
   - Colors: Navy Blue, Olive Green, Charcoal Grey
   - Sizes: Small (S), Medium (M), Large (L), Extra Large (XL)

2. Classic Oxford Shirt (abc.com/orford-shirt.jpg)
   - Colors: White, Light Blue, Pastel Pink
   - Sizes: Small (S), Medium (M), Large (L), Extra Large (XL), XXL

Pants:
1. Heritage Stretch Chinos (abc.com/heritage-chinos.jpg)
   - Colors: Khaki, Slate Grey, Black
   - Sizes: 30, 32, 34, 36, 38 (Waist) | Regular, Short, Long (Length)

2. Essential Slim Jeans (abc.com/essential-jeans.jpg)
   - Colors: Indigo, Washed Blue, Black
   - Sizes: 28, 30, 32, 34, 36 (Waist) | Regular, Short, Long (Length)

Give any information related to products if users ask.
Do not list everything to user all at once, if information is overloaded on user, they get confused.
Slowly narrow down on user requirements by asking question and suggest the exact product for them.
Your job is to only talk about the products nothing else. If customer asks anything else, deny it and stick to only give product info.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", ecommerce_system_message),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{input_user_message}"),
    ]
)
chain = prompt | chat | parser
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input_user_message",
    history_messages_key="history_messages",
)
response = chain_with_message_history.invoke(
    {"input_user_message": "hi"},
    {"configurable": {"session_id": "1"}},
)

print(response)
# Hey there! Looking for something specific in our product range? Let me know what you need help with!
response = chain_with_message_history.invoke(
    {"input_user_message": "maybe shirts"},
    {"configurable": {"session_id": "1"}},
)

print(response)
# Great choice! We have two types of shirts. Are you looking for something casual or more formal?
response = chain_with_message_history.invoke(
    {"input_user_message": "cna you show some pics?"},
    {"configurable": {"session_id": "1"}},
)

print(response)
# I can't show pictures, but I can describe our shirts for you! We have the Urban Explorer Shirt and the Classic Oxford Shirt. 

# Which style are you interested in: a casual vibe with the Urban Explorer or a more formal look with the Classic Oxford?
# store["1"]
# InMemoryChatMessageHistory(messages=[HumanMessage(content='hi', additional_kwargs={}, response_metadata={}), AIMessage(content='Hey there! Looking for something specific in our product range? Let me know what you need help with!', additional_kwargs={}, response_metadata={}), HumanMessage(content='maybe shirts', additional_kwargs={}, response_metadata={}), AIMessage(content='Great choice! We have two types of shirts. Are you looking for something casual or more formal?', additional_kwargs={}, response_metadata={}), HumanMessage(content='cna you show some pics?', additional_kwargs={}, response_metadata={}), AIMessage(content="I can't show pictures, but I can describe our shirts for you! We have the Urban Explorer Shirt and the Classic Oxford Shirt. \n\nWhich style are you interested in: a casual vibe with the Urban Explorer or a more formal look with the Classic Oxford?", additional_kwargs={}, response_metadata={})])
 