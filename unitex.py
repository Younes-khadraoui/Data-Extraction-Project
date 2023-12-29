'''
"Alphabet.txt" est un fichier qui spécifie l'alphabet utilisé dans le corpus médical
il définit les caractères considérés comme des lettres, de la ponctuation, etc
ce fichier est utilisé pendant le processus de normalisation pour découper le texte en tokens
exemple1 : si le corpus ne doit considerer que les lettres de l'alphabet latin, le fichier Alphabet.txt pourrait rassembler a ceci:
 A B C D E F I G K L M N O P Q R S T U V W X Y Z 
 a b c d e f i g k l m n o p q r s t u v w x y z
exemple2 : si on a des chiffres et des symboles spéciaux sont inclus dans l'alphabet
cela peut être considéré comme un échec si ces caractères ne sont pas pertinents pour le corpus
l'inclusion d'éléments inappropriés dans l'alphabet peut conduire à des résultats incorrects ou indésirables lors de l'analyse du corpus.
'''

import os 
os.mkdir("corpus-medical_snt")
os.system("UnitexToolLogger Normalize corpus-medical.txt -r Norm.txt")
os.system("UnitexToolLogger Tokenize corpus-medical.snt -a Alphabet.txt")
os.system("UnitexToolLogger Compress subst.dic")
os.system("UnitexToolLogger Dico -t corpus-medical.snt -a Alphabet.txt subst.bin Delaf.bin")
os.system("UnitexToolLogger Grf2Fst2 posologie.grf")
os.system("UnitexToolLogger Locate -t corpus-medical.snt posologie.fst2 -a Alphabet.txt -L -I --all")
os.system("UnitexToolLogger Concord corpus-medical_snt/concord.ind -f \"Courier new\" -s 12")
