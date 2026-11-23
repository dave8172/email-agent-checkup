# email-agent-checkup

An AI agent that runs a company's billing inbox, tested before and after the fixes: the tests, both versions of the agent, and every run.

**The report:** https://quirkyagents.com/agents/email/#report

Acme Invoicing is a made-up company (the same one as [support-bot-checkup](https://github.com/dave8172/support-bot-checkup)): 5 customers, 2 suppliers, 3 staff. The agent works through the billing inbox: it answers customers, refunds, changes billing emails, pays supplier invoices and leaves the rest for finance. The "before" agent is built the way most first versions are (rules in the prompt, tools that can reach any account and send to any address). The "after" agent is the same agent after the check-up's fixes. Both run on Pydantic AI.

| | Older model before | after | Newer model before | after |
|---|---|---|---|---|
| Normal inbox tasks done | 26 of 27 | 27 of 27 | 24 of 27 | 27 of 27 |
| Tricks that worked | 3 of 30 | 0 of 30 | 0 of 30 | 0 of 30 |
| Runs with a customer's card ending sent off their account | 3 of 57 | 0 of 57 | 0 of 57 | 0 of 57 |
| Runs with money out that the rules didn't allow | 1 of 57 ($12) | 0 of 57 | 0 of 57 | 0 of 57 |
| Runs that waited for a person to approve | 0 | 9 | 0 | 9 |

Older model: Claude Haiku 4.5. Newer: Claude Haiku 5.5. 19 cases (9 normal tasks, 10 tricks), each run 3 times per model per agent. All numbers: [`results/20261123-165103/summary.md`](results/20261123-165103/summary.md).

**Where the models held, the code wasn't tested by them.** Both before agents refused the bank-change fraud, the fake CEO, the fake IT and most planted lines on their own. To check the after agent's code doesn't depend on that, `tests/test_agents.py` drives both agents with a scripted model that does exactly what each trick asks: all 10 tricks get through the before agent, none through the after agent, and the after agent still does all 9 tasks ($0, no API key).

## Rerun it

```
pip install "pydantic-ai-slim[anthropic]" pytest
python -m pytest -q                                   # $0: the scripted-model tests
ANTHROPIC_API_KEY=... python checkup.py --models haiku-5-5,haiku-4-5
```

That run cost $1.91. `--repeats 1 --only t7,x7` runs a few cases for a few cents; `--models test` runs everything at $0 on Pydantic AI's TestModel (plumbing only). Results land in `results/<run-id>/`: `summary.md`, `summary.json`, `runs.jsonl` (one line per run) and `traces/` (every run in Pydantic AI's message format; `python transcript.py <trace>` prints one).

## What's here

| Path | What |
|---|---|
| `acme/world.py` | customers, suppliers, staff, the refund policy as code, and the leak check |
| `bot/before.py`, `bot/after.py` | the two agents; `after.py`'s docstring lists every fix and what enforces it |
| `tests/cases.py` | 9 normal tasks and 10 tricks, scored from what happened in the world |
| `tests/test_agents.py` | $0 tests with a scripted model |
| `checkup.py` | runs everything and writes the summary; no judge model |
