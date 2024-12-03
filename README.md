# optcg_companion
NLP Project - Companion for the One Piece Card Game
Demo Video: https://youtu.be/KQIz5-BInOU
---
Currently includes functionality for:
- Decklist Scraping
  - Currently supports taking posted lists from (https://onepiecetopdecks.com/)
- Deck Construction Assistance
  - Users can either request deck ideas based off a specific leader or can instead submit their own deck lists to get helpful suggest(s based off of common card type ratios and other successful decks based off of the leader
  - Users can also request to see useful statistics for cards in the deck such as likelihood to see a card on curve based on ratios or average amount of bricks in hand
  - Data is taken from winning deck lists aggregated by other sites (https://onepiece.limitlesstcg.com/), (https://egmanevents.com/one-piece), (https://onepiecetopdecks.com/)

<!-- end of the list -->

Working on the implementation for:
- Comprehensive Rules Assistance
  - Users can request either a generic rules overview (for beginners) or specific rules regarding specific cards in which the companion will process the request and search through the current comprehensive rules for relevant results and then present the most useful ones
  - Data is taken from the official comprehensive rules (https://en.onepiece-cardgame.com/rules/)
---
Methods:
- Decklist Scraping is accomplished through Python's Selenium package, extracting the data from the html code
- Deck Construction Assistance is accomplished through a Discord Bot frontend supported by OpenAI

<!-- end of the list -->

Future goals:
- Implementation with the OPTCG Sim
  - This will help with both card data visualization as well as card classification, as integrating it into OPTCG Sim will provide the necessary tags and databases
