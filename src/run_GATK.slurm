#!/bin/bash
#SBATCH --array=0-17
#SBATCH -t 48:00:00
#SBATCH --mem=3750
#SBATCH -n 1
#SBATCH -p general
#SBATCH -o log/gatk_%A_%a.out
#SBATCH -e log/gatk_%A_%a.err

GATKPATH=$1
REFPREFIX=$2
CHROMFILE=$3
BAMLISTFILE=$4
OUTPUTPREFIX=$5

CHROM=$(sed ${SLURM_ARRAY_TASK_ID}'q;d' ${CHROMFILE})
OUTPUTFILE=${OUTPUTPREFIX}-${CHROM}.vcf

# Run GATK UnifiedGenotyper on the lowest confidence setting to get a permissive list of candidate mutations.
java -jar -Xmx2g ${GATKPATH} \
	-R ${REFPREFIX}.fasta \
	-T UnifiedGenotyper \
	-I ${BAMLISTFILE} \
	--genotype_likelihoods_model BOTH \
	-ploidy 1 \
	-stand_call_conf 4 \
	-o ${OUTPUTFILE}\
    -L ${CHROM}
