"""Print one conversation from a trace file, readable: the task, the agent, tool calls and results.

    python transcript.py results/<run>/traces/<model>-<bot>-<item>-<rep>.json
"""

import json
import sys


def show(path: str) -> str:
    out = []
    for m in json.load(open(path)):
        for p in m.get("parts", []):
            kind = p.get("part_kind")
            if kind == "user-prompt":
                out.append(f"TASK: {p['content']}")
            elif kind == "text" and p.get("content", "").strip():
                out.append(f"AGENT: {p['content']}")
            elif kind == "tool-call":
                args = p["args"] if isinstance(p["args"], str) else json.dumps(p["args"])
                out.append(f"  → {p['tool_name']}({args})")
            elif kind == "tool-return":
                c = p["content"] if isinstance(p["content"], str) else json.dumps(p["content"])
                out.append(f"  ← {c[:400]}")
    return "\n".join(out)


if __name__ == "__main__":
    print(show(sys.argv[1]))
