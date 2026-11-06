# STE word list for software writing

Read this file when you need a replacement for a word, or when you check a long document. The left column has words that cause problems for non-native readers or machine translation. The right column has the word to use. The list follows the approach of the ASD-STE100 dictionary, adapted for software text. It is not the ASD-STE100 dictionary.

## Contents

1. Complex words and their simple replacements
2. Phrasal verbs
3. Words with more than one meaning
4. Modal verbs
5. Filler phrases to remove
6. Idioms and metaphors common in software text

## 1. Complex words and their simple replacements

| Do not use | Use |
| --- | --- |
| accomplish, achieve | do, get |
| additional | more, other |
| adjacent to | next to |
| approximately | about |
| ascertain | find, make sure |
| assist, facilitate | help |
| attempt (verb) | try |
| commence, initiate | start |
| component (if a simpler name exists) | the name of the part |
| comprise, consist of | have, contain |
| demonstrate | show |
| determine | find, decide |
| due to | because of |
| eliminate | remove |
| ensure | make sure |
| equivalent | the same as, equal to |
| execute (a step or task) | do, run |
| expedite | make faster |
| failure to (do X) | if you do not (do X) |
| following (as a preposition) | after |
| implement (a step) | do. Keep "implement" as a technical verb for code. |
| indicate | show |
| leverage, utilize | use |
| locate | find |
| modify | change |
| numerous | many |
| obtain | get |
| perform | do |
| permit | let, allow |
| previously | before |
| prior to | before |
| provide | give |
| require | need |
| reside | be, is in |
| retain | keep |
| subsequently | then, after this |
| sufficient | enough |
| terminate | stop, end |
| verify | make sure, check |
| via | through, with |

"Verify", "execute", "terminate" and "initialize" are also technical verbs in some contexts (`terminate` a process, `execute` a query). Keep them when they name the exact technical action, and use them only in that meaning.

## 2. Phrasal verbs

| Do not use | Use |
| --- | --- |
| back up (support) | support |
| bring up (a service) | start |
| carry out | do |
| check out (examine) | examine. Keep `git checkout` as a technical name. |
| figure out, find out | find |
| fire off, kick off | send, start |
| get rid of | remove |
| go over | examine |
| hook up, wire up | connect |
| look into | examine, find the cause of |
| make sure of | make sure |
| point at (configuration) | set to, use |
| put in | add |
| run into (a problem) | get, have |
| set off | cause, start |
| sort out | correct, repair |
| spin up | start |
| take out | remove |
| turn on, turn off | start, stop (or enable, disable for a setting) |

Fixed technical terms such as "log in", "sign in", "roll back", "set up" (as a noun: "the setup") and "clean up" (as a noun: "the cleanup") are acceptable. Use the same form every time.

## 3. Words with more than one meaning

Use these words in one meaning only, or replace them.

| Word | Problem | Do this |
| --- | --- | --- |
| since | "because" or "after a time" | Use "because" or "after". |
| as | "because", "while" or "in the role of" | Use "because", "while" or "in the role of". |
| while | "at the same time" or "but" | Use "while" for time only. Use "but" for contrast. |
| once | "one time" or "after" | Use "after" or "when". |
| issue | "problem", "release" or "send" | Use "problem", "release" or "send". |
| run | "start", "operate" or "a single execution" | Use "run" for one meaning in a document. |
| address | "location" or "solve" | Use "address" for a location only. Use "solve" or "correct" for a problem. |
| call | "invoke" or "name" | Use "call" for a method or API call only. |
| clear | "remove" or "easy to understand" | Use "remove" or "easy to understand". |
| hit (an endpoint) | informal | Use "call" or "send a request to". |
| fire (an event) | informal | Use "raise" or "send". |
| drop | "remove", "lose" or "decrease" | Use the specific word. |
| handle | "process" or "the object you hold" | Use "process", or keep "handle" as a technical name only. |
| state | "condition" or "say" | Use "state" for condition only. Use "say" or "tell" for speech. |

## 4. Modal verbs

| Do not use | Problem | Use |
| --- | --- | --- |
| should (instruction) | could mean "must" or "it is a good idea to" | "must" for a requirement, the imperative for an instruction, "we recommend that you" for advice |
| should (prediction) | could be read as an instruction | "will probably", "usually" |
| may (permission) | could mean "possibly" | "can" |
| might, could (possibility) | weak and vague | "can", or give the condition: "If X, Y occurs." |
| would | conditional tense | "will", or rewrite as "If X, Y occurs." |
| need to | indirect | the imperative: "Set X." |

Exception: in a spec that defines RFC 2119 keywords (MUST, SHOULD, MAY), keep those keywords with their defined meaning.

## 5. Filler phrases to remove

| Do not use | Use |
| --- | --- |
| in order to | to |
| it is important to note that | (delete) |
| please note that | (delete, or make it a note) |
| basically, actually, simply, just | (delete) |
| at this point in time | now |
| in the event that | if |
| for the purpose of | to, for |
| with regard to, in terms of | about, for |
| a number of | some, or the number |
| is able to | can |
| has the ability to | can |
| make a decision | decide |
| perform a check of | check |
| it should be noted that | (delete) |
| there is / there are (at the start of a sentence) | rewrite with a real subject |

## 6. Idioms and metaphors common in software text

| Do not use | Use |
| --- | --- |
| out of the box | by default, with no changes |
| under the hood | internally |
| on the fly | while it runs, at run time |
| happy path | the normal case, the success case |
| low-hanging fruit | easy changes |
| moving target | a requirement that changes |
| smoking gun | the cause, the evidence |
| silver bullet | a complete solution |
| boil the ocean | do too much |
| single source of truth | the one authoritative source |
| belt and braces | two checks for the same risk |
| a no-op | no change, nothing happens |
| wire up | connect, register |
| dial up / dial down (traffic) | increase, decrease |
| land (a change) | merge |
| plumbing | the connection code, the configuration |
| bake in | include |
| blast radius | the affected area |
