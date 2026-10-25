# Tells to cut from a reply

Read this during the check step, after `scripts/check.py` runs clean. The checker already flags dashes, mid-sentence line breaks, split short replies, mixed quote styles, labels before the answer, chatbot wrappers, recap lines, "not X but Y" contrasts, stock AI words and the stock phrases of each language it knows. This list is what a regex can't see. Each item is a habit models have and people mostly don't. One weak tell alone proves little; several together make a reply read as generated. Fix by rewriting the sentence, keeping every fact.

Adapted for replies from [blader/humanizer](https://github.com/blader/humanizer) (MIT), which is based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

The tells are ideas, not English words. In another language, find that language's version of the same move (its chatbot wrapper, its stock words, its run-ups) and rewrite it. Leave alone what the language does normally: Chinese 首先/其次 when they mark a real order, « » and „ “ quotes, the Russian subject–predicate dash.

## Rebuilding what the reader knows

The strongest tell in a reply. The asker already has the context, so restating their problem, walking through the diagnosis, or proving the plan works before reaching the answer buries the point. Lead with the decision and keep only the one fact they lack and any link they need. The full write-up belongs in the ticket or doc.

## Staging instead of stating

- **Run-ups:** a standalone "Look," or any opener that delays the point. Cut the run-up and make the point.
- **Arguing with no one:** "You might think... but", or any defense against something nobody in the thread said. Drop the defense.
- **One-line closers:** a row of fragments ("No setup. No config."), or a short last line that repeats what came before. Keep a short line only when it adds a new fact.
- **Sayings that sound deep:** "the real question is", "X is the Y of Z". Replace with the plain claim.

## Rhythm by rule

- **Triads:** three reasons, adjectives or examples in a row. Keep the one that matters.
- **Same opener:** several sentences in a row starting with the same word ("It... It... It..."). Merge them or start with the action.
- **Stacked qualifiers:** "could potentially", "might arguably", "in some cases it may". Keep one hedge where the doubt is real.

## Inflated words

- **Stock AI words the checker skips:** key as an adjective ("the key point") and highlight as a verb ("highlights the need"). The nouns ("API key", "syntax highlight") are fine.
- **Long verbs for simple ones:** "features" as a verb ("the app features..."). Use has.
- **-ing riders:** "..., ensuring a smooth experience", "..., highlighting the need for". Cut the rider or state the fact it hints at.
- **Sales tone:** groundbreaking, stunning, "a step in the right direction". Say what the thing does.

## Chat leftovers

- **Knowledge disclaimers:** "as of my last update", "based on available information". Say what you don't know plainly, or cut it.

## Language-specific tells

Mostly small in a short reply, but worth a look. Sources are the localized humanizer skills and the Wikipedia AI-signs pages in each language.

- **Italian:** "Non è X, è Y", a subject pronoun in every sentence where Italian would drop it.
- **French:** calques like "faire du sens", "adresser un problème", "impacter"; crucial, également, notamment everywhere.
- **Russian:** bureaucratic nouns (осуществление, обеспечение, в рамках), "данный", "является" over and over.
- **Chinese:** 进行 + verb, stacked 的, 随着…的发展 openers.
- **Japanese:** the same keigo pace in every sentence, a subject stated each time, 〜することができます.
- **Korean:** one politeness level (합니다) with no variation, or levels mixed inside a paragraph; commas in most sentences; translationese (에 대해, 통해, 되어진다).
