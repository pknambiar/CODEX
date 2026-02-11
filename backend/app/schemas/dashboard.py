from pydantic import BaseModel


class StageMetric(BaseModel):
    stage: str
    count: int


class SourceMetric(BaseModel):
    source: str
    count: int


class MonthlyMetric(BaseModel):
    month: str
    count: int


class DashboardMetrics(BaseModel):
    total_opportunities: int
    opportunities_by_stage: list[StageMetric]
    conversion_rates: dict[str, float]
    average_days_in_stage: dict[str, float]
    source_effectiveness: list[SourceMetric]
    monthly_additions: list[MonthlyMetric]
