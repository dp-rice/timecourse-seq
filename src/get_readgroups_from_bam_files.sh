#!/bin/bash
module load centos6/samtools-0.1.19

while read f; do
    RG=$(samtools view -H $f | awk -F ':' '/@RG/{print $3}')
    TP=${f##*/}
    TP=${TP%%.dm.bam}
    echo $TP $RG
done 
