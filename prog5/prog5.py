import requests
from bs4 import BeautifulSoup
import json
import argparse 
parser = argparse.ArgumentParser(description='program 5')
parser.add_argument('plik',help='plik')
args=parser.parse_args()
res = requests.get('https://2e.aonprd.com/SpellLists.aspx?Tradition=1')
#print(res.status_code)
#print(res.headers)
#print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')

main_div = soup.find('div',class_='main')

#names = main_div.find_all('u')
#for name in names:
#     print(name.text.strip())
#     print('------------------')

#names = []
#contacts = []
spells=[]
raw_data = main_div.select('h2,u')
for data in raw_data:
   # print(data.name)
   # print(data.text.strip())
   # print('------------------')
    
    if data.name == 'h2':
        spells.append("*********************************************")
        spells.append(data.text.strip())
        spells.append("----------------------------------------------")
 #       names.append(data.text.strip())
    else:
        spells.append(data.text.strip())
  #      contacts.append(data.text.strip())

#assert len(names) == len(contacts)

#print(names)
#print(contacts)

#employees = list(zip(names, contacts))
#print(employees)

with open(args.plik, 'w') as f:
    json.dump(spells, f, indent=4)