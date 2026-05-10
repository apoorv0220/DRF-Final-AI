from pathlib import Path


def _solutions_dir() -> Path:
    # varynt_api/ -> q02-core-implementation/ -> solutions/
    return Path(__file__).resolve().parents[2]


def load_prompt(relative_under_solutions: str) -> str:
    path = _solutions_dir() / relative_under_solutions
    return path.read_text(encoding="utf-8")
