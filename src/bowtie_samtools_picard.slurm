#!/bin/bash
#SBATCH -t 48:00:00
#SBATCH --mem=3750
#SBATCH -n 1
#SBATCH -p general

bowtie2 --rg-id ${INDEX} --rg SM:${INDEX} -x ${REFPREFIX} -X 1000 \
	-1 ${FQDIR}/${INDEX}.R1.trimmed.fastq \
	-2 ${FQDIR}/${INDEX}.R2.trimmed.fastq \
	| samtools view -hbS - > ${BAMDIR}/${INDEX}.unsorted.bam

samtools sort -m 10000000 ${BAMDIR}/${INDEX}.unsorted.bam ${BAMDIR}/${INDEX}

rm ${BAMDIR}/${INDEX}.unsorted.bam

java -jar -Xmx2g /n/sw/picard-tools-1.44/MarkDuplicates.jar \
	INPUT=${BAMDIR}/${INDEX}.bam \
	OUTPUT=${BAMDIR}/${INDEX}.dm.bam \
	METRICS_FILE=picard_metrics/picard-${INDEX}.txt \
	ASSUME_SORTED=TRUE

samtools index ${BAMDIR}/${INDEX}.dm.bam
