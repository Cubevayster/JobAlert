from ctypes import PyDLL

import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

job_description_class = "fastviewjob jobsearch-ViewJobLayout--embedded css-1s5gqtr eu4oa1w0 hydrated"

knownVJK = []

def loadKnownVJK(fileName):
    try:
        with open(fileName, 'r', encoding='utf-8') as file:
            # Lire tout le contenu du fichier
            content = file.read()
        string_list = content.splitlines()
        return string_list[0:len(string_list) - 1]
    except:
        return []

def getSoupFromURL(driver,url):
    print("  > Opening URL...")
    driver.get(url)
    try:
        print("  > Waiting for the page to load...")
        # Attendre qu'un élément spécifique de la page soit présent avant de continuer
        # Ici, nous attendons qu'un élément avec une balise <body> soit chargé (par exemple)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print(f"  > Error during page load: {e}")
        return []
    time.sleep(0.5)
    # Récupérer le code HTML de la page
    page_source = driver.page_source
    # Parse le contenu HTML
    print("  > Parsing HTML...")
    return BeautifulSoup(page_source, 'html.parser')

def scrapFromKeywork(keyword,pageCount):
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver = Driver(uc=True, headless=True)

    # URL de la page web
    url = 'https://fr.indeed.com/jobs?q='+keyword+'&l=Lyon+%2869%29&filter=0&sort=date&from=searchOnDesktopSerp&start'
    print("Using URL=" + url)

    vjk_ids = []
    knownVJK = loadKnownVJK("VJK.txt")

    for i in range(pageCount):
        ji = i * 10
        print("Scarping url data from page " + str(i) + "...")
        soup = getSoupFromURL(driver,url+"="+str(ji))
        print("Done.")

        # Trouver toutes les balises contenant l'identifiant unique 'vjk'
        # En général, les identifiants vjk se trouvent dans des balises <a> avec des attributs data-jk ou similaires
        print("Finding all VJKs...")
        job_elements = soup.find_all('a', {'data-jk': True})

        # Extraire tous les identifiants 'vjk'
        found_vjks = [job['data-jk'] for job in job_elements]
        for fvjk in found_vjks:
            if vjk_ids.count(fvjk) > 0:
                print("Reached end of pages")
                break
            if knownVJK.count(fvjk) :
                continue
            vjk_ids.append(fvjk)
            with open('VJK.txt', 'a', encoding='utf-8') as file:
                file.write(fvjk + "\n")

    job_descriptions = []
    job_titles = []

    for vkj_id in vjk_ids:
        url_1 = url + "&vjk=" + vkj_id
        print("Scraping job description from vkj '" + vkj_id + "'...")
        soup = getSoupFromURL(driver,url_1)
        print("Done.")
        jobdescription_div = soup.find('div', class_=job_description_class)
        if jobdescription_div is None:
            print("None job description_div for jvk " + vkj_id +  " !!!")
        else:
            job_titles.append(jobdescription_div.find("span").get_text())
            job_descriptions.append(jobdescription_div.get_text())

    # Fermer le navigateur une fois le scraping terminé
    driver.quit()

    return (job_titles,job_descriptions)