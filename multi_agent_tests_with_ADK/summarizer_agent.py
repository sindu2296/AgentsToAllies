from google.adk.agents import Agent

class SummarizerAgent(Agent):
    def __init__(self, model_name: str):
        super().__init__(
            name="summarizer_agent",
            model=model_name,
            instruction="You are a highly skilled summarizer. Your task is to concisely summarize provided text, extracting the key information.",
            # No specific tools needed if it just processes text
        )

    async def execute(self, text_to_summarize: str) -> str:
        # The LLM will use its instruction to summarize
        response = await self.model.generate_content(
            f"Summarize the following news article: {text_to_summarize}\n\nSummary:"
        )
        return "Summary: "+response.text