import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

import scrap_indeed

balise = "<<puechpuechpuechnourah!>>"

job_descriptions = scrap_indeed.scrapFromKeywork("analyse d'images",2)

with open('testext.txt', 'w', encoding='utf-8') as file:
    for ji in job_descriptions:
        file.write(ji)
        file.write("\n" + balise + "\n")