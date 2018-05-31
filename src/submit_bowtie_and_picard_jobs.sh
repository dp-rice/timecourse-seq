#!/bin/bash

# This script submits jobs to the cluster to align reads,
# sort the resulting BAM files and mark the duplicate reads.

PLANFILE=$1
export FQDIR=$2
export BAMDIR=$3
export REFPREFIX=$4

sed 1d $PLANFILE |
while read l; do
    a=( $l )
    pop=${a[4]}
    gen=${a[5]}
    export INDEX=${pop}-${gen}
    echo ${INDEX}
    sbatch  -J ${INDEX} \
            -o log/bowtie-${INDEX}.out \
            -e log/bowtie-${INDEX}.err \
            src/bowtie_samtools_picard.slurm
done
