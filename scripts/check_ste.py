#!/usr/bin/env python3
"""Find mechanical STE problems in a Markdown or plain-text file.

The script reports candidates, not verdicts. Correct each finding, or keep it for a reason
(technical name, quoted text, a defined RFC 2119 keyword, a name from code).

Usage: python check_ste.py FILE [--level strict|light]     FILE "-" reads stdin.
Exit code: 0 if no findings, 1 if findings.
"""

import argparse
import re
import sys
from pathlib import Path

WORD_LIST = Path(__file__).resolve().parent.parent / "references" / "word-list.md"
STRICT_SECTIONS = ("1.", "2.", "5.", "6.")  # section 3 needs a reading of meaning; section 4 is MODALS below
LIGHT_SECTIONS = ("2.", "5.", "6.")

PROCEDURE_MAX, DESCRIPTION_MAX, PARAGRAPH_MAX = 20, 25, 6

CONTRACTION = re.compile(
    r"\b\w+n['’]t\b|\b\w+['’](?:re|ll|ve|d|m)\b|\b(?:it|that|there|here|what|let|who)['’]s\b", re.I)
IRREGULAR = ("built|chosen|done|found|given|held|hidden|kept|known|lost|made|put|read|run|seen|sent|"
             "set|shown|split|taken|told|thrown|written|broken")
PASSIVE = re.compile(
    rf"\b(?:is|are|was|were|be|been|being|get|gets|got|gotten|getting)\s+(?:\w+ly\s+)?(?:\w+ed|{IRREGULAR})\b", re.I)
PERFECT = re.compile(
    rf"\b(?:(?:will|would|could|should|might|must)\s+have|has|have|had)\s+(?:not\s+)?(?:\w+ly\s+)?(?:been|\w+ed|{IRREGULAR})\b",
    re.I)
MEANING = re.compile(r"\b(?:[Ss]ince|[Oo]nce|hit|hits|hitting|issue|issues|issued|issuing)\b")  # section 3, low noise only
MODALS_STRICT = re.compile(r"\b(?:[Ss]hould|[Mm]ay|[Mm]ight|[Cc]ould|[Ww]ould|[Nn]eeds? to)\b")
MODALS_LIGHT = re.compile(r"\b[Ss]hould\b")
ING_AFTER = re.compile(r"\b(?:[Bb]efore|[Aa]fter|[Ww]hen|[Ww]hile|[Bb]y|[Ww]ithout)\s+\w+ing\b")
PRONOUN_START = re.compile(
    r"^(?:It|Its|They|Their)\b"
    r"|^(?:This|That|These|Those)\s+(?:is|are|was|were|has|have|will|can|does|do|means|makes|lets|gives|shows|helps|causes|also)\b")

LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s+(?:\[[ xX]\]\s+)?|\d+[.)]\s+)")
STEP_ITEM = re.compile(r"^\s*(?:\d+[.)]\s+|[-*+]\s+\[[ xX]\]\s+)")
IGNORE_START, IGNORE_END = "<!-- ste-ignore-start -->", "<!-- ste-ignore-end -->"

IMPERATIVES = ("add|apply|build|call|change|check|clear|click|clone|close|commit|configure|connect|copy|create|"
               "delete|deploy|disable|download|edit|enable|enter|examine|export|fetch|find|give|import|install|"
               "make|merge|monitor|move|open|press|pull|push|put|read|rebuild|record|register|reload|remove|"
               "rename|replace|reset|restart|restore|review|run|save|scale|select|send|set|start|stop|tag|tell|"
               "test|type|update|upload|use|verify|wait|write")
STEP_START = re.compile(rf"^(?:If [^,]+,\s*|When [^,]+,\s*)?(?:{IMPERATIVES})\b", re.I)
AND_IMPERATIVE = re.compile(rf"\band\s+(?:then\s+)?(?:{IMPERATIVES})\s+(?:the|a|an|this|that|it|all|each|CODE)\b")
THEN_IMPERATIVE = re.compile(rf",\s*then\s+(?:{IMPERATIVES})\b")
NO_ED_FORM = ("require",)  # 'required' is usually an adjective: 'a required parameter'

DETERMINER = r"(?:the|a|an|this|that|these|those|each|every|our|your|its|their)"
FUNCTION_WORDS = set((
    "a an the this that these those each every all any some no not and or but if when while before after "
    "because so than then to of in on at by for from with without into onto over under about as is are was "
    "were be been being has have had do does did will can must may might could would should it its they "
    "them their you your we our he she his her who whom whose which what where how there here one two three "
    "through across between during against per via like until within also only more most less too very "
    "never always still again up down out off same other new first last").split())
NOUN_STACK_MIN = 4


def load_terms(sections: tuple[str, ...]) -> list[tuple[re.Pattern, str, str]]:
    terms, section = [], ""
    for line in WORD_LIST.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not section.startswith(sections) or not line.startswith("|") or line.startswith(("| Do not use", "| ---")):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        raw, use = cells[0], cells[-1]
        anchored = "start of a sentence" in raw
        preposition = "as a preposition" in raw
        for term in re.split(r"[,/]", re.sub(r"\([^)]*\)", "", raw)):
            term = term.strip()
            if term:
                terms.append((term_pattern(term, anchored, preposition), term, use))
    return terms


def term_pattern(term: str, anchored: bool, preposition: bool = False) -> re.Pattern:
    words = term.split()
    first = words[0]
    if len(first) <= 3:
        head = re.escape(first)
    elif first in NO_ED_FORM:
        head = re.escape(first[:-1]) + "(?:e|es|ing)"
    elif first.endswith("e"):
        head = re.escape(first[:-1]) + "(?:e|es|ed|ing)"
    elif first.endswith("y"):
        head = re.escape(first[:-1]) + "(?:y|ies|ied|ying)"
    else:
        head = re.escape(first) + "(?:s|es|ed|ing)?"
    body = r"\s+".join([head] + [re.escape(w) for w in words[1:]])
    start = r"(?:^|(?<=[.!?]\s))" if anchored else r"(?<![\w-])"
    if preposition:
        start += r"(?<!the\s)"  # 'the following steps' is an adjective, not a preposition
    return re.compile(start + body + r"(?![\w-])", re.I)


def clean(line: str, drop_quotes: bool) -> str:
    line = re.sub(r"`[^`]*`", "CODE", line)  # a code span counts as one word
    line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"https?://\S+", "URL", line)
    line = re.sub(r"\*\*|__|(?<!\w)[*_](?=\w)|(?<=\w)[*_](?!\w)", "", line)
    if drop_quotes:
        line = re.sub(r"\"[^\"]*\"|“[^”]*”", "QUOTE", line)
    return line


def prose_units(text: str) -> list[tuple[int, str, str]]:
    """(start line, kind, text) where kind is 'step', 'item' or 'para'. Skips code, tables, headings, HTML."""
    units: list[list] = []
    lines = text.splitlines()
    in_code = in_front = ignoring = False
    current = None
    for n, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if n == 1 and stripped == "---":
            in_front = True
            continue
        if in_front:
            in_front = stripped != "---"
            continue
        if stripped in (IGNORE_START, IGNORE_END):
            ignoring = stripped == IGNORE_START
            current = None
            continue
        if ignoring:
            continue
        if stripped.startswith(("```", "~~~")):
            in_code = not in_code
            current = None
            continue
        if in_code or not stripped or stripped.startswith(("#", "|", "<", "---", "[")):
            current = None
            continue
        body = re.sub(r"^\s*(?:>\s?)+", "", raw)
        if LIST_ITEM.match(body):
            kind = "step" if STEP_ITEM.match(body) else "item"
            current = [n, kind, LIST_ITEM.sub("", body, count=1).strip()]
            units.append(current)
        elif current is not None and (current[1] == "para" or raw[:1].isspace()):
            current[2] += " " + body.strip()
        else:
            current = [n, "para", body.strip()]
            units.append(current)
    return [tuple(u) for u in units]


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?:(?<=[.!?])|(?<=[.!?][\"”')]))\s+(?=[A-Z0-9\"“(])", text) if s.strip()]


def word_count(sentence: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][\w'’./:-]*", sentence))


def noun_stacks(text: str) -> list[str]:
    """Runs of 4 or more content words after a determiner, such as 'the payments API base URL value'."""
    stacks = []
    for m in re.finditer(rf"\b{DETERMINER}\s+((?:[\w-]+\s+){{{NOUN_STACK_MIN - 1},}}[\w-]+)", text, re.I):
        run = []
        for i, word in enumerate(m.group(1).split()):
            if word.lower() in FUNCTION_WORDS or re.search(r"(?:ly|ed|ing)$", word):
                break
            if i > 0 and re.fullmatch(r"[a-z]+s", word):  # probably a present-tense verb: 'the log entry shows'
                break
            run.append(word)
        if len(run) >= NOUN_STACK_MIN:
            stacks.append(" ".join(run))
    return stacks


def check(text: str, level: str) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    seen: set[tuple[int, str]] = set()
    terms = load_terms(STRICT_SECTIONS if level == "strict" else LIGHT_SECTIONS)
    modals = MODALS_STRICT if level == "strict" else MODALS_LIGHT

    def add(line: int, category: str, message: str, matched: str | None = None) -> None:
        if matched is not None:
            key = (line, matched.lower())
            if key in seen:
                return
            seen.add(key)
        findings.append((line, category, message))

    for start, kind, raw in prose_units(text):
        unit = clean(raw, drop_quotes=False)
        limit = PROCEDURE_MAX if kind == "step" else DESCRIPTION_MAX
        sents = sentences(unit)
        for s in sents:
            n = word_count(s)
            if n > limit:
                label = "procedure" if kind == "step" else "description"
                add(start, "length", f"{n} words (max {limit}, {label}): {s[:90]}")
        if kind == "para" and len(sents) > PARAGRAPH_MAX:
            add(start, "paragraph", f"{len(sents)} sentences (max {PARAGRAPH_MAX})")
        if PRONOUN_START.match(unit):
            label = "paragraph" if kind == "para" else "list item"
            add(start, "subject", f"{label} starts with a pronoun; name the subject: {unit[:60]}")
        if kind == "step":
            commands = [s for s in sents if STEP_START.match(s)]
            joined = AND_IMPERATIVE.search(unit)
            then = THEN_IMPERATIVE.search(unit)
            if then and not STEP_START.match(unit[:then.start()]):  # 'If X, then do Y' is one instruction
                then = None
            if len(commands) > 1 or joined or then:
                add(start, "one-step", f"possibly two instructions; split the step: {unit[:80]}")

        words_only = clean(raw, drop_quotes=True)
        for stack in noun_stacks(words_only):
            add(start, "nouns", f"'{stack}': more than 3 nouns in a row; use 'of' or the key name", stack)
        for m in CONTRACTION.finditer(words_only):
            add(start, "contraction", m.group(0), m.group(0))
        for m in modals.finditer(words_only):
            add(start, "modal", f"'{m.group(0)}': use must, can or the imperative", m.group(0))
        for m in PERFECT.finditer(words_only):
            add(start, "tense", f"'{m.group(0)}': use the present, past or future tense", m.group(0))
        for m in PASSIVE.finditer(words_only):
            add(start, "passive", f"'{m.group(0)}': if you know the actor, make it active", m.group(0))
        if level == "strict":
            for m in ING_AFTER.finditer(words_only):
                add(start, "-ing", f"'{m.group(0)}': use a clause, such as 'before you deploy'", m.group(0))
        for m in MEANING.finditer(words_only):
            add(start, "meaning", f"'{m.group(0)}': more than one meaning; see section 3 of the word list",
                m.group(0))
        for pattern, term, use in terms:
            for m in pattern.finditer(words_only):
                add(start, "word", f"'{m.group(0)}' -> {use}", m.group(0))
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", help="Markdown or text file, or - for stdin")
    parser.add_argument("--level", choices=("strict", "light"), default="strict")
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.file).read_text(encoding="utf-8")
    findings = check(text, args.level)
    for line, category, message in sorted(findings):
        print(f"line {line} [{category}] {message}")
    print(f"{len(findings)} findings ({args.level}). Each finding is a candidate: correct it, or keep it for a reason.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
