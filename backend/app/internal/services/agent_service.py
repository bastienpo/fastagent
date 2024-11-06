"""Service module for agent."""

from langchain_core.language_models import BaseLanguageModel, FakeListLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


class AgentBuilder:
    """Agent builder."""

    def __init__(self: "AgentBuilder") -> None:
        """Initialize the builder."""
        self.prompt = ChatPromptTemplate.from_template(
            "Tell me a story about a {topic}."
        )
        self.model = FakeListLLM(
            responses=["I'm sorry, I don't have any stories to tell."]
        )

    def set_prompt(self: "AgentBuilder", prompt: ChatPromptTemplate) -> "AgentBuilder":
        """Set the prompt."""
        self.prompt = prompt
        return self

    def set_model(self: "AgentBuilder", model: BaseLanguageModel) -> "AgentBuilder":
        """Set the model."""
        self.model = model
        return self

    def build(self: "AgentBuilder") -> Runnable:
        """Build a langchain runnable."""
        return self.prompt | self.model
