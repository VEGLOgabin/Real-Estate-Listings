import asyncio
from playwright.sync_api import sync_playwright

# from playwright.async_api import async_playwright

import streamlit as st
import time
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import logging


URL = "https://www.zillow.com/homes/usa_rb/"

def scrape_page(page, page_number):
    # Locate all real estate articles
    realestates = page.locator("article").all()
    links = []
    estates = []
    
    for item in realestates:
        estate = item.locator("a.klMkvj")
        estates.append(estate)
        link = estate.get_attribute("href")
        links.append(link)
   
    
    time.sleep(2)
    data = [links, page]
    return data



def scrape_all_pages():
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        
        
        page_number = 1
        
        while True:
            
            print(page_number)
            current_data_and_page = scrape_page(page, page_number)
            current_data = current_data_and_page[0]
            page = current_data_and_page[1]
            # data.append(current_data)
            for item in current_data:
                data.append([page_number, item]) 
            
            # Check if there is a next page
            next_page_button = page.locator("li.WDDJJ")
            if next_page_button.count() == 0:
                break
            
            next_page_button1 = page.locator("li.WDDJJ:last-child a")
            aria_disabled = next_page_button1.get_attribute("aria-disabled")
            if aria_disabled == "true":
                break
            
            page.locator("li.WDDJJ:last-child a").click()
            page_number +=1
            time.sleep(10)  # Wait for the page to load
        
        browser.close()
    return data
        
        
def save_to_csv(data, filename="scraped_data.csv"):
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["Page Number", "Product Links"])
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)

# Run the scraping process
if __name__ == "__main__":
    try:
        data = scrape_all_pages()
        # HEADERS = ["Page NUMBER", "PRODUCT LINKS"]
        save_to_csv(data, filename="zillow_scraped_data.csv")  # Save data to CSV
        # print(data)
    except KeyboardInterrupt:
        print("Process interrupted")
