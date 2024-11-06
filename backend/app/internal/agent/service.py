"""Service module for agent."""

from langchain_core.language_models import FakeListLLM
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Tell me a story about a {input}.")

model = FakeListLLM(responses="I'm sorry, I don't have any stories to tell.")

chain = prompt | model
