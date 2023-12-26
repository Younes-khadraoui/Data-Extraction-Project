import sys
import re
import locale
from functools import cmp_to_key

locale.setlocale(locale.LC_ALL, "fr_FR")

def list_to_string(lst):
    string = ''
    for item in lst:
        string = string + item
    return string

if len(sys.argv) == 2:
    path = sys.argv[1]
else:  # default location
    path = 'corpus-medical.txt'

corpus = open(path, 'r', encoding='utf-8').read()

subst_corpus = re.findall(r'([A-Z][A-Za-z]{4,})\s[:,]?\s?(\d*[,.]\d+|\d+|½)\s?(g|mg|µg|mcg|ml|µl|ui|iu|ml|mol|mmol|cp|amp|flacon|G|MG|ΜG|MCG|ML|ΜL|UI|IU|ML|MOL|MMOL|CP|AMP)[\s,./:]', corpus)

new_subst = []

for item in subst_corpus:
    new_subst.append(item[0].lower() + ',.N+subst\n')

subst = open('subst.dic', 'r', encoding='utf-16le').readlines()
subst[0] = subst[0][1:]  # remove BOM for sorting (will add it back during writing)

new_subst_sorted = list(set(new_subst))
new_subst_sorted.sort()

# difference between corpus and subst.dic
diff = [item for item in new_subst_sorted if item not in subst]

subst = subst + new_subst  # add new substances
subst = list(set(subst))
# Sort according to the French language
subst = sorted(set(new_subst_sorted).union(set(subst)), key=cmp_to_key(locale.strcoll))

subst = list_to_string(subst)
open('subst.dic', 'w', encoding='utf-16le').write('\ufeff' + subst)

print('subst.dic was modified.')

new_subst = list_to_string(new_subst)
open('subst_corpus.dic', 'w', encoding='utf-16le').write('\ufeff' + new_subst)

print('subst_corpus.dic is created.')

# fill info2.txt
info2 = open('info2.txt', 'w')
total_count = 0
data = {}
for item in sorted(new_subst_sorted, key=cmp_to_key(locale.strcoll)):
    first_letter = item[0].upper()

    if first_letter == 'É':
        first_letter = 'E'

    if first_letter in data:
        data[first_letter] += 1
    else:
        data[first_letter] = 1
    total_count += 1

for letter in data.keys():
    info2.write("Number of entities starting with " + letter + " = " + str(data[letter]) + "\n")

info2.write("----------------------------\n")
info2.write("Total number of entities = " + str(total_count))  # save the total number of entities
info2.close()

print('info2.txt is created.')

# fill info3.txt
info3 = open('info3.txt', 'w')
total_count = 0
data = {}
for item in sorted(diff, key=cmp_to_key(locale.strcoll)):
    first_letter = item[0].upper()

    if first_letter == 'É':
        first_letter = 'E'

    if first_letter in data:
        data[first_letter] += 1
    else:
        data[first_letter] = 1
    total_count += 1

for letter in data.keys():
    info3.write("Number of entities starting with " + letter + " = " + str(data[letter]) + "\n")

info3.write("----------------------------\n")
info3.write("Total number of entities = " + str(total_count))  # save the total number of entities
info3.close()

print('info3.txt is created.')
