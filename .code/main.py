# Module 1: Deck Construction
# 1. Scrape data from tournament reporting sites
# 2. Categorize card categories
# 3. Deck list input
# 4. Calculate deck statistics
# 5. NLP: Analyze differences between input deck and winning decks and give suggestions based off of list
#    -Any immediate suggestions (specific card is missing that exists in majority of winning decks)
#    -Recommend ratio changes (winning decks have certain ratios of card types)
#    -Ask for anything specific the user wants to analyze
# 
# Modules 2: Rules Assistance
# 1. Search for relevant results for specific comprehensive rules (input card name or specific card)
# 2. NLP: Multi-step dialog for basic rules explanation (targeted towards beginners)


# Deck data scraping
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("https://onepiecetopdecks.com/deck-list/japan-op-09-the-new-emperor-decks/")

# finds all the links on page
### NEED TO IMPLEMENT CHANGING PAGE ON TABLE ###
table_trs = driver.find_elements(By.TAG_NAME, 'a')
filtered_links = []

# filter the deck list links out
for x in table_trs:
    if "deckgen" in x.get_attribute('href'):
        filtered_links.append(x.get_attribute('href'))

#print(filtered_links)


for link in filtered_links:
    link.click()

    #find the tabletop textarea and grab
    unfiltered_text = ...

    #filter the text looping through

# go through deck list links and find actual deck list and store
# grab from tabletop simulator data (already nicely formatted), will further format later

driver.quit()

