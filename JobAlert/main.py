import time

import scrap_indeed
import gpt
from gpt import GptAgent

balise = "<<>>"

reformator = GptAgent("Reformator", "", "reformator.txt")
def reformatJobDescription(jb):
    return reformator.tell(jb)

classificator = GptAgent("Reformator", "", ["classificator.txt","profile.txt"])
def classifyJobDescription(jb):
    tt = classificator.tell(jb)
    parts = tt.split('@')
    return (tt,int(parts[1]))

def loadJobs(fileName):
    # Ouvrir le fichier en mode lecture
    with open(fileName, 'r', encoding='utf-8') as file:
        # Lire tout le contenu du fichier
        content = file.read()

    # Séparer le contenu en utilisant la balise définie
    string_list = content.split(balise)

    return string_list

job_descriptions = []
def concatJobDescriptions(jdl):
    txt = ""
    for jb in jdl:
        txt += jb + "\n>>>\n"
    return txt

mode = 2

if mode == 0:
    job_descriptions = scrap_indeed.scrapFromKeywork("analyse d'images",2)

    with open('testext.txt', 'w', encoding='utf-8') as file:
        for ji in job_descriptions:
            file.write(ji)
            file.write("\n" + balise + "\n")
else:
    job_descriptions = loadJobs("testext.txt")

reformated_job_descriptions = []
if mode < 2 :
    print("Processing " + str(len(job_descriptions)) + " jobs ! ")
    reformated_job_descriptions =  []
    for i in range(len(job_descriptions)):
        reformated_job_descriptions.append(reformatJobDescription(job_descriptions[i]))
        print("  >> Reformated offer " + str(i))

    with open('reformated_concat_job_descriptions.txt', 'w', encoding='utf-8') as file:
        for rjb in reformated_job_descriptions:
            file.write(rjb + "\n"+balise+"\n")
else:
    reformated_job_descriptions = loadJobs("reformated_concat_job_descriptions.txt")

print("Ranking " + str(len(reformated_job_descriptions)) + " jobs")
for i in range(len(reformated_job_descriptions)):
    note = classifyJobDescription(reformated_job_descriptions[i])
    print("Job N° " + str(i) + " graded " + str(note[1]) + " :\n   " + note[0])
