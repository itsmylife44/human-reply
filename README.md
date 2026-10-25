# human-reply

An agent skill that makes Claude, Codex and other models write like a person in comments, threads, reviews, DMs, PR descriptions, issues and commits: the point first, plain words, no em dashes, then stop.

## Install

Claude Code, best option: install it as a plugin. You get the skill plus a hook that makes the agent load it before it posts.

```
/plugin install human-reply --marketplace itsmylife44/human-reply
```

Any other harness, with the skills CLI, which picks the right folder for Claude Code, Codex, Cursor, Gemini CLI, OpenCode and the other harnesses that read `SKILL.md`:

```
npx skills add itsmylife44/human-reply -g
```

Or copy this folder by hand into your harness's global skills folder:

| Harness | Folder |
| --- | --- |
| Claude Code | `~/.claude/skills/human-reply` |
| Codex, Cline, Warp, Zed | `~/.agents/skills/human-reply` |
| Cursor | `~/.cursor/skills/human-reply` |
| Gemini CLI | `~/.gemini/skills/human-reply` |
| OpenCode | `~/.config/opencode/skills/human-reply` |

No skills support? Paste the **Rules** section of `SKILL.md` into your `AGENTS.md` or `CLAUDE.md`.

Use either the plugin or a copied folder in Claude Code, not both, or the skill shows up twice.

## Make it fire every time

A skill fires when the model decides it should, and models often skip it for a quick reply. Tests with plain "reply to this issue" prompts didn't load it. Two things fix that.

**1. One line in your global instructions.** Add this near the top of `~/.claude/CLAUDE.md` (Claude Code), `~/.codex/AGENTS.md` (Codex), `~/.gemini/GEMINI.md` (Gemini CLI), `~/.config/opencode/AGENTS.md` (OpenCode), or your Cursor User Rules:

```
Before drafting or posting any text another person will read (comment, PR or issue reply or description, review reply, commit message, chat, DM, email, ticket, post), load the human-reply skill and follow it.
```

**2. The posting gate.** `hooks/gate.py` stops the first `gh` comment, review, PR, issue or release call, `git commit -m`, or MCP reply/comment/send tool in a session, and tells the agent to load the skill and retry. The plugin installs it for Claude Code. For Codex, add it to `~/.codex/hooks.json`, then trust it in `/hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 ~/.agents/skills/human-reply/hooks/gate.py" }] },
      { "matcher": "mcp__.*(comment|reply|respond|review|send|post|message).*",
        "hooks": [{ "type": "command", "command": "python3 ~/.agents/skills/human-reply/hooks/gate.py" }] }
    ]
  }
}
```

The same block works in `~/.claude/settings.json` if you installed the folder instead of the plugin (point the path at `~/.claude/skills/human-reply`).

Lots of skills installed? Claude Code drops the descriptions of the least-used ones when the list gets too long, so the model may see only the name. Raise `skillListingBudgetFraction` in settings, or set rarely used skills to name-only with `skillOverrides`.

## Check a draft

```
python3 scripts/check.py --lang it draft.txt
```

`--lang` is the language (default `en`). `--kind` is `reply` (default), `post` for PR descriptions, issues and posts (template headers allowed) or `commit` (72-column wrap allowed). The rules in `SKILL.md` work in any language. The checker has phrase packs for en, it, fr, es, pt, de, ru, zh, ja, ko, and any other code still gets the layout and quote checks. Adding a language is one line in `WRAPPERS`.

Dashes follow each language's own rules: banned in English, Japanese and Korean, at most one elsewhere, and the grammatical Russian dash is allowed.

It flags dashes, line breaks in the middle of sentences, double blank lines, stacks of one-line paragraphs, labels before the answer ("Short answer:"), chatbot sign-offs, recap lines, "not X but Y" contrasts and stock AI words. Silent output means clean. `--selftest` runs its own check.

The full list of tells the agent rewrites by hand is in `references/tells.md`, adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT).

## License

MIT, see `LICENSE`. `references/tells.md` is adapted from blader/humanizer, whose MIT notice is in `THIRD_PARTY_NOTICES`.
