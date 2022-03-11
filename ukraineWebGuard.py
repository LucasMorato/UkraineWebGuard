# ------------------------------------------------
# Important: THIS SCRIPT SHOULD BE USED WITH CAUTION. OVERLOADING GOOGLE SERVERS MAY CAUSE TEMPORARY BLOCKING OF YOUR IP ADDRESS
# You must have installed Wpscan By WPScan Team https://github.com/wpscanteam/wpscan before running the script
# ------------------------------------------------
import subprocess as sp
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from googlesearch import search
import urllib.parse
import sys
import os

print('\n')
print('\n')
print('\n')
print("  _    _ _              _             __          __  _      _____                     _ ")
print(" | |  | | |            (_)            \ \        / / | |    / ____|                   | |")
print(" | |  | | | ___ __ __ _ _ _ __   ___   \ \  /\  / /__| |__ | |  __ _   _  __ _ _ __ __| |")
print(" | |  | | |/ / '__/ _` | | '_ \ / _ \   \ \/  \/ / _ \ '_ \| | |_ | | | |/ _` | '__/ _` |")
print(" | |__| |   <| | | (_| | | | | |  __/    \  /\  /  __/ |_) | |__| | |_| | (_| | | | (_| |")
print("  \____/|_|\_\_|  \__,_|_|_| |_|\___|     \/  \/ \___|_.__/ \_____|\__,_|\__,_|_|  \__,_|")
print('\n')
print('\n')
print('\n')
print('by Lucas F. Morato')
print('Version 1.0')
print('\n')

token = "ayewkTKpNefcJMhu7oPTswvB1KpWIGoDQgyH8ofn5sw" ############# change here | you can get a plan free here: https://wpscan.com/pricing

# stores the search for ukraine websites 
keyword = 'site:"au" inurl:wp-content/ intext:ukraine' # you can chance intext parameter to get another websites and (au)  to (com.au)

# search for ukraine addresses and send to a tmp file
try:
  print("Searching Ukraine Url's...")
  sys.stdout = open("urls.tmp", "w")
  for urls in search(keyword, num=3, stop=3, pause=3): # change "num=" to search more than 5 websites | IMPORTANT: DO NOT DECREASE THE "PAUSE TIME" TO LESS THAN 4
    print(urls)

  sys.stdout.close()
except ImportError:
  print('Google Database connection error!')

# filters the website address (remove /wp-content... etc)
new_urls = []

with open("urls.tmp", "r") as urls_file:
    old_urls = urls_file.readlines()

for line in old_urls:
    url_parts = urllib.parse.urlparse(line)
    proc_url = "{uri.scheme}://{uri.netloc}/\n".format(uri=url_parts)
    new_urls.append(proc_url)

with open("urls.tmp", "w") as urls_file:
    urls_file.writelines(new_urls)

# remove duplicated urls (for dont make scan twice) and save urls in 
a_file = open("urls.tmp", "r")
writeFile = open("updatedUrls.txt", "w")
tmp = set()
for txtLine in a_file:
    if txtLine not in tmp:
        writeFile.write(txtLine)
        tmp.add(txtLine)
a_file.close()
writeFile.close()
os.remove("urls.tmp")

# run wpscan and store only vulnerabilities (save vulnerabilities in vulns.txt)
with open("updatedUrls.txt", "r") as h:
  for line in h:
    wpsfile = line.strip()
    with open("vulns.txt", "w") as external_file:
        vulns_output = sp.getoutput(f"wpscan --url {wpsfile} --api-token {token} --random-user-agent --ignore-main-redirect | grep -i '[!]\| url:\|started\|Aborted' | grep -v 'Effective\|style\|WARNING\|The version'")
        print(vulns_output, file=external_file)
        external_file.close()
    

#save emails in emails.txt from captured sites
with open("updatedUrls.txt", "r") as smails:

    original_url = smails.read().splitlines()

unscraped = deque(original_url)

scraped = set()
emails = set()

while len(unscraped):

    url = unscraped.popleft()
    scraped.add(url)

    parts = urlsplit(url)

    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
        path = url[:url.rfind('/') + 1]
    else:
        path = url

    
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue

    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
    emails.update(new_emails)

    soup = BeautifulSoup(response.text, 'lxml')

    for anchor in soup.find_all("a"):
        if "href" in anchor.attrs:
            link = anchor.attrs["href"]
        else:
            link = ''

            if link.startswith('/'):
                link = base_url + link

            elif not link.startswith('http'):
                link = path + link

            if not link.endswith(".gz"):
                if not link in unscraped and not link in scraped:
                    unscraped.append(link)

df = pd.DataFrame(emails, columns=None)
df.to_csv('emails.txt', index=False)
with open('emails.txt', 'r') as fin:
    data = fin.read().splitlines(True)
with open('emails.txt', 'w') as fout:
    fout.writelines(data[1:])

