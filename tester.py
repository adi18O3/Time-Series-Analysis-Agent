from models import AnalysisPlan

plan = AnalysisPlan(
    intent="trend_analysis",
    target_signals=["temperature"],
    analysis=["trend"],
    execution_steps=["calculate trend", "plot graph"],
    reason="User wants to identify the trend."
)

print(plan)