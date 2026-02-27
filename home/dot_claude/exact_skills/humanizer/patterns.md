---
description: Full reference of 24 AI writing patterns with signal words and before/after examples
---

# AI Writing Patterns Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).

---

## Content Patterns

### 1. Significance inflation

**Watch for:** stands/serves as, testament, vital/crucial/pivotal role/moment, underscores/highlights importance, reflects broader, evolving landscape, indelible mark, deeply rooted, setting the stage

LLM writing inflates importance by claiming arbitrary things represent or contribute to broader topics.

> **Before:** The institute was established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain, part of a broader movement to decentralize administrative functions.
>
> **After:** The institute was established in 1989 to collect and publish regional statistics independently from Spain's national office.

### 2. Notability inflation

**Watch for:** independent coverage, local/regional/national media outlets, active social media presence, written by a leading expert

LLMs list media mentions without context to assert notability.

> **Before:** Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
>
> **After:** In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

### 3. Superficial -ing analyses

**Watch for:** highlighting..., underscoring..., emphasizing..., ensuring..., reflecting..., symbolizing..., showcasing..., cultivating..., fostering..., encompassing...

Present participle phrases tacked on to add fake depth.

> **Before:** The color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets and the Gulf of Mexico, reflecting the community's deep connection to the land.
>
> **After:** The temple uses blue, green, and gold. The architect said these reference local bluebonnets and the Gulf coast.

### 4. Promotional language

**Watch for:** boasts a, vibrant, rich (figurative), profound, nestled, in the heart of, groundbreaking, renowned, breathtaking, must-visit, stunning, natural beauty, commitment to

Neutral tone replaced with marketing copy, especially on cultural or geographic topics.

> **Before:** Nestled within the breathtaking region of Gonder, Alamata stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
>
> **After:** Alamata is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

### 5. Vague attributions

**Watch for:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications

Opinions attributed to unnamed authorities without specific sources.

> **Before:** Experts believe the river plays a crucial role in the regional ecosystem.
>
> **After:** The river supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

### 6. Formulaic challenges/prospects sections

**Watch for:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

Formulaic section that acknowledges problems then immediately dismisses them.

> **Before:** Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion. Despite these challenges, Korattur continues to thrive as an integral part of Chennai's growth.
>
> **After:** Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a drainage project in 2022 to address recurring floods.

---

## Language & Grammar Patterns

### 7. Overused AI vocabulary

**Watch for:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

These words appear far more frequently in post-2023 text and often co-occur.

> **Before:** Additionally, a distinctive feature is the incorporation of camel meat. An enduring testament to Italian influence is the adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
>
> **After:** Somali cuisine also includes camel meat, considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common in the south.

### 8. Copula avoidance

**Watch for:** serves as, stands as, marks, represents [a], boasts, features, offers [a]

Elaborate substitutes for simple "is", "are", "has".

> **Before:** Gallery 825 serves as the exhibition space. The gallery features four spaces and boasts over 3,000 square feet.
>
> **After:** Gallery 825 is the exhibition space. The gallery has four rooms totaling 3,000 square feet.

### 9. Negative parallelisms

**Watch for:** Not only...but..., It's not just about..., it's..., It's not merely..., it's...

Overused rhetorical construction.

> **Before:** It's not just about the beat; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
>
> **After:** The heavy beat adds to the aggressive tone.

### 10. Rule of three

**Watch for:** Three-item lists where two would suffice, forced triads

Ideas forced into groups of three to appear comprehensive.

> **Before:** The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
>
> **After:** The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Synonym cycling

**Watch for:** Same entity referred to by multiple names in quick succession (protagonist/main character/central figure/hero)

Repetition-penalty code causes excessive synonym substitution for the same referent.

> **Before:** The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
>
> **After:** The protagonist faces many challenges but eventually triumphs and returns home.

### 12. False ranges

**Watch for:** from X to Y constructions where X and Y are not on a meaningful scale

"From X to Y" constructions where the endpoints are not on a real spectrum.

> **Before:** Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter.
>
> **After:** The book covers the Big Bang, star formation, and current theories about dark matter.

---

## Style Patterns

### 13. Em dash overuse

Excessive em dashes (---) mimicking punchy sales writing. Replace with commas, periods, or parentheses.

> **Before:** The term is promoted by Dutch institutions---not by the people themselves. You don't say "Netherlands, Europe"---yet this mislabeling continues---even in official documents.
>
> **After:** The term is promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe," yet this mislabeling continues in official documents.

### 14. Mechanical boldface

Phrases bolded mechanically for emphasis without editorial purpose.

> **Before:** It blends **OKRs**, **KPIs**, and tools such as the **Business Model Canvas** and **Balanced Scorecard**.
>
> **After:** It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 15. Inline-header vertical lists

Lists where each item starts with a bolded header and colon. Convert to prose when possible.

> **Before:**
> - **User Experience:** The interface has been redesigned.
> - **Performance:** Algorithms have been optimized.
> - **Security:** End-to-end encryption has been added.
>
> **After:** The update redesigns the interface, optimizes algorithms for speed, and adds end-to-end encryption.

### 16. Title case headings

All main words capitalized in headings. Use sentence case instead.

> **Before:** ## Strategic Negotiations And Global Partnerships
>
> **After:** ## Strategic negotiations and global partnerships

### 17. Emoji decoration

Emojis decorating headings or bullet points without communicative purpose.

> **Before:** :rocket: **Launch Phase:** Q3 launch. :bulb: **Key Insight:** Users prefer simplicity.
>
> **After:** The product launches in Q3. User research showed a preference for simplicity.

### 18. Curly quotation marks

ChatGPT uses curly quotes instead of straight quotes. Replace with straight quotes.

---

## Communication Patterns

### 19. Chatbot artifacts

**Watch for:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

Conversational phrases from chatbot interaction left in published text.

> **Before:** Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
>
> **After:** The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 20. Knowledge-cutoff disclaimers

**Watch for:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

AI disclaimers about data freshness left in text.

> **Before:** While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
>
> **After:** The company was founded in 1994, according to its registration documents.

### 21. Sycophantic tone

**Watch for:** Great question!, You're absolutely right, That's an excellent point, What a wonderful...

Overly positive, people-pleasing language.

> **Before:** Great question! You're absolutely right that this is complex. That's an excellent point about the economic factors.
>
> **After:** The economic factors you mentioned are relevant here.

---

## Filler & Hedging

### 22. Filler phrases

Common substitutions:

| Filler | Replacement |
|---|---|
| In order to | To |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| It is important to note that | _(cut entirely)_ |

### 23. Excessive hedging

Over-qualifying statements with stacked hedges.

> **Before:** It could potentially possibly be argued that the policy might have some effect on outcomes.
>
> **After:** The policy may affect outcomes.

### 24. Generic positive conclusions

Vague upbeat endings with no specific content.

**Watch for:** the future looks bright, exciting times lie ahead, journey toward excellence, step in the right direction, continues to thrive

> **Before:** The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.
>
> **After:** The company plans to open two more locations next year.
