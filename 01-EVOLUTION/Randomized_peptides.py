import pandas as pd
from multiprocessing import Pool
import random
import os
from numpy import number

#CREATING FILE CONTAINING RANDOM PEPTIDES AND EVALUATING IT

#Input
output_file_name = "random_peptides_0to2000.csv"
Initial_peptide = 0
Number_aa = 29 #Desired peptides -1
Number_peptides = 2000

#Defyining functions

aminoacids = ['A', 'R', 'D', 'N', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

def random_mkers(number_amino, library_size):
    Library = []
    for i in range(library_size):
        Library.append(random.choice(aminoacids))
    for aa in range(number_amino):
        for e in range(len(Library)):
            Library[e] = Library[e] + random.choice(aminoacids)
    return Library

#Building and procesing library of random peptides

library_random_aa = random_mkers(Number_aa, Number_peptides)

ACP_library = open("library.csv", "w")

FASTA_names = []

for i in range(Number_peptides):
    FASTA_names.append(">" + str(int(Initial_peptide)+i))

for i in range(Number_peptides):
    ACP_library.write(FASTA_names[i] + "\n" + library_random_aa[i] + "\n")
