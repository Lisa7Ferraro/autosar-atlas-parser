import json
import subprocess
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
    result = subprocess.run(
        ["markitdown"],
        input=text,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"markitdown failed with code {result.returncode}: {result.stderr.strip()}"
        )
    return json.loads(result.stdout)
