---
name: human-reply
description: Write replies and posts that sound like a person typed them. Use whenever you draft or post text other people will read in a thread or channel, such as a reply to a comment, a PR or code review reply, a GitHub issue or discussion comment, a PR description, a new issue, a commit message, release notes, a forum, Reddit or social post, a Slack or Discord message, a DM, a support ticket or an email. Also use when the user asks to make text sound more human, shorter, less technical, or less like AI.
---

# Human reply

A reply is one person answering another. The reader asked something specific, and they will judge the answer in the first sentence. Write the way a busy, friendly expert types in a thread: the answer first, plain words, then stop.

Answering someone? Follow **Steps**. Writing something new that nobody asked for yet (a PR description, an issue, a commit, a post)? Follow **New posts**. The **Rules** apply to both.

## Steps

1. **Find the question.** Reread the comment you are answering and write down, for yourself, the one thing they asked, in their words. If they asked two things, answer both, in their order. Done when you can say the question in one line.
2. **Answer it in the first sentence.** That sentence would work as the whole reply if the thread cut off after it. "Yes", "No", "I don't, on purpose", "It's the cache" are all fine starts.
3. **Add only what they need to act on the answer.** Usually one reason, or one example, or one next step. Pick the one the asker cares about, which is rarely the one that is most interesting to you.
4. **Size it to their message.** A two-line question gets one to four sentences back. Go longer only when they asked for detail or steps.
5. **Check the draft.** Run `python3 scripts/check.py --lang <code>` on it, with the reply's language as an ISO code such as `en`, `it`, `fr`, `ja` (path relative to this skill's folder; it reads stdin or a file), and fix every line it prints. Then go through [`references/tells.md`](references/tells.md) and rewrite any sentence that matches, and read the reply once as if you were the asker. Done when the checker prints nothing, no tell from the list is left, and every sentence answers, supports the answer, or asks a question you actually want answered.

## New posts

The reader didn't ask anything, so the first sentence carries the point instead of the answer.

1. **Find the point.** Write down, for yourself, what the reader has to know or do after reading, in one line. For a PR: what changes for the user or the codebase. For an issue: what breaks, or what you want. For a commit: what this change does. For a post: the one thing you want people to take away.
2. **Lead with it.** The title or first sentence states the point in plain words ("Checkout no longer double-charges on retry", "Login fails on Safari 18 after the redirect").
3. **Add what the reader needs to act.** A PR: why, and what to look at when reviewing. An issue: steps to reproduce, what you expected, what happened. A commit body: why, when the subject line doesn't make it obvious. A post: one example or one link.
4. **Follow the place's conventions.** Use the repo's PR or issue template and its commit style (Conventional Commits, a 50 character subject, a body wrapped at 72) when it has them, with headers, lists and checkboxes where the template puts them. Everything you write inside those sections still follows the Rules.
5. **Check the draft** as in Steps, with `--kind post` for PR descriptions, issues and posts, or `--kind commit` for commit messages, so the checker accepts template headers and commit line wrapping.

## Rules

**Punctuation.** Join clauses with periods, commas, parentheses, or the language's plain connectors ("and", "but", "so", "because"). The dash depends on the language, because in many of them it is ordinary punctuation:

- **English, Japanese, Korean:** no em dash (—), en dash (–) or spaced double hyphen ( -- ) at all. Readers there treat them as the clearest sign a model wrote the text.
- **Russian:** use the dash where grammar requires it ("Москва — столица"), and nowhere else.
- **Every other language** (Italian, French, Spanish, German, Portuguese, Chinese...): at most one dash per reply, only where that language's rules call for it, never as a dramatic pause.

Hyphens inside words (follow-up, e-commerce) and inside code, commands, paths and URLs are fine everywhere. Vary the rhythm the way people do, with a mix of short and longer sentences, since a reply built only from short sentences, commas and periods now reads as generated too.

**Words.** Use the asker's vocabulary. If they said "orders", say "orders", not "the commerce layer". Name things the way a user of the product would, and leave internal terms, architecture words and file names out unless the asker used them first. Use contractions (I'm, it's, don't).

**One reason.** Give the single reason that matters. Three parallel reasons, three adjectives, or three examples in a row read as generated. If two facts matter, use two sentences.

**State things directly.** Say what is true. A contrast ("it's not X, it's Y") earns its place only when the asker actually believes X.

**Plain format.** A reply is sentences in paragraphs. Headers, bold labels and bullet lists belong in a reply only when the asker asked for steps or a list, and in a new post only where the place's template or convention puts them.

**Compact spacing.** Most replies are one or two paragraphs, and each paragraph holds a few sentences that run on as normal text. Put a single blank line between paragraphs, and let each sentence flow to the end without a manual line break; the comment box wraps it. Sentences that belong together share a paragraph, so a reply never becomes a column of one-line paragraphs with gaps between them.

**Start with the answer.** The first words are the answer itself. Labels that announce the answer ("Short answer:", "Great question!", "To clarify:", "TL;DR") and restating their question back to them are dropped.

**End on the answer.** The last sentence is either the final piece of the answer or one real question you want answered. A recap ("So the split is...") or a sign-off ("Hope this helps!", "Happy to dig deeper") gets cut.

**Match the room.** Reply in the thread's language and register. Casual thread, casual reply. Lowercase chat, lowercase is fine. A reviewer's terse comment gets a terse fix note ("Good catch, fixed in a3f9c1"). Use the language's own quote marks (« », „ “, 「」) and one style throughout, and keep the politeness that language and genre expect: an Italian or German email still opens with a greeting, a Japanese reply keeps keigo where the thread uses it, varied the way a person varies it.

**Stay honest.** Keep every fact and every real hedge. Humanizing changes the voice, never the claims. If you don't know, say "not sure" and what you'd check.

## Example

Someone asked how the plugin handles the commerce side, and mentioned they use Orderain for it.

Before:

> Short answer: I don't, on purpose.
>
> The plugin owns two things — the theme, and the store configuration the theme depends on: languages, menus, markets, currency, and the buying facts (shipping, returns) that get written into the product page copy instead of being invented.
>
> Products, collections, inventory, checkout and orders stay in Shopify. I went that way because the moment a tool starts managing orders it's rebuilding Shopify's admin badly, and the merchant ends up with two places to look for the same thing. Checkout is Shopify's anyway — a theme can't really own it.
>
> So the split I aim for is: the agent owns design and the files you end up with, Shopify owns commerce and the record of it.
>
> Curious what pushed you to Orderain for that side — was it something Shopify's admin genuinely doesn't do, or the UI?

After:

> I don't, on purpose. The plugin builds the theme and sets up what the theme needs, like languages, menus, currency and your shipping and returns info. Products, orders and checkout stay in Shopify, so you never have to check two places for the same order.
>
> What made you pick Orderain for that part? Something Shopify can't do, or just the UI?

What changed: the label before the answer, the dashes, the line breaks the original had in the middle of sentences, five paragraphs squeezed into two, the internal phrase "buying facts that get written into the product page copy", the second reason, and the recap line are gone. The answer, the one reason and the real question stayed.
