import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

job_description_class = "fastviewjob jobsearch-ViewJobLayout--embedded css-1s5gqtr eu4oa1w0 hydrated"

def getSoupFromURL(url,delay=5):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("  > Opening URL...")
    driver.get(url)
    print("  > Loading URL...")
    time.sleep(delay)
    # Récupérer le code HTML de la page
    page_source = driver.page_source
    # Fermer le navigateur une fois le scraping terminé
    driver.quit()
    # Parse le contenu HTML
    print("  > Parsing HTML...")
    return BeautifulSoup(page_source, 'html.parser')

def scrapFromKeywork(keyword):
    # URL de la page web
    url = 'https://fr.indeed.com/jobs?q='+keyword+'&l=Lyon+%2869%29&from=searchOnDesktopSerp'
    print("Using URL=" + url)

    print("Scarping url data...")
    soup = getSoupFromURL(url)
    print("Done.")

    # Trouver toutes les balises contenant l'identifiant unique 'vjk'
    # En général, les identifiants vjk se trouvent dans des balises <a> avec des attributs data-jk ou similaires
    print("Finding all VJKs...")
    job_elements = soup.find_all('a', {'data-jk': True})
    # Extraire tous les identifiants 'vjk'
    vjk_ids = [job['data-jk'] for job in job_elements]

    job_descriptions = []

    for vkj_id in vjk_ids:
        url_1 = url + "&vjk=" + vkj_id
        print("Scraping job description from vkj '" + vkj_id + "'...")
        soup = getSoupFromURL(url_1)
        print("Done.")
        jobdescription_div = soup.find('div', class_=job_description_class)
        job_descriptions.append(jobdescription_div.get_text())

    return job_descriptions