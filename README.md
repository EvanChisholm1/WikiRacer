# Wiki Racer

Wiki Racer is an AI system that aims to complete wikipedia speedruns at a super human level.

## how it works:

1. gets the wikipedia page of the start and target
2. embeds both of their titles
3. from the current url embed all the titles of the available urls
4. move to the url with the highest semantic similarity with the target
5. repeat steps 3 - 5 until you arrive at the target

Currently goes from Dune (novel) to Barbie (film) in just 5 moves.

## Weaknesses

-   Crappy embedding model, not smart enough
-   not always enough information in the embeddings.
-   sometimes things are very tangentally related.
-   struggles with names of people

## ideas to improve

-   use gpt4 or some sort of llm to try to plan a route
-   use an llm to generate more information on each topic such that the embeddings could have more information compressed in them?
