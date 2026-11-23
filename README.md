# Multi-Agent AI Research Assistant

An autonomous research pipeline that leverages a team of specialized AI agents to investigate topics, search the live internet, verify facts, and generate structured, professional reports. 

Built to demonstrate practical multi-agent orchestration, this project uses CrewAI to manage sequential workflows, Google Gemini for reasoning, Tavily for grounded web search, and Pydantic to enforce strict data validation on the final outputs.

## Overview

Traditional LLM applications often struggle with hallucinations and lack real-time context. This project addresses those limitations by decomposing the research process into distinct, verifiable steps handled by specialized agents:

1. **Research Manager**: Parses the user's prompt and formulates a targeted search strategy.
2. **Web Researcher**: Executes live internet searches via the Tavily API, retrieving text snippets and source URLs.
3. **Research Analyst**: Synthesizes the raw data to identify trends, advantages, disadvantages, and core findings.
4. **Fact Checker**: Cross-references the analyst's claims against the original source data, filtering out unsupported statements.
5. **Report Writer**: Compiles the verified information into a comprehensive, structured report.

The final output is not just raw text; it is a strictly validated Pydantic model. This ensures the Streamlit UI can reliably parse and display the introduction, key findings, analysis, limitations, and references without relying on fragile text parsing.

## Tech Stack

- **Orchestration**: CrewAI
- **LLM**: Google Gemini (via LiteLLM)
- **Search**: Tavily API
- **Frontend**: Streamlit
- **Data Validation**: Pydantic
- **Environment**: Python 3.10+

## Getting Started

### Prerequisites

Before running the application, you will need:
- Python 3.10 or higher.
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey).
- A [Tavily API Key](https://tavily.com/) (required for live web search).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/multi-agent-research-assistant.git
   cd multi-agent-research-assistant
