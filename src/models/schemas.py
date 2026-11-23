from pydantic import BaseModel, Field
from typing import List

class Reference(BaseModel):
    title: str = Field(description="Title of the source article or document")
    url: str = Field(description="Direct URL to the source")

class ResearchReport(BaseModel):
    title: str = Field(description="Professional title of the research report")
    introduction: str = Field(description="Brief overview and context of the research topic")
    key_findings: List[str] = Field(description="List of the most important discoveries or facts")
    analysis: str = Field(description="Detailed analysis including advantages, disadvantages, and trends")
    limitations: str = Field(description="Limitations of the research, missing data, or biases")
    conclusion: str = Field(description="Final summary and actionable recommendations")
    references: List[Reference] = Field(description="List of all cited sources with their URLs")