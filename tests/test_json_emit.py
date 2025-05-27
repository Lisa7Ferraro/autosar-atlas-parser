import json
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.json_emitter import Requirement, emit_jsonl


def test_emit_jsonl(tmp_path: Path) -> None:
    reqs = [
        Requirement(
            requirement_id="RS_Diag_00001",
            section="Diagnostics",
            title="First",
            description="Desc",
            rationale="Rat",
            use_case="Use",
            applies_to=["CP"],
            dependencies=[],
        ),
        Requirement(
            requirement_id="RS_Diag_00002",
            section="Diagnostics",
            title="Second",
            description="",
            rationale="",
            use_case="",
            applies_to=[],
            dependencies=["RS_Diag_00001"],
        ),
    ]
    output = tmp_path / "out.jsonl"
    emit_jsonl(reqs, output)

    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2

    objs = [json.loads(line) for line in lines]
    assert objs[0]["requirement_id"] == "RS_Diag_00001"
    assert objs[1]["dependencies"] == ["RS_Diag_00001"]
