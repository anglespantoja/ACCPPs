import pandas as pd
from multiprocessing import Pool
import random
import os
from numpy import number

#First time evaluation of random peptides and generation of library of random peptides that can be evolved
output_file_name = "random_peptides_0to500.csv"

command = "python3 anticp2.py -i " + "library.csv " + " -o " + output_file_name + " -m 1 -d 2"
os.system(command)

df = pd.read_csv(output_file_name, skiprows=1)
df.to_csv(output_file_name, index=False)

#DIRECTED EVOLUTION PART

df = pd.read_csv(output_file_name, header=None)
df.columns = ["Identifier", "Sequence", "Prediction", "Score"]

Peptides_identifiers = []
Peptides_sequences = []
Peptides_scores = []

for i in range(len(df.index)):
    Peptides_identifiers.append((df.loc[i][0]).replace(">",""))    
    Peptides_sequences.append(df.loc[i][1])
    Peptides_scores.append(df.loc[i][3])

total_peptides_number = len(df.index)

# DEFYINING FUNCTIONS
# Randomization

aminoacids = ['A', 'R', 'D', 'N', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
aminoacid_number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

def randomize(Old_peptide):
    aminoacid_number_random = random.choice(aminoacid_number)
    new_aminoacid = random.choice(aminoacids)

    New_peptide = Old_peptide[0:aminoacid_number_random]
    New_peptide = str(New_peptide) + str(new_aminoacid)
    New_peptide = str(New_peptide) + str(Old_peptide[aminoacid_number_random+1:])

    return New_peptide

# Directed Devolution

def evolve(Identifier, Best_peptide, Best_score):
    Evolved = open("Evolved_list.csv", "a")
    Input_execution_name = str(Identifier) + ".fa"
    History_file_name = "Evolution_history_" + str(Identifier) + ".csv"
    Output_execution_name = str(Identifier) + "evolved.csv"
    execution_name = "python3 anticp2.py -i " + str(Input_execution_name) + " -o" + str(Output_execution_name) + " -m 1 -d 2"
    
    I = 0
    E = 0 # - Evolved
    
    History = open(History_file_name, "a")
    History.write(str(Identifier)+"E"+str(E)+"I"+str(I)+", " + str(Best_peptide)+", "+str(Best_score) + "\n") # Test_identifier is always the same - E=Evolved         
    History.close()

    New_score_percentage = 100
    Best_score_percentage = int(Best_score*100)
    Best_evol_count = 0
  
    while New_score_percentage > 0 and Best_evol_count < 100: #Best_evol_count is the number of iterations without visible improvement before the loop breaks
        if New_score_percentage >= Best_score_percentage:
            Best_evol_count += 1
            New_candidate = open(Input_execution_name, "w")
            New_peptide = randomize(Best_peptide)
            New_candidate.write(">" + str(Identifier)+"E"+str(E) + "\n")
            New_candidate.write(str(New_peptide)+ "\n")
            New_candidate.close()
            os.system(execution_name)

            df = pd.read_csv(Output_execution_name, header=None)
            df.drop(index=df.index[0], axis=0, inplace=True)
            df.columns = ["Identifier", "Sequence", "Prediction", "Score"]
            New_score = float(df.iloc[0]["Score"])
            New_score_percentage = int(New_score*100)
            I += 1
            
        elif Best_score_percentage > New_score_percentage:
            E += 1
            History = open(History_file_name, "a")
            History.write(str(Identifier)+"E"+str(E)+"I"+str(I)+", " + str(New_peptide)+", "+str(New_score) + "\n") # Test_identifier is always the same - E=Evolved         
            History.close()
            Best_score_percentage = New_score_percentage
            Best_peptide = New_peptide
            Best_evol_count = 0

    Recover = open(History_file_name, "r")
    Lines = Recover.readlines()
    Evolved.write(Lines[-1])
    Recover.close()
    
    os.system("rm " + str(Output_execution_name))
    os.system("rm " + str(Input_execution_name)) 


### Para lograr un mayor score, debo guardar la ultima variable que permitio una evolucion,
#  y si la variable no evoluciona mas despues de varias generaciones, matar el proceso o mutar
#  esta posicion aunque haya un decremento en el score momentaneamente

# MULTIPROCESSING

def evolve_peptide(peptide):
    Identifier, Best_peptide, Best_score = peptide
    evolve(Identifier, Best_peptide, Best_score)

with Pool(38) as p: #Change Pool number and adapt it to the number of processors available
    p.map(evolve_peptide, zip(Peptides_identifiers, Peptides_sequences, Peptides_scores))
    p.join()   

#Evolved = open("Evolved_list.csv", "a")

#if __name__ == '__main__':
#    procs = []

#    for i in range(total_peptides_number):
#        procs.append(multiprocessing.Process(target=evolve, args=[Peptides_identifiers[i], Peptides_sequences[i], Peptides_scores[i]]))
    
#    [proc.start() for proc in procs]


Evolved.close()
