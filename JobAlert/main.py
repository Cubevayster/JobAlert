import time

from Tools.scripts.abitype import classify

import scrap_indeed
import gpt
from gpt import GptAgent
from scrap_indeed import job_description_class
import os
from datetime import date, datetime, timedelta

# Obtenir la date du jour
today = date.today()
folder_name = today.strftime("%Y-%m-%d")

existing_folders = [
        d for d in os.listdir()
        if os.path.isdir(d) and d.startswith("20")  # Vérifie un format de date AAAA-MM-JJ
    ]
print(str(len(existing_folders)) + " previous searches")
date_folders = sorted(
        [datetime.strptime(d, "%Y-%m-%d").date() for d in existing_folders if len(d) == 10]
    )
previous_folder = None
for folder_date in reversed(date_folders):
    if folder_date <= today:
        previous_folder = folder_date.strftime("%Y-%m-%d")
        break

balise = "<<>>"
balise_title = "++++"

filtered_raw_job_descriptions = {}
prefiltor = GptAgent("Prefiltor","",["prompts/prefiltor.txt","user/profile.txt"])
prefiltor_title = GptAgent("PrefiltorTitle","",["prompts/prefiltortitle.txt","user/profile.txt"])
def filterJobDescription(jb):
    tt = prefiltor.tell(jb)
    parts = tt.split('@')
    prefiltor.removeLastContext()
    prefiltor.removeLastContext()
    return (tt,int(parts[1]))

def filterJobTitle(jb):
    tt = prefiltor_title.tell(jb)
    parts = tt.split('@')
    prefiltor_title.removeLastContext()
    prefiltor_title.removeLastContext()
    return (tt,int(parts[1]))

reformated_job_descriptions = {}
reformator = GptAgent("Reformator", "", "prompts/reformator.txt")
def reformatJobDescription(jb):
    tt = reformator.tell(jb)
    reformator.removeLastContext()
    reformator.removeLastContext()
    return tt

classified_job_descriptions = {}
classificator = GptAgent("Classificator", "", ["prompts/classificator.txt","user/profile.txt"])
def classifyJobDescription(jb):
    tt = classificator.tell(jb)
    parts = tt.split('@')
    classificator.removeLastContext()
    classificator.removeLastContext()
    return (tt,int(parts[1]))

def loadJobs(fileName):
    # Ouvrir le fichier en mode lecture
    with open(fileName, 'r', encoding='utf-8') as file:
        # Lire tout le contenu du fichier
        content = file.read()

    # Séparer le contenu en utilisant la balise définie
    string_list = content.split(balise)
    string_list = string_list[0:len(string_list)-1]

    dictio = {}
    for jb in string_list:
        jbsplit = jb.split(balise_title)
        dictio[jbsplit[0]] = jbsplit[1]

    return dictio

all_raw_job_descriptions = {}
def concatJobDescriptions(jdl):
    txt = ""
    for jb in jdl:
        txt += jb + "\n>>>\n"
    return txt




mode = input("Appuyez sur A pour lancer une nouvelle recherche, et sur B pour récupérer la recherche précédente : ")
mode = 0 if (mode == "A" or mode == "a") else 1


if mode < 1:
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    scrap_result = scrap_indeed.scrapFromKeywork("computer vision",2)
    all_raw_job_descriptions = dict(scrap_result)

    with open(folder_name + "/all_raw_job_descriptions.txt", 'w', encoding='utf-8') as file:
        tuples = list(all_raw_job_descriptions.items())
        for i in range(len(tuples)):
            file.write(tuples[0] + balise_title + tuples[1])
            file.write("\n" + balise + "\n")
else:
    if previous_folder == None:
        print("Error : No previous search")
        exit()
    else:
        folder_name = previous_folder
        all_raw_job_descriptions = loadJobs(folder_name + "/all_raw_job_descriptions.txt")

input("Appuyez sur ENTRER pour continuer...")

if mode < 2:
    liste = list(all_raw_job_descriptions.items())
    print("Pre-Filtering" + str(len(liste)) + " jobs ! ")

    for i in range(len(liste)):
        filt = filterJobTitle(liste[i][0])
        if filt[1] > 0:
            filt = filterJobDescription(liste[i][1])
            if filt[1] > 0:
                filtered_raw_job_descriptions[liste[0]] = liste[1]
                print("Job N° " + str(i) + " ketp ! :\n   " + filt[0])
            else:
                print("Job N° " + str(i) + " discarded. :\n   " + filt[0])
        else:
            print("Job N° " + str(i) + " discarded. :\n   " + filt[0])

    with open(folder_name + "/filtered_raw_job_descriptions.txt", 'w', encoding='utf-8') as file:
        tuples = list(filtered_raw_job_descriptions.items())
        for jb in tuples:
            file.write(jb+ " \n" + balise + "\n")
else:
    filtered_raw_job_descriptions = loadJobs(folder_name + "/filtered_raw_job_descriptions.txt")

input("Appuyez sur ENTRER pour continuer...")

if mode < 3 :
    liste = list(filtered_raw_job_descriptions.items())
    print("Processing " + str(len(liste)) + " jobs ! ")

    for i in range(len(liste)):
        reformated_job_descriptions[liste[i][0]] = reformatJobDescription(liste[i][1])
        print("  >> Reformated offer " + str(i))

    with open(folder_name + "/reformated_concat_job_descriptions.txt", 'w', encoding='utf-8') as file:
        tuples = list(reformated_job_descriptions.items())
        for rjb in tuples:
            file.write(rjb + "\n"+balise+"\n")
else:
    reformated_job_descriptions = loadJobs(folder_name + "/reformated_concat_job_descriptions.txt")

input("Appuyez sur ENTRER pour continuer...")

if mode < 4:
    liste = list(reformated_job_descriptions.items())
    print("Ranking " + str(len(liste)) + " jobs")

    notes = []
    classes = []
    for i in range(len(liste)):
        note = classifyJobDescription(liste[i][0])
        print("Job N° " + str(i) + " graded " + str(note[1]) + " :\n   " + note[0])
        notes.append(note[1])

    classes = [s for _, s in sorted(zip(notes, liste))]
    classes = classes[::-1]

    classified_job_descriptions = dict(classes)

    with open(folder_name + "/classified_job_descriptions.txt", 'w', encoding='utf-8') as file:
        tuples = list(classified_job_descriptions.items())
        for jb in tuples:
            file.write(jb+ " \n" + balise + "\n")
else:
    classified_job_descriptions = loadJobs(folder_name + "/classified_job_descriptions.txt")