from agents import Agent, WebSearchTool
from .config import MODEL
from .catalog import search_open_library, search_google_books

RULES = """
Recommend books based on the reader's actual inquiry. Never invent titles, authors, publication
dates, awards, ratings, ISBNs or URLs. Verify title/author metadata against catalog search results.
Treat ratings as optional and source-specific. Distinguish subjective fit from bibliographic facts.
Do not reproduce copyrighted book text or long excerpts.
"""
intent = Agent(name="Reader Intent Analyst", model=MODEL,
    instructions=RULES + " Interpret topic, genre, purpose, level, tone, language, length and exclusions. Ask only if a crucial ambiguity blocks useful recommendations.",
    tools=[WebSearchTool()])
genre = Agent(name="Genre Specialist", model=MODEL,
    instructions=RULES + " Identify relevant genres, subgenres, authors and diverse literary approaches.",
    tools=[WebSearchTool(), search_open_library, search_google_books])
catalog = Agent(name="Book Catalog Researcher", model=MODEL,
    instructions=RULES + " Search Open Library and Google Books. Cross-check candidate titles/authors and return a broad candidate pool.",
    tools=[search_open_library, search_google_books])
selector = Agent(name="Top Five Selector", model=MODEL,
    instructions=RULES + """
Select exactly five verified books. Rank by relevance, usefulness, readability and diversity.
For each give title/author, why it fits, what reader gains, difficulty, caveat and verified catalog
or preview link if available. Explain ranking. If fewer than five suitable records can be verified,
be transparent rather than fabricating titles.
""",
    tools=[search_open_library, search_google_books, WebSearchTool()])
manager = Agent(name="Literary Recommendation Manager", model=MODEL,
    instructions=RULES + """
Analyze the inquiry, consult intent and genre specialists, search catalogs, then call the Top Five
Selector. Return exactly five ranked books with concise explanations, metadata and source links.
Format: interpretation; Top 5; why selected; suggested reading order. State assumptions. Do not
present popularity as literary quality.
""",
    tools=[
        WebSearchTool(),
        intent.as_tool(tool_name="analyze_reader_intent", tool_description="Analyze the reader's purpose and preferences."),
        genre.as_tool(tool_name="consult_genre_specialist", tool_description="Identify suitable genres, authors and diverse choices."),
        catalog.as_tool(tool_name="research_book_catalogs", tool_description="Find and cross-check real book catalog records."),
        selector.as_tool(tool_name="select_top_five_books", tool_description="Rank exactly five verified book recommendations."),
    ])
