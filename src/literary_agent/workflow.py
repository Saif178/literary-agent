from agents import Runner
from .agents import manager

async def recommend(inquiry, level="Any", language="Any", length="Any", exclusions=""):
    prompt = f"""
Reader inquiry: {inquiry}
Reading level: {level}
Preferred language: {language}
Preferred length: {length}
Already read / exclusions: {exclusions or "None"}
Recommend exactly five ranked books. Verify titles/authors through book catalog tools. If request is
clear, proceed without asking a clarification. Explain assumptions and provide source links.
"""
    result = await Runner.run(manager, prompt)
    return str(result.final_output)
