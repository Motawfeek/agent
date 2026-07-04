"""Wikipedia lookup tool for factual knowledge."""
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

_wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=_wiki_wrapper,
    name="wikipedia",
    description=(
        "Look up factual information, definitions, and background knowledge on Wikipedia. "
        "Use this for historical facts, scientific concepts, biographies, "
        "geography, and general knowledge questions. "
        "Input: a topic or search query, e.g. 'Great Wall of China', 'Albert Einstein'."
    ),
)
