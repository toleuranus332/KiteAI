"""
Kite AI Bot — Task registry.
Returns list of enabled task functions based on config toggles.
"""
from typing import Callable, List

from tasks.faucet import claim_faucet
from tasks.staking import stake_tokens
from tasks.swap import execute_swap
from tasks.quiz import complete_quiz
from tasks.bridge import bridge_tokens

_TASK_MAP: List[tuple] = [
    ("auto_claim_faucet", claim_faucet),
    ("auto_stake", stake_tokens),
    ("auto_swap", execute_swap),
    ("auto_quiz", complete_quiz),
    ("auto_bridge", bridge_tokens),
]


def get_enabled_tasks(config: dict) -> List[Callable]:
    return [fn for key, fn in _TASK_MAP if config.get(key, True)]
