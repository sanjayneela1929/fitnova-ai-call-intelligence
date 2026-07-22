from typing import List

from pydantic import BaseModel


class CategoryScores(BaseModel):

    needs_discovery: int

    product_knowledge: int

    objection_handling: int

    compliance: int

    next_step_booking: int


class CallIssue(BaseModel):

    issue_type: str

    severity: str

    timestamp: str

    quote: str

    reason: str

    recommendation: str


class AnalysisResult(BaseModel):

    overall_score: int

    category_scores: CategoryScores

    summary: str

    strengths: List[str]

    issues: List[CallIssue]

    action_items: List[str]