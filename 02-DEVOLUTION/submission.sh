#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=38
#SBATCH --partition=batch
#SBATCH -J MyJob
#SBATCH -o MyJob.%J.out
#SBATCH -e MyJob.%J.err
#SBATCH --time=14:00:00
#SBATCH --mem=5G
#SBATCH --constraint=intel

#run the application:
time python3 Directed_Evolution.py

