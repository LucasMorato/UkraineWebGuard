import subprocess as sp
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import sys
import os
import re


#abre o arquivo de email lê o arquivo, salva em uma lista e fecha
with open("emails.txt", "r") as mails:
     xMails = mails.read() #var
mails.close()

#abre o arquivo vulns.txt, salva tudo em um string e fecha
with open("vulns.txt", "r") as vulns:
    xVulns = vulns.read() #var
vulns.close()

#pega a primeira palavra depois do http ou https:// (nome do site)
# AQUI USANDO seperj
wordSite = "spleen"

#aqui testando pegar a primeira palavra mas só está pegando as urls inteiras do vulns.txt
#for line in xVulns:
 #   urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', xVulns)

#aqui tentando também https://stackoverflow.com/questions/44021846/extract-domain-name-from-url-in-python


#se a palavra existir na lista de emails e na lista vulns (spleen por exemplo)
if wordSite in xMails and xVulns:
    # pega o item da lista(email) da lista e envia o email
    print("Enviando email para o host | Seu website pode estar vulnerável, nos contate imediatamente!")
else:
    # vai para o próximo
    print("Escaneando verificando outros emails")
