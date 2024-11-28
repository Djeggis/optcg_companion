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
#################################################################################################

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

adblockfile = "uBlock0_1.61.2.firefox.signed.xpi"

driver = webdriver.Firefox()

driver.install_addon(adblockfile, temporary=True)

time.sleep(5)

driver.get("https://onepiecetopdecks.com/deck-list/japan-op-09-the-new-emperor-decks/")

driver.maximize_window()


# Define a custom condition to check if the element is in the viewport
def is_element_in_viewport(driver, element):
    # Get the element's location and size
    location = element.location
    size = element.size
    
    # Check if the element is in the visible part of the viewport
    return (location['y'] >= 0 and location['y'] + size['height'] <= driver.execute_script("return window.innerHeight"))

# Scroll and wait until the button is in the viewport
def scroll_until_element_in_view(driver, element):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the page to load (you may adjust the time based on your page load speed)
        time.sleep(2)
        
        # Check if the element is now in the viewport
        if is_element_in_viewport(driver, element):
            break
        
        # If the page height hasn't changed, we've reached the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, '.dt-paging-button.next')
        except Exception as e:
            break

# finds all the links on page

final_page = -1
filtered_links = []

# Call the function to scroll until the button is in the viewport
next_btn = driver.find_element(By.CSS_SELECTOR, '.dt-paging-button.next')

while(final_page<0):
    table_trs = driver.find_elements(By.TAG_NAME, 'a')

    # filter the deck list links out
    for x in table_trs:
        if "deckgen" in x.get_attribute('href'):
            filtered_links.append(x.get_attribute('href'))

    try:
        scroll_until_element_in_view(driver, next_btn)
        next_btn.click()
    except Exception as e:
        final_page = 1
        break

print(filtered_links)


unfiltered_texts = []
for link in filtered_links:
    
    # change web address to full_link
    driver.get(link)

    #find the tabletop textarea and grab
    unfiltered_texts.append(driver.find_element(By.TAG_NAME, 'textarea').text)

print(unfiltered_texts)

# go through deck list links and find actual deck list and store
# grab from tabletop simulator data (already nicely formatted), will further format later

driver.quit()

#################################################################################################

# transfer into csv
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for textarea in unfiltered_texts:

        row = list(map(str.strip, textarea[1:-1].split(",")))

        writer.writerow(row)

print("Data written to 'output.csv' successfully.")