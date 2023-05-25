import sys
from Scanner_PS import *
from Parser_PS import *

#assert len(sys.argv)==2, "Nalerzy podać ścieerzkę do pliku źródłowego"

#scierzka = str(sys.argv[1])
with open('kod.txt') as plik:
    input_string = plik.read()

scanner = Scanner(input_string)
print(scanner)

parser = Parser(scanner)
parser.start()
