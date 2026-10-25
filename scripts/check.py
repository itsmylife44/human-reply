#!/usr/bin/env python3
"""Flag machine tells in a reply draft. Prints one line per issue, exits 1 if any.

Usage: python3 check.py --lang it draft.txt   or   echo "text" | python3 check.py --lang en
--lang is the reply's ISO code (default en). Unknown codes get the universal checks only.
--kind reply (default), post (PR description, issue, post: template headers allowed)
or commit (also allows the 72-column wrap).
Self-test: python3 check.py --selftest
"""
import argparse
import re
import sys

# Checks for every language.
UNIVERSAL = [(r"\s--\s", "double hyphen used as a dash")]
FORMAT = [(r"^\s*#{1,6}\s|\*\*[^*]+\*\*:", "header or bold label: write plain sentences")]  # replies only

# English phrasing tells. Other languages carry their own pack in WRAPPERS.
ENGLISH = [
    (r"^\s*(short answer|tl;?dr|great question|good question|to clarify|in short|certainly|of course)\b",
     "label before the answer: start with the answer itself"),
    (r"\b(here'?s the thing|the thing is|honestly\?|let'?s (break|dive)|quick note)\b",
     "staged run-up: make the point directly"),
    (r"\b(to be clear|i'?m not saying|don'?t get me wrong)\b", "arguing with no one: drop the defense"),
    (r"\b(you'?re absolutely right|want me to|would you like|hope (this|that) helps|happy to (help|clarify|dig)"
     r"|let me know if|feel free to)\b", "chatbot wrapper: end on the answer"),
    (r"\b(let that sink in|that'?s the real|that distinction matters|at its core|what really matters)\b",
     "line that sounds deep but adds nothing: state the plain claim"),
    (r"\bnot (just|only|merely)\b[^.?!]*\bbut\b", "'not just X but Y' contrast: state it directly"),
    (r"\bit'?s not\b[^.?!]*,\s*it'?s\b", "'it's not X, it's Y' contrast: state it directly"),
    (r"^\s*(so|in summary|to sum up|overall),?\s", "recap line: cut it"),
    (r"\b(additionally|delve|leverage|seamless(ly)?|robust|holistic|game[- ]changer|crucial|pivotal"
     r"|showcase|testament|underscores?|meticulous(ly)?|vibrant|garner|interplay|intricate)\b",
     "stock AI word: use a plainer one"),
    (r"\b(serves as|stands as|functions as|boasts)\b", "long verb: use is, are or has"),
]

# Chatbot openers, closers and recaps per language, from the localized humanizer skills
# and Wikipedia's AI-signs pages. ponytail: one regex per language, add a language with one line.
WRAPPERS = {
    "it": r"certamente!|ottima domanda|vediamo insieme|sono qui per aiutarti|spero (che questo )?ti sia (stato )?utile"
          r"|spero di esserti stat[oa] utile|fammi sapere se|non esitare a|in sintesi,|in conclusione,"
          r"|gioca un ruolo (cruciale|fondamentale)",
    "fr": r"j['’]espère que (cela|ça) (vous|t['’])aide|bien sûr\s?!|absolument\s?!"
          r"|vous avez tout à fait raison|souhaitez-vous que|n['’]hésitez pas à"
          r"|excellente question|en résumé,|en conclusion,",
    "es": r"espero que esto te ayude|^\s*¡claro!|¡por supuesto!|tienes toda la razón"
          r"|excelente pregunta|no dudes en|en resumen,|en conclusión,",
    "pt": r"espero ter ajudado|^\s*claro!|com certeza!|você está absolutamente cert[oa]"
          r"|você gostaria de|me avise|ótima pergunta|em resumo,|em conclusão,",
    "de": r"ich hoffe,? das hilft|im kern|in wirklichkeit|gute frage!|zusammenfassend|zögere nicht",
    "ru": r"стоит отметить, что"
          r"|важно (понимать|отметить), что"
          r"|можно с уверенностью сказать"
          r"|подводя итог|^\s*таким образом,"
          r"|в современном мире"
          r"|надеюсь, это поможет"
          r"|отличный вопрос",
    "zh": r"好问题|希望(这|以上)对(您|你)有(所)?帮助"
          r"|总而言之|综上所述|拭目以待|不断发展的时代",
    "ja": r"ここでは.{0,20}について解説します"
          r"|注目を集めています|以上のことから"
          r"|お役に立てれば幸いです|良い質問ですね",
    "ko": r"좋은 질문이(에요|네요|입니다)|도움이 되었으면"
          r"|정말 훌륭한 지적|결론적으로|요약하면",
}

STRICT_DASH = {"en", "ja", "ko"}  # dashes are rare in normal writing there, so any dash is a tell
NO_SPACES = {"zh", "ja"}  # word counts mean nothing without spaces
CODE = re.compile(r"```.*?```|`[^`]*`|<!--.*?-->|https?://\S+", re.S)
BLOCK_START = re.compile(r"\s*([-*>#]|\d+[.)])\s")  # list items, quotes and headers start their own line
SENTENCE_END = re.compile(r"[.!?:;)\"'»”’」。！？]\s*$")


def dash_issues(text, lang):
    if lang in STRICT_DASH:
        return [f"line {n}: dash: use a period, comma or parentheses"
                for n, line in enumerate(text.splitlines(), 1) if re.search("[—–]", line)]
    if lang == "zh":
        if re.search("(?<!—)—(?!—)", text):
            return ["single half-width dash: Chinese uses ——, or rewrite with ， or 。"]
        count = len(re.findall("——", text))
    else:
        count = len(re.findall("[—–]", text))
    # ponytail: Russian grammatical dashes count too, a reply rarely needs two
    return [f"{count} dashes: keep at most one, where the language requires it"] if count > 1 else []


def quote_styles(text):
    styles = set()
    if '"' in text:
        styles.add("straight")
    if "„" in text:
        styles.add("low")  # German/Polish style closes with “ or ”, so those belong to it
    elif re.search("[“”]", text):
        styles.add("curly")
    if re.search("[«»]", text):
        styles.add("guillemets")
    if "「" in text:
        styles.add("corner")
    return styles


def breaks_mid_sentence(line, nxt):
    if not line.strip() or not nxt.strip() or SENTENCE_END.search(line):
        return False
    return not BLOCK_START.match(line) and not BLOCK_START.match(nxt)


def check(text, lang="en", kind="reply"):
    # blank out code and URLs (dashes and quotes there are fine) but keep newlines so line numbers hold
    text = CODE.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), text)
    lines = text.splitlines()
    patterns = UNIVERSAL + (FORMAT if kind == "reply" else []) + (ENGLISH if lang == "en" else [])
    if lang in WRAPPERS:
        patterns = patterns + [(WRAPPERS[lang], f"stock chatbot phrase ({lang}): cut it or say it plainly")]
    issues = dash_issues(text, lang)
    for n, line in enumerate(lines, 1):
        for pat, msg in patterns:
            if re.search(pat, line, re.I):
                issues.append(f"line {n}: {msg}")
        nxt = lines[n] if n < len(lines) else ""
        if kind != "commit" and breaks_mid_sentence(line, nxt):
            issues.append(f"line {n}: line break in the middle of a sentence: let it run on")
    # ponytail: nested quotes in another style (French « “ ” ») trip this, rare in a short reply
    if len(quote_styles(text)) > 1:
        issues.append("mixed quote styles: pick the language's own and use it throughout")
    if re.search(r"\n[ \t]*\n[ \t]*\n", text):
        issues.append("more than one blank line between paragraphs: use a single one")
    paras = [p for p in re.split(r"\n[ \t]*\n", text.strip()) if p.strip()]
    # ponytail: word-count heuristic, a reply with 3+ paragraphs averaging under 15 words is fragmented
    fragmented = len(paras) >= 3 and sum(len(p.split()) for p in paras) / len(paras) < 15
    if kind == "reply" and lang not in NO_SPACES and fragmented:
        issues.append(f"{len(paras)} short paragraphs: merge sentences that belong together")
    return issues


def selftest():
    # English
    assert check("I don't, on purpose — really.")
    assert check("Short answer: no.")
    assert check("Hope this helps!")
    assert check("It's not a bug, it's a feature.")
    assert check("So the split is: A and B.")
    assert check("The plugin owns the theme and the\nstore settings.")
    assert check("First point.\n\n\nSecond point.")
    assert check("Yes.\n\nIt works.\n\nTry it.")
    assert check('He said "yes" and “no”.')
    assert not check("I don't, on purpose. Run `ls -- -x` or see https://a.b/c--d")
    assert not check("Good catch, fixed in a3f9c1. The follow-up is in #12.")
    assert not check("Two steps:\n- run the build\n- open the app")
    # other languages: one dash is fine, two are not, own quotes are fine
    assert not check("Lo faccio apposta — il checkout resta su Shopify.", "it")
    assert check("Uno — due — tre.", "it")
    assert check("Spero di esserti stato utile!", "it")
    assert not check("Il dit « oui » et c'est fait.", "fr")
    assert check("N'hésitez pas à demander.", "fr")
    assert not check("Москва — столица.", "ru")
    assert check("Надеюсь, это поможет.", "ru")
    assert not check("Er sagt „ja“ und geht.", "de")
    assert check("希望这对你有帮助。", "zh")
    assert check("そうです — たぶん。", "ja")
    assert not check("そうです。いいですね。", "ja")
    # new posts: template headers and commit wrapping are fine, dashes still are not
    assert not check("## Summary\n\nCheckout no longer double-charges on retry.\n\n<!-- template -- note -->", kind="post")
    assert check("## Summary\n\nCheckout no longer double-charges on retry.")
    assert not check("Fix double charge on retry\n\nThe retry handler reused the old payment\nintent, so Stripe charged twice.", kind="commit")
    assert check("Fix double charge \u2014 finally", kind="commit")
    print("selftest ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Flag machine tells in a reply draft.")
    ap.add_argument("file", nargs="?", help="draft file; reads stdin when omitted")
    ap.add_argument("--lang", default="en", help="reply language as an ISO code, e.g. en, it, fr, ja")
    ap.add_argument("--kind", default="reply", choices=["reply", "post", "commit"])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        sys.exit(0)
    src = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    found = check(src, args.lang.lower().split("-")[0], args.kind)
    if found:
        print("\n".join(found))
    sys.exit(1 if found else 0)
