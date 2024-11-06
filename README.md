# ACCPPs
Identification of Anticancer-Cell-Penetrating Peptide (ACCPP) candidates

- There are four folders, "01-EVOLUTION". "02-DEVOLUTION", "03-EVOLVED_RESULTS" and "04-DEVOLVED_RESULTS"
  - 01-EVOLUTION contains the pipeline to evolve the peptides for their anticancer feature. 
  - 02-DEVOLUTION contains a modified version of the 01-EVOLUTION script required to identify non-anticancer peptides (which may serve as negative controls). It also contains the output results after utilizing the algorithm to devolve anticancer peptides. 
  - 03-EVOLVED RESULTS contains the results of evolving anticancer peptides, their selection, results after being processed through the cell-penetrating module (MLCPP 2.0.), and final ACCPP selection.
  - 04-DEVOLVED RESULTS contains the results of evolving anticancer peptides, their selection, results after being processed through the cell-penetrating module (MLCPP 2.0.), and final ACCPP selection. 
 
* Both Evolution and Devolution algorithms rely on the AntiCP2 AI modules and scripts, developed by Prof. G. P. S. Raghava's group. "agrawal et al., (2020) AntiCP 2.0: an updated model for predicting anticancer peptides. Briefings in Bioinformatics, doi: 10.1093/bib/bbaa153"
* Cell-penetrating AI-module utilized was the MLCPP 2.0. developed by Prof. B. Manavalan and M. C. Patra. "Patra et al., (2022) MLCPP 2.0: An Updated Cell-penetrating Peptides and Their Uptake Efficiency Predictor. Journal of Molecular Biology, doi: 10.1101/2020.03.23.003780"

SCRIPTS DESCRIPTIONS
- submission.sh (found in 01-EVOLUTION and 02-DEVOLUTION) are the bash codes required to submit the jobs to the IBEX cluster.
- "Randomized_peptides.py" (found in 01-EVOLUTION and 02-DEVOLUTION) helps to build a library of randomized peptides. The user has to specify how many peptides are desired to be contained in the library. Also, it has to specify the length of the peptides (number of desired amino acids -1). It also has to specify the name of the output file. Since all peptides contain an identifier based on numbers. We ask the user to specify what will be the number of the first peptide in the list. The reason for this is that we are building several libraries, and we want each library to contain different identifiers. So if the first library contains 2000 peptides (numbered from 0 to 1999), we want the second library to contain peptides whose numeration starts from 2000.
- The Directed_Evolution.py script (found in 01-EVOLUTION), requires two main parameters to be modified: the output_file name (which at the end can be deleted), and the pool number in the multiprocessing section. This has to be adjusted based on the number of tasks that can be handled by the node available in the Ibex Cluster. This file algorithm calls the anticp2 AI module to score each of the input peptides (those found in the libraries created by "Randomized_peptides". Then insert random mutations to analyze if this one is increasing the score. If it is not increasing, then it tries another mutation, if any mutation increases the score, it is kept, and new mutations are tested to increase the score of the peptide. Sometimes, after many attempts of mutation, the score of the peptide won't increase, for that reason, we limit the attempt numbers to 100. If after 100 attempts, the peptide does not increase its score, a new peptide is attempted to be evolved. All evolved peptides are stored in a file called "Evolved_list.csv"
- "Directed_Devolution.py" is similar to "Directed_Evolution.py), but it is modified so peptides with lower anticancer scores can be identified.
- aac_extra_model, anticp2.py and dpc_extra_model (found in 01-EVOLUTION and 02-DEVOLUTION) are the scripts belonging to the AntiCP2 algorithm developed by agrawal etl.al. These are used to score the potential of peptides to be anticancer.
- ACCPP_env.text contains the packages required to execute either the evolution or devolution pipelines. These packages can be installed as an environment through conda. The environment has to be activated before running the pipelines. 


HOW TO USE THE ANTICANCER_EVOLUTION_PIPELINE (01-EVOLUTION)?
The file that must be executed primarly is the “Directed_Evolution.py”. This script communicates with the AI modules and the “Randomized_peptides.py” script. To execute this on the IBEX cluster, the “submission.sh” bash file can be used. 

DETAILS OF 03-EVOLVED_RESULTS
- All initial random peptides are shown in “01-Randomized_peptides.csv”
- During the evolution process, amino acid changes in peptide and resulting anticancer scores are recorded for each peptide (See “02-Evolution_history.zip”).
- After evolving all peptides, the final sequences with their scores are written on the “03 - Evolved_list.csv”
- Those that have a score higher than 0.9 were selected and placed on the “04 - Evolved_above_0.9.csv file”. This file contains 11926 candidates.
- Previous file is converted now into a fasta file (05 - Evolved_above_0.9.fa)
- For easy processing in the MLCPP 2.0 Cell-Penetrating predictor, the file was segmented into 12 smaller files (All segments are found in the Cell-Penetrating-Results directory). See “06 – Segmented_Evolved_above_0.9”.
- Segmented files are submitted to the MLCPP 2.0. module, and results are recovered in “07 – Cell-Penetrating-Results.zip”.
- Peptides with low CPP scores or low uptake efficiency are removed. Resulting list of ACCPP candidates is found in “08(02) – ACP_CPP_Compiled_Cleaned_for_Analysis”. A total of 337 ACCPP candidates are found.
- The top 10 candidates are selected based on a new ACCPP score, which is calculated as shown in the ACCPP score cells equation. - 
- 09 – OPTIMIZATION.zip. Amino acid sequences are converted into nucleotide sequences utilizing the GeneArt Optimization tool from ThermoFisher Scientific. Codons are optimized for Escherichia coli. 

DETAILS OF 04-DEVOLVED_RESULTS
These files follow the same logic as “03-EVOLVED_RESULTS”. 


USEFUL COMMANDS

- This command allows to create a list with only the desired numbers

ls Evolution_history_*.csv | grep -Eo '[0-9]+' > files.txt


- This command extracts numbers from the Evolved_list.csv file

cut -d',' -f1  Evolved_list.csv | grep -o '^[0-9]*' > Evolved_numbers.txt


- To extract missing numbers

awk 'BEGIN { for(i=8000; i<=11999; i++) arr[i] }
     { delete arr[$1] }
     END { for(num in arr) print num }' Evolved_numbers.txt > missing_numbers.txt


- Creating Evolution_history name files:

while IFS= read -r number; do echo "Evolution_history_$number.csv"; done < missing_numbers.txt > rm_evolved_history.txt


- Removing files from history

while IFS= read -r file; do rm "$file"; done < rm_evolved_history.txt



- Counting files in a directoryI ha

ls -1 | wc -l


- The following is for creating a list with the > from another .txt list

sed 's/^/>/' missing_numbers.txt > missing_numbers_formated.txt


- To extract desired rows from the library

awk -F',' 'FNR==NR{a[$0]; next} $1 in a{print $1; getline; print $0}' missing_numbers_formated.txt library.csv > new_library.csv


- The next one works great to convert generate fasta files for analysis on the CPP algorithm

iconv -f UTF-8 -t UTF-8//IGNORE Candidates_above_0.9.csv | awk -F',\040*' '{print ">", $1; print $2}' > Candidates.fa

iconv -f UTF-8 -t UTF-8//IGNORE Devolved_list.txt | awk -F',\040*' '{print ">", $1; print $2}' > Candidates.fa


