#!/bin/bash

# This script submits jobs to the cluster to align reads,
# sort the resulting BAM files and mark the duplicate reads.

# NOTE: Change to load the modules on your cluster
module load centos6/bowtie2-2.1.0
module load centos6/samtools-0.1.19
module load hpc/picard-tools-1.44

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
            src/bowtie_samtools_picard.batch
done
