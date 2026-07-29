from app.ai.policy import MEDIASSIST_SYSTEM_INSTRUCTION


def test_mediassist_policy_covers_required_safety_boundaries() -> None:
    policy = MEDIASSIST_SYSTEM_INSTRUCTION.lower()

    for requirement in (
        "educational and informational",
        "never diagnose",
        "prescribe medicines",
        "dosage",
        "licensed healthcare professional",
        "immediate emergency medical assistance",
        "do not provide emergency treatment instructions",
    ):
        assert requirement in policy
