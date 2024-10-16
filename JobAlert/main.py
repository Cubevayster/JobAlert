import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# URL de la page web
url = 'https://fr.indeed.com/jobs?q=analyse+d%27image&l=Lyon+%2869%29&from=searchOnDesktopSerp&vjk=c2b6128c049d8b48'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)  # Ouvre le navigateur et charge la page

# Optionnel : Attendre quelques secondes pour que la page charge
time.sleep(5)

# Récupérer le code HTML de la page
page_source = driver.page_source
# Fermer le navigateur une fois le scraping terminé
driver.quit()

# Parse le contenu HTML
soup = BeautifulSoup(page_source, 'html.parser')

with open('testext.txt', 'w', encoding='utf-8') as file:
    # Parcourir les titres et les enregistrer dans le fichier
    file.write(soup.get_text())

# Trouver toutes les balises contenant l'identifiant unique 'vjk'
# En général, les identifiants vjk se trouvent dans des balises <a> avec des attributs data-jk ou similaires
job_elements = soup.find_all('a', {'data-jk': True})

# Extraire tous les identifiants 'vjk'
vjk_ids = [job['data-jk'] for job in job_elements]

# Afficher les identifiants extraits
for vjk_id in vjk_ids:
    print(vjk_id)