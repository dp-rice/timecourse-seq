#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-23:59
#SBATCH -p general
#SBATCH --mem=1000

PLANFILE=$1
PREFIX=$2
BASESTOMATCH=8

sed 1d $PLANFILE | \
while read l; do
    a=( $l )
    pop=${a[4]}
    gen=${a[5]}
    for i in 1 2; do
        python src/trim_adaptor_seqs.py \
            ${PREFIX}${pop}-${gen}.R${i} \
            $BASESTOMATCH
    done
done
