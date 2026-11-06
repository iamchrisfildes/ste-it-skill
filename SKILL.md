---
name: ste-it
description: Write or rewrite technical text in Simplified Technical English (STE), a controlled-language style based on ASD-STE100. STE uses short sentences, one instruction per step, the active voice, one word for one meaning and no idioms. Use this skill as a style layer on top of other skills and tasks, or to convert existing text into STE. Use it when the user says "use STE", "in simplified technical English", "STE style", "plain technical English" or "easy for non-native readers", or mentions ASD-STE100. Do not use it when the user does not ask for STE. When the user asks for STE, it applies to any document, such as a spec, runbook, PR description or code comment, and to text that an AI agent reads, such as a system prompt or a skill file. It applies also when another skill produces the document.
license: MIT
---

# Simplified Technical English

STE is a controlled form of English for technical text. Its goal is that each reader gets the same meaning on the first read. These readers include people whose first language is not English, people in a hurry, machine translators, search tools and AI agents. STE gets this result with limits on sentence length, sentence structure and vocabulary.

This skill follows the ASD-STE100 writing rules. It does not limit the text to the ASD-STE100 dictionary, because software text needs the names of real software parts, tools and concepts. The section "Technical names and technical verbs" tells you how to use these names.

This skill does not make text compliant with ASD-STE100. Do not say that a text complies with ASD-STE100 or that it has STE certification. Say that the text uses an STE style or follows the STE writing rules.

## Two ways to use this skill

**1. As a style layer on another task (the main use).** The user asks for a document, such as a spec, plan, task list or runbook, and tells you to use STE. Another skill, or the request, sets the content and the structure. This skill sets the form of each sentence.

In style-layer mode, keep the template, headings, sections and necessary content of the other skill. Write the prose inside them in STE. Do not add change notes or an STE report, because the document is the output.

**2. As a converter.** The user gives you text and asks for it in STE. Rewrite it. Keep the meaning, the structure (headings, lists, tables) and all technical content. If the text is long and has no headings, you can add headings to help the reader find each part.

After a conversion, write a short list of items that you cannot solve. An example is a sentence with two possible meanings, where you had to choose one. If there is nothing to report, give only the rewrite.

In both cases, write in STE from the start. Do not write normal text first and then convert it. The result is cleaner, and you do the work only one time.

## Choose the strictness level

The cost of an incorrect reading sets the level. Use the strict level or the light level. If the user names a level, use that level.

**Strict level.** Apply all the rules in this skill and the full word list. Use the strict level for text where an incorrect reading causes an incorrect action:

- Text that an AI agent or a tool reads: system prompts, tool descriptions, AGENTS.md, CLAUDE.md, skill files and other prompts
- Procedures, runbooks, installation steps and the response steps of an incident report
- Warnings, cautions and error messages
- Requirements, acceptance criteria and task lists
- Docstrings and descriptions of public APIs

**Light level.** Apply all the rules for sentences, paragraphs, procedures and protected items. The vocabulary rules are less strict:

- You can use a word from section 1 of the word list if your readers know it and it is more exact. Examples are "determine" and "provide".
- You can use an "-ing" word if the other form is longer or less clear.
- These rules stay: no phrasal verbs, no idioms, no filler phrases, no "should", no contractions and one word for one meaning.

Use the light level for text that explains, where the reader does not act on each sentence:

- Design rationale, the context of an ADR, analysis, and the overview parts of a README or spec
- PR descriptions, the body of a commit message and release notes
- The timeline and the cause in an incident report
- Code comments and emails

**Documents with two types of text.** Use the correct level for each part. In a runbook, use the strict level for the steps and the light level for the background. If you are not sure which level applies, use the strict level.

## What you must not change

STE applies to prose. Keep these items exactly as they are. A change to them can break a command or change the meaning.

- Code, commands, file paths, URLs, configuration keys, environment variable names, log messages and error text from a system
- Identifiers: the names of classes, methods, endpoints, fields and operations (`getOrder`, `Payments__ApiBaseUrl`)
- Text quoted from another source, such as a requirement from a ticket
- Requirement keywords that the document defines. If a spec uses MUST, SHOULD and MAY (RFC 2119), keep them with their defined meanings.
- Product names and other proper names

If a quoted item is not clear, explain it in an STE sentence next to it. Do not edit the quoted item.

## Writing rules

### Sentences

- **Use a maximum of 20 words in a procedure sentence and 25 words in a descriptive sentence.** A code item or identifier counts as one word. If a sentence is longer, split it. Long sentences are the main cause of incorrect reading.
- **Write about one topic in each sentence.** If "and" joins two different facts, write two sentences.
- **Use the active voice.** Name the actor: "The handler logs the reply status", not "The reply status is logged". In descriptive text, use the passive voice only when the actor is not known or is not important.
- **Use simple verb tenses:** the present, the past and the future ("logs", "logged", "will log"). Do not use forms such as "has been logging" or "would have logged".
- **Keep the short words.** Keep "the", "a", "this" and "that". "Make sure that the service is running" is clearer than "Make sure service running". Text with missing words is more difficult for non-native readers, not easier.
- **Do not use contractions.** Write "do not", "it is" and "cannot".

### Paragraphs and references

- **Use a maximum of 6 sentences in a paragraph.** Write about one topic in each paragraph.
- **Name the subject in the first sentence of each paragraph.** Write "The gateway sends each request to...", not "It sends each request to...". A reader can go directly to one paragraph. A search tool can give an agent only one paragraph of the document. In both cases, the reader must know the subject from that paragraph.
- **Do not start a paragraph with "it", "this", "they" or "the service"** if the name is in an earlier paragraph. In a paragraph, "it" and "this" are acceptable if they refer to a noun in the previous sentence.
- **Apply the same rule to list items that a reader reads alone**, such as a requirement, a task or an acceptance criterion.
- **If you choose the headings, put the subject in each heading.** Write "Retry policy for the payments API", not "Details". Do not change a heading that the user, the template or the source text gives. Do not add headings to a section that the user or the template defines.

### Procedures and instructions

- **Write each step as a command.** Use the imperative: "Set the base URL." Do not write "You should set the base URL" or "The base URL needs to be set".
- **Write one instruction in each step.** Put two actions in one sentence only if the reader must do them at the same time ("Hold the button and turn the key").
- **Put the condition first.** Write "If the readiness probe fails, examine the connection string." The reader must know the condition before the action.
- **Use a numbered list for steps in a sequence.** Use bullets for items that have no sequence.
- **Tell the reader the result** when this helps them to make sure the step worked: "Run `docker ps`. The `orders-api` container shows `healthy`."

### Text that an AI agent reads

An AI agent is a reader that cannot ask a question. The agent reads the words, chooses one meaning and acts on that meaning. A human reader who is not sure can ask the writer. An agent continues with its guess. Thus, use the strict level for all text that an agent reads, and apply these rules exactly:

- **Use the imperative for an instruction:** "Run the tests before you commit."
- **Use "must" for a requirement on a result or a condition:** "The reply must be valid JSON."
- **Use "can" only for a permitted option:** "If the cache is empty, you can skip step 3." Do not use "may" for an option, because an agent can read "may" as "possibly". For a possible event, give the condition: "If the cache is empty, the first request takes 2 seconds."
- **Do not use words that leave the decision open,** such as "should", "ideally", "if possible" or "try to". Write the rule. If the rule has exceptions, write each exception as a condition.
- **Use the names that the code or the tool uses.** If the tool parameter is `repo_path`, write `repo_path`, not "the repository folder".

### Warnings and cautions

- Start with a clear command, then give the risk: "Do not run the migration twice. A second run creates duplicate rows."
- Use **Warning** for a risk of injury or data loss. Use **Caution** for a risk of damage to equipment or systems. Use a note for other information.
- Do not put a command in a note. If the reader must do it, make it a step.

### Words

- **Use one word for one meaning.** In a document, give each word only one meaning, and use only one word for each thing. If you call it "the gateway" one time, do not call it "the proxy" later. A non-native reader thinks that two words are two different things. A search tool does not find the paragraphs that use the other word.
- **For a long document, make a glossary before you write.** Do this if the document has more than about 1,000 words or more than 5 technical names. For each important thing, write the one word that you will use and the words that you will not use: "gateway (not: proxy, router)". Use this glossary when you write and when you check. Do not add the glossary to the document, unless the template has a glossary section or the user asks for one.
- **Use the simple, common word.** Write "use", not "utilize". Write "start", not "initiate". Write "help", not "facilitate". The file `references/word-list.md` has the full list. Read it when you need a replacement word or when you check a long document.
- **Do not use phrasal verbs if a single verb has the same meaning.** Write "start", not "fire up". Write "find", not "find out". Write "remove", not "get rid of". Phrasal verbs are difficult for non-native readers and for machine translation. A phrasal verb that is the technical name of an action is acceptable, such as "log in" or "roll back". Use it the same way each time.
- **Do not use idioms, slang or metaphors**, such as "out of the box", "under the hood" or "low-hanging fruit". Write the fact that the idiom stands for.
- **Do not use "-ing" words if a different form is possible.** Write "Before you deploy", not "Before deploying". An "-ing" word can be a noun, an adjective or a verb, so its meaning is less clear. Technical names that end in "-ing" are acceptable, such as "logging", "routing" and "caching".
- **Do not use more than three nouns in a row.** "The payments API base URL configuration value" is difficult to read. Write "the value of the payments API base URL setting", or give the key.
- **Use exact words for quantity and time.** Write "in 2 hours", not "soon". Write "3 retries", not "a few retries". If you know the number, write "all 67 cases", not "most cases".
- **Do not use "should" in an instruction.** The word can mean "must", "it is a good idea to" or "it is probably true that". Use "must" for a requirement, the imperative for an instruction and "can" for an option. The exception is a spec that defines SHOULD (see "What you must not change").

### Technical names and technical verbs

ASD-STE100 lets you use words that are not in its dictionary if they are technical names or technical verbs. A technical name is the name of a thing, and a technical verb is the name of an action in your field. In software, these include *endpoint, container, cache, queue, schema, deploy, commit, merge, serialize* and *authenticate*.

- Use a technical name if your readers know it and no simpler word has the same meaning.
- Use it the same way each time.
- If some readers possibly do not know it, give a definition at its first use. For example: "the gateway (the service that sends each request to the correct backend)".
- Do not use a technical word in place of a simple word. "Leverage the cache" does not contain a technical verb. Write "Use the cache".

## Use with other skills

- **The other skill sets the content and structure.** This skill does not add, remove or move sections. It does not change requirement keywords that the other skill defines.
- **Short fragments can stay short.** If the template has table cells, headings or checklist labels, keep them short. STE does not need full sentences in these places.
- **STE has priority for sentence form when the user asks for STE.** Other style guidance can ask for a varied rhythm, a personal voice or long sentences. For these points, follow STE.
- **Keep code, diagrams and data as the other skill makes them.**

## Check before you finish

Do the check in two parts. A script finds the mechanical problems, because models count words badly. Then you read the text for the problems of meaning.

**Part 1: Run the checker.** If the text is not in a file, save it to a temporary file. Run the script `scripts/check_ste.py` from the folder of this skill:

```
python scripts/check_ste.py FILE --level strict
```

Use `--level light` for text at the light level. If `python` is not on the path, use `uv run --no-project python` or `py`. The script ignores code blocks, inline code, tables, headings and text in double quotes. It also ignores the lines between `<!-- ste-ignore-start -->` and `<!-- ste-ignore-end -->`. Use these markers only for text that must stay as it is, such as an example of bad text. The script reports these items:

- Sentences longer than 20 words (numbered steps and checklist items) or 25 words (other text). A code span counts as one word.
- Paragraphs with more than 6 sentences, and paragraphs and list items that start with a pronoun
- Steps that possibly contain two instructions
- Contractions, modal verbs, perfect tenses and possible passive verbs (also with "get")
- More than 3 nouns in a row
- "since", "once", "hit" and "issue" from section 3 of the word list
- Words from the word list, and "-ing" words after "before", "after", "when", "while", "by" or "without". At the light level, the script does not check section 1 of the word list or "-ing" words.

Each finding is a candidate. Correct it, or keep it for a reason, such as a technical name, a defined RFC 2119 keyword or a name from code. Run the script again until all the findings that remain have a reason. If you cannot run the script, do these checks when you read the text.

**Part 2: Read the text again.** Check these items. The script cannot find them.

1. For each step that the script found: does the step contain two instructions? If yes, split it. Also look for steps that the script did not find.
2. For each passive verb that the script found: do you know the actor? If yes, make the verb active.
3. Did you use two different words for the same thing? Compare the text with your glossary.
4. Does the text use a word from section 3 of the word list in two meanings? Examples are "as", "while", "run" and "call". Use the replacement from the list.
5. Does the first sentence of each paragraph name its subject?
6. Did you change code, an identifier, a path, quoted text or a requirement keyword? Change it back.
7. Did you use the correct level for each part of the text?
8. In converter mode, is the meaning the same as the original? If you had to guess, tell the user in the notes.
9. Did you say that the text complies with ASD-STE100? Remove that statement.

## Examples

**Procedure**

<!-- ste-ignore-start -->
Before:
> Once you've got everything up and running, you'll want to make sure the orders service is actually able to hit the payments API, so fire off a test order and keep an eye on the logs, which should show the call going out (if they don't, the env var probably isn't set).
<!-- ste-ignore-end -->

After:
> 1. Start the services.
> 2. Send a test order to `orders-api` on port 8080.
> 3. Examine the `orders-api` logs. The logs show a call to the payments API.
> 4. If the logs do not show this call, make sure that `Payments__ApiBaseUrl` has a value.

**Description**

<!-- ste-ignore-start -->
Before:
> Basically, the gateway sits in front of the old and new services and decides on the fly where each request goes, which lets us dial traffic up gradually while comparing results to catch regressions.
<!-- ste-ignore-end -->

After:
> The gateway receives each request and sends it to the old service or to the new service. A weight for each route sets the percentage of requests that go to each one. When comparison is on, the gateway also sends the request to the old service and compares the two replies. This shows differences before more traffic moves to the new service.

**Tool description (strict level, an agent reads it)**

<!-- ste-ignore-start -->
Before:
> Use this to look up orders. You should pass the customer ID if you have it, otherwise it'll fall back to searching by email, which may be slow. Results might be paginated.
<!-- ste-ignore-end -->

After:
> The `find_orders` tool finds the orders of one customer.
> - If you know the customer ID, give `customer_id`.
> - If you do not know the customer ID, give `email`. The search by `email` takes up to 10 seconds.
> - The tool returns a maximum of 50 orders. If the reply contains `next_page`, call the tool again with that value.

**Task list (style layer on a planning task)**

<!-- ste-ignore-start -->
Before:
> - [ ] Sort out the logging config so dev logs actually show up in the console
> - [ ] Look into why the metrics dashboard isn't getting anything from the orders service
<!-- ste-ignore-end -->

After:
> - [ ] Add a console sink to `logging.Development.json`, before the file sink.
> - [ ] Find why the metrics dashboard does not receive data from `orders-api`.
