from memory.memory_manager import save_conversation, get_last_conversation
from models import AnalysisPlan

plan = AnalysisPlan(
    intent="trend",
    target_signals=["Temperature"],
    analysis=["trend"],
    execution_steps=["detect_trend"],
    reason="Testing conversation memory."
)

save_conversation(
    "Show temperature trend",
    plan
)

print(get_last_conversation())