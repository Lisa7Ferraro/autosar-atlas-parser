from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from typing import List, Sequence

from pydantic import BaseModel, ValidationError


@dataclass
class Requirement:
    """Data container for a single requirement."""

    requirement_id: str
    section: str
    title: str
    description: str = ""
    rationale: str = ""
    use_case: str = ""
    applies_to: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


class RequirementModel(BaseModel):
    requirement_id: str
    section: str
    title: str
    description: str | None = ""
    rationale: str | None = ""
    use_case: str | None = ""
    applies_to: List[str] = []
    dependencies: List[str] = []


def emit_jsonl(requirements: Sequence[Requirement], output_path: str) -> None:
    """Write requirements to a JSON Lines file with schema validation."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for req in requirements:
            data = asdict(req)
            # Validate against schema
            RequirementModel(**data)
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
