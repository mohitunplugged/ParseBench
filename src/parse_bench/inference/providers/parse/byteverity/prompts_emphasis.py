"""Shared residual-emphasis prompt and line extraction (used by the offline replay and the live provider)."""
import re
TABLE = re.compile(r"<table[\s\S]*?</table>", re.I)

PROMPT = """You are acting purely as a vision checker. Do NOT run any commands.
The attached image is a document page. Below are the text lines already transcribed from it, numbered.
Look at the IMAGE and report visual emphasis only — do not re-transcribe, correct, or add text.

Return ONLY a JSON object:
{"headings": [{"line": <n>, "level": <1|2|3>}], "bold": [{"line": <n>, "text": "<exact substring of that line that is printed in bold>"}]}

Rules:
- headings: lines that are visually titles or section headings (larger / bold / standalone). level 1 = document title, 2 = section, 3 = subsection.
- bold: only text visibly printed in a heavier weight. Copy the substring EXACTLY as it appears in the numbered line.
- Do not list a line as both heading and bold. If nothing qualifies, return empty lists.

LINES:
"""


def lines_of(md: str) -> list[str]:
    md = TABLE.sub("\n", md)
    out = []
    for ln in md.split("\n"):
        t = re.sub(r"^\s*(#{1,6}\s+|[-*•]\s+)", "", ln).replace("**", "").strip()
        if t and not t.startswith("<"):
            out.append(t)
    return out[:180]


