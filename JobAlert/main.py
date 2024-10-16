import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

job_description_class = "fastviewjob jobsearch-ViewJobLayout--embedded css-1s5gqtr eu4oa1w0 hydrated"

def getSoupFromURL(url,delay=2):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(delay)
    # Récupérer le code HTML de la page
    page_source = driver.page_source
    # Fermer le navigateur une fois le scraping terminé
    driver.quit()
    # Parse le contenu HTML
    return BeautifulSoup(page_source, 'html.parser')

# URL de la page web
url = 'https://fr.indeed.com/jobs?q=analyse+d%27image&l=Lyon+%2869%29&from=searchOnDesktopSerp'

soup = getSoupFromURL(url)

# Trouver toutes les balises contenant l'identifiant unique 'vjk'
# En général, les identifiants vjk se trouvent dans des balises <a> avec des attributs data-jk ou similaires
job_elements = soup.find_all('a', {'data-jk': True})

# Extraire tous les identifiants 'vjk'
vjk_ids = [job['data-jk'] for job in job_elements]

# Afficher les identifiants extraits
for vjk_id in vjk_ids:
    print(vjk_id)

url_1 = url + "&vjk=" + vjk_ids[0]

soup = getSoupFromURL(url_1)

with open('testext.txt', 'w', encoding='utf-8') as file:
    # Parcourir les titres et les enregistrer dans le fichier
    jobdescription_div = soup.find('div', class_=job_description_class)
    file.write(jobdescription_div.get_text())