from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template_string = """
I want you to act as a tech writer for a music app called Spinamp.

Every 2 weeks you will be asked to write a summary of the last 2 weeks of recent changes to the app.

The app is built on 3 git repositories:
 - spindexer-internal is the open source, decentralized indexer
 - spinamp-backend is the backend for the app
 - spinamp is the frontend for the app

You will be given a list of recent commits to each of these repositories as a JSON document from the developer.

Your summary should be a list of bullet points written in simple language that could be understood by a non-technical user of the app that may not be familiar with engineering details or terms. DO NOT use the respository names at all in your summary

You can use seperate points for each of the repositories, or you can combine changes across repositories together into a single item if you think they are all related to the same user-facing feature.

Respond with only the summary list, no other context.
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_template_string
)
human_template = "{commits_string}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)


class SummarizeCommits(BaseTool):
    name = "SummarizeCommits"
    description = (
        "use this to summarize a batch of github commits from one or multiple repos"
    )

    def _run(self, commits_string: str) -> str:
        """Summarizes a batch of github commits from one or multiple repos"""
        messages = chat_prompt.format_prompt(
            commits_string=commits_string
        ).to_messages()

        chat = ChatOpenAI(temperature=0.8, model_name="gpt-4")

        summary = chat(messages)

        return summary

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GithubRecentCommits does not support async")