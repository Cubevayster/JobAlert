import openai
from colorama import Fore, Back, Style
import random
import math
import time

max_response_tokens = 10000


keyFile = open("key.txt", "r")
api_key = keyFile.read() #open key.txt


def gptPull(context):
    while True:
        try:
            chat = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=context,
                    temperature = 0.85,
                    max_tokens=max_response_tokens
                )
            choices = chat.choices
            reply = choices[0].message.content
            context.append({"role":"assistant","content":reply})
            return context

        except Exception as error:
            print(">>>>>>>>>  OPEN AI RATE LIMIT  <<<< WAITING 5 seconds",error)
            time.sleep(5)

    return context

def gptRequest(context,request):
    context.append(request)
    return gptPull(context)

def displayContext(context):
    color = Fore.CYAN
    if context["role"] == "user":
        color = Fore.YELLOW
    elif context["role"] == "system":
        color = Fore.GREEN
    print(color + "> " + context["content"])

def displayContexts(context,time,count=10000):
    for i in range(0,count):
        if (time + i) >= len(context):
            break
        displayContext(context[time + i])
        print("   ")
    print(Fore.WHITE)

def displayContextOf(agent,context):
    print("CONTEXT OF " + agent.name)
    displayContexts(context,1)

def makeRequest(text):
    return {"role":"user", "content":text}

def makeAnswer(text):
    return {"role":"assistant", "content":text}

def makePrePrompt(text):
    return {"role":"system", "content":text}

def contextToStr(context):
     text = ""
     for c in context:
          text += c["role"] + " : " + c["content"] + "\n\n"
     return text

class GptAgent:
    def __init__(self, name, color,prepromptPath,additionnal=""):
        self.name = name
        self.color = color
        if isinstance(prepromptPath,list):
            pp = ""
            for p in prepromptPath:
                pp += open(p, "r").read()
            self.preprompt = makePrePrompt(pp +"\n" + additionnal)
        else:
            self.preprompt = makePrePrompt(open(prepromptPath, "r").read() + "\n" + additionnal)
        self.context = [self.preprompt]
        self.lastTalked = 1
        
    def tellFromFile(self,file):
        return self.tell(open(file, "r").read())

    def tell(self,request):
        self.context = gptRequest(self.context,makeRequest(request))
        self.lastTalked = 1
        return self.context[len(self.context)-1]["content"]

    def talk(self):
        self.context = gptPull(self.context)
        self.lastTalked = 1
        return self.context[len(self.context)-1]["content"]

    def addContext(self,context,isUser = True):
        if isUser :
            self.context.append(makeRequest(context))
        else:
            self.context.append(makeAnswer(context))
    
    def addContextFromFile(self,file):
        return self.addContext(open("prompts/"+file, "r").read())

    def removeLastContext(self):
        self.context.pop()
        return

    def removeContext(self,id):
        self.context.pop(id)
        return

def check_openai_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Model.list()
    except openai.error.AuthenticationError as e:
        return False
    else:
        return True

print("Loading OPEN-AI code...")
if check_openai_api_key(api_key):
    print("  > Valid API KEY !")
else:
    print("  > API KEY not valid")
print("OPEN-AI successfully loaded !\n")