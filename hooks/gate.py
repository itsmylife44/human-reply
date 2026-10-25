#!/usr/bin/env python3
"""PreToolUse gate for Claude Code and Codex: stop the first call that posts text people will read
(gh comment/review/PR/issue/release, git commit with a message, MCP reply/comment/send tools) until
the agent has loaded the human-reply skill. Description triggering alone misses these, so this blocks
once and tells the agent what to do; the retry goes through.

Reads the hook JSON on stdin. Self-test: python3 gate.py --selftest
"""
import json
import os
import re
import sys
import tempfile

POSTING_COMMAND = re.compile(
    r"\bgh\s+(pr|issue)\s+(comment|review|create|edit)\b"
    r"|\bgh\s+api\b.*(comments|reviews|replies)"
    r"|\bgh\s+release\s+create\b"
    r"|\bgit\s+commit\b.*\s(-m|-F|--message|--file)\b"
)
POSTING_TOOL = re.compile(r"^mcp__.*(comment|reply|respond|review|send|post|message)", re.I)
READ_WORDS = {"list", "get", "search", "find", "read", "view", "fetch", "query", "summary", "status"}

REASON = (
    "Before posting text people will read, load the human-reply skill, rewrite this text with it "
    "and run its scripts/check.py, then retry the same call. This gate stops only the first post."
)


def is_posting(event):
    tool = event.get("tool_name", "")
    if tool in ("Bash", "shell", "exec_command", "local_shell"):
        cmd = event.get("tool_input", {}).get("command", "")
        return bool(POSTING_COMMAND.search(cmd if isinstance(cmd, str) else " ".join(cmd)))
    words = set(tool.split("__")[-1].lower().split("_"))
    return bool(POSTING_TOOL.search(tool)) and not words & READ_WORDS


def first_time(event):
    # Claude Code keeps a loaded skill for the whole session; Codex drops skills between turns,
    # so key on turn_id when the harness sends one.
    key = re.sub(r"\W", "_", f"{event.get('session_id', 'none')}-{event.get('turn_id', '')}")
    marker = os.path.join(tempfile.gettempdir(), "human-reply-gate", key)
    if os.path.exists(marker):
        return False
    os.makedirs(os.path.dirname(marker), exist_ok=True)
    open(marker, "w").close()
    return True


def selftest():
    def bash(c):
        return {"tool_name": "Bash", "tool_input": {"command": c}}
    assert is_posting(bash('gh pr comment 12 --body "Fixed"'))
    assert is_posting(bash("gh issue create --title x --body y"))
    assert is_posting(bash("gh api repos/a/b/pulls/3/comments -f body=hi"))
    assert is_posting(bash('git commit -m "Fix retry"'))
    assert is_posting({"tool_name": "mcp__appeeky__asc_respond_to_review"})
    assert not is_posting(bash("gh pr view 12 --comments"))
    assert not is_posting(bash("git commit --amend --no-edit"))
    assert not is_posting(bash("git status"))
    assert not is_posting({"tool_name": "mcp__appeeky__asc_list_customer_reviews"})
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        event = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)  # never break the harness on odd input
    if is_posting(event) and first_time(event):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": REASON}}))
    sys.exit(0)
