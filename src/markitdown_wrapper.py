import json
import subprocess
import shutil
from typing import Any


def run_markitdown(text: str) -> Any:
    """Run the ``markitdown`` CLI on the given text and return parsed JSON.

    Parameters
    ----------
    text : str
        The input text, typically Markdown, to feed into markitdown.

    Returns
    -------
    Any
        Parsed JSON object produced by markitdown.
    """
    if shutil.which("markitdown") is None:
        raise FileNotFoundError("markitdown command not found. Install the markitdown package.")

    result = subprocess.run(
        ["markitdown", "--json"],
        input=text,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"markitdown failed with code {result.returncode}: {result.stderr.strip()}"
        )

    if not result.stdout.strip():
        raise ValueError("markitdown produced no output")

    return json.loads(result.stdout)
