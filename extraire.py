import sys
import re
import urllib
import requests
from bs4 import BeautifulSoup as bs

# Function to check if the provided interval is valid (A-Z)
def checkInterval(interval):
   global start, end
   if re.match('[A-Z]-[A-Z]', interval) and interval[0] <= interval[2]:
       start = interval[0]
       end = interval[2]
   else:
       print('Invalid interval :(\n')
       exit()

# Function to check if the provided port number is valid (0-1023)
def checkPort(port):
   if int(port) < 0 or int(port) > 1023:
       print('Invalid port :(\n')
       exit()
   else:
       print('Valid port :D\n')
   return port

# Function to convert a list of BeautifulSoup elements to strings
def bs4ToString(data):
   return [str(item) for item in data]

# Function to convert a list of substances to a string formatted for a dictionary file
def listToString(list):
   return '\n'.join(item + ',.N+subst' for item in list)

# Main execution
if len(sys.argv) > 1:  # User provided arguments
   checkInterval(sys.argv[1].upper())
   port = checkPort(sys.argv[2])
else:  # Default values
   start = 'A'
   end = 'Z'
   port = '80'

file = 'vidal/vidal-Sommaires-Substances-'
path = 'http://localhost:' + port + '/' + file

with open('info1.txt', 'w') as info:  # Open info1.txt for writing
   meds = []
   nbrTotal = 0

   while start <= end:
       url = path + start + '.html'

       result = requests.get(url)
       html = bs(result.text.encode('latin1').decode(), 'html.parser')  # Handle special characters

       data = html.find_all('li')
       data = bs4ToString(data)  # Convert BS elements to strings

       nbr = 0
       for i in data:  # Filter for substance links
           if '<a href=\"Substance/' in i:
               med = re.findall('.htm">(.+)</a>', i)[0]  # Extract substance name
               meds.append(med)
               nbr += 1
           else:
               data.remove(i)  # Remove non-substance items

       nbrTotal += nbr
       info.write(f"Number of entities for {start} = {nbr}\n")  # Write entity count to file

       print(f"\nURL = \"{url}\": Process completed!\n")

       start = chr(ord(start) + 1)  # Increment letter

   info.write("----------------------------\n")
   info.write(f"Total number of entities = {nbrTotal}\n")  # Write total entity count

substances = listToString(meds)  # Convert substance list to dictionary string

with open('subst.dic', 'w', encoding='utf-16le') as f:
   f.write('\ufeff' + substances)

print('subst.dic is created.')