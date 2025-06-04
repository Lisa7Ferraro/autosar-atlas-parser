# Contributing to AUTOSAR Atlas Parser

Thank you for considering contributing!

## Opening Issues
- Check existing issues to avoid duplicates.
- Include a clear description of the problem and steps to reproduce.
- Specify your environment (Python version, operating system) and which AUTOSAR PDF you used.

## Coding Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use 4 spaces for indentation.
- Add type hints and docstrings where possible.
- Keep functions small and focused.

## Running the Parser
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Place the target AUTOSAR PDF inside the `samples/` directory.
3. Execute the parser:
   ```sh
   python3 src/main.py
   ```
   Output JSON files will be written to the `output/` directory.

We welcome pull requests for bug fixes and new features. Feel free to open an issue if you have any questions.
