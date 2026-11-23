import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

from models.schemas import ResearchReport

# Load environment variables
load_dotenv()

# Initialize Tool
search_tool = TavilySearchTool()

def create_research_crew(topic: str) -> Crew:
    """Initializes and returns the configured Research Crew."""
    
    # --- AGENTS ---
    manager = Agent(
        role="Research Manager",
        goal="Deconstruct the research topic '{topic}' into 3-5 specific, actionable search directives.",
        backstory="An expert research coordinator who excels at breaking down complex topics into searchable sub-queries.",
        llm="gemini/gemini-3.5-flash-lite",
        verbose=True
    )

    researcher = Agent(
        role="Web Researcher",
        goal="Execute the search directives using the Tavily tool to gather comprehensive data and source URLs.",
        backstory="A meticulous investigator who scours the internet for high-quality, relevant information and always records the source URLs.",
        tools=[search_tool],
        llm="gemini/gemini-3.5-flash-lite",
        verbose=True,
        allow_delegation=False
    )

    analyst = Agent(
        role="Research Analyst",
        goal="Synthesize the raw data into key findings, trends, advantages, and disadvantages.",
        backstory="A sharp analytical mind that connects the dots between disparate pieces of information to find the core narrative.",
        llm="gemini/gemini-3.5-flash-lite",
        verbose=True
    )

    fact_checker = Agent(
        role="Fact Checker",
        goal="Verify all claims made by the analyst against the raw sources. Flag or remove unsupported claims.",
        backstory="A rigorous skeptic who never accepts a claim without evidence. Ensures absolute factual accuracy.",
        llm="gemini/gemini-3.5-flash-lite",
        verbose=True
    )

    writer = Agent(
        role="Report Writer",
        goal="Draft a professional, structured research report based on the verified analysis.",
        backstory="A professional technical writer who crafts clear, engaging, and highly structured reports.",
        llm="gemini/gemini-3.5-flash-lite",
        verbose=True
    )

    # --- TASKS ---
    plan_task = Task(
        description="Analyze the topic '{topic}' and generate a list of 3 to 5 specific search directives.",
        expected_output="A numbered list of specific search queries or directives.",
        agent=manager
    )

    search_task = Task(
        description="Use the Tavily search tool to execute the directives. Collect text snippets and exact URLs for each.",
        expected_output="Raw research data including text snippets and a list of source URLs.",
        agent=researcher,
        context=[plan_task]
    )

    analyze_task = Task(
        description="Analyze the raw data. Identify key findings, pros, cons, and emerging trends.",
        expected_output="A structured analytical summary of the research data.",
        agent=analyst,
        context=[search_task]
    )

    fact_check_task = Task(
        description="Cross-reference the analytical summary with the raw data. Remove any claims not supported by the sources.",
        expected_output="A verified analytical summary, with unsupported claims removed or flagged.",
        agent=fact_checker,
        context=[analyze_task, search_task]
    )

    write_task = Task(
        description="Write the final professional research report using the verified analysis. Include all required sections and references.",
        expected_output="A complete research report matching the ResearchReport Pydantic schema.",
        agent=writer,
        context=[fact_check_task, search_task],
        output_pydantic=ResearchReport
    )

    # --- CREW ---
    crew = Crew(
        agents=[manager, researcher, analyst, fact_checker, writer],
        tasks=[plan_task, search_task, analyze_task, fact_check_task, write_task],
        process=Process.sequential,
        verbose=True
    )

    return crew