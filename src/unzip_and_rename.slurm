#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-23:59
#SBATCH -p general
#SBATCH --mem=1000

PLANFILE=$1
OLDPREFIX=$2
NEWPREFIX=$3

sed 1d $PLANFILE | \
while read l; do
    a=( $l )
    N7seq=${a[1]}
    N5seq=${a[2]}
    pop=${a[4]}
    gen=${a[5]}

    for i in 1 2; do
        gunzip -c ${OLDPREFIX}*_${N7seq}-${N5seq}.R${i}.fastq.gz \
            > ${NEWPREFIX}${pop}-${gen}.R${i}.fastq
    done
done
