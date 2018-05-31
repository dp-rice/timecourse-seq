#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 4:00:00
#SBATCH -p serial_requeue
#SBATCH --mem=1000
#SBATCH -o log/parse_vcf_%A.out
#SBATCH -e log/parse_vcf_%A.err

python src/parse_sort_and_combine_vcfs.py $1 $2 $3 > $4
