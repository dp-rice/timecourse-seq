#!/bin/bash

# WARNING: Do not execute this file all at once.
# Several commands submit batch jobs and need to be run sequentially.

### bash variables ###

# Prefix for reference genome files.
# For example, if your reference genome is in the file `/Users/username/reference/ref_sequence.fasta`,
# REFPREFIX should be `/Users/username/reference/ref_sequence`
REFPREFIX=path_to_reference_genome
# NOTE: bowtie2 and GATK may require you to make some index files for your reference,
# but I don't remember which ones. Please see the docs for those programs.

# File with the name of one chromosome on each line.
# Names should match your reference sequence file.
CHROMFILE=chromosomes.txt

# Text file containing metadata for your sequenced timepoints
# The first four columns specify nextera tag information.
# Column 5 gives the population name.
# Column 6 gives the generation number.
# Rows should be sorted by population and then by generation.
PLANFILE=planfile.txt

# Directory containing your zipped original fastq files
SOURCEDIR=path_to_raw_fastq_files/

# Directory to store large intermediate files (e.g. .fastq, .bam)
DATADIR=path_to_intermediate_data_files/

# Path to GATK .jar file, wherever it is installed.
GATKPATH=/absolute/path/GenomeAnalysisTK.jar

# Create a log directory for slurm log files and directories for output files
mkdir -p log/
mkdir -p $DATADIR/fastq/
mkdir -p $DATADIR/bam/
mkdir -p $DATADIR/vcf/

### Batch jobs on computing cluster ###

# Unzip and rename fastq files according to population and generation.
# Creates new files, does not modify source files.
# WARNING: Make sure that your fastq filenames match the format in unzip_and_rename.slurm
sbatch -J unzip -o log/unzip.out -e log/unzip.err \
    src/unzip_and_rename.slurm \
    $PLANFILE \
    $SOURCEDIR/ \
    $DATADIR/fastq/

# Trim adaptor sequences from fastq files.
sbatch -J trim -o log/trim.out -e log/trim.err \
    src/trim_fastq.slurm \
    $PLANFILE \
    $DATADIR/fastq/

# Align reads to reference sequence with bowtie2.
# NOTE: Change to load the modules on your cluster
module load centos6/bowtie2-2.1.0
module load centos6/samtools-0.1.19
module load hpc/picard-tools-1.44
bash src/submit_bowtie_and_picard_jobs.sh \
    $PLANFILE \
    $DATADIR/fastq/ \
    $DATADIR/bam/ \
    $REFPREFIX

# Make a list of the duplicate-marked bam files you want to include in GATK run.
# NOTE: edit this file to ignore some bam files or include others.
ls -d $DATADIR/bam/*.dm.bam > bam_list.txt

# Call candidate variants using GATK.
sbatch --array=1-$(wc -l $CHROMFILE) \
    src/run_GATK.slurm \
    $GATKPATH \
    $REFPREFIX \
    $CHROMFILE \
    bam_list.txt \
    $DATADIR/vcf/snps_and_indels

# Parse vcf and merge files.
sbatch src/parse_vcfs.slurm \
    $CHROMFILE \
    $DATADIR/vcf/snps_and_indels \
    $PLANFILE \
    $DATADIR/vcf/snps_and_indels_parsed.txt

### May be done locally or interactively ###

# Filter candidate mutations. This is done in two steps:

# This script does most of the filtering. It filters on:
# - number of alternate alleles (=1)
# - total read count supporting the mutation (>=10)
# - maximum frequency within the focal population (>0.1)
# - average frequency outside of the focal population (<0.05)
# - frequency lag-1 autoccorelation (>0.2)
# NOTE: filter values are "magic numbers" in the code. You can modify them there.
python filter_mutations.py \
    $DATADIR/vcf/snps_and_indels_parsed.txt \
    $PLANFILE \
    > snps_and_indels_filtered1.txt

# This script does one additonal filtering step:
# calculates the likelihood of the data under the model:
# k ~ Binom(n,p),
# where k is the total allele count within the focal popualtion,
# n is the total coverage in the focal population,
# and p is the allele frequency outside of the focal population.
python filter_by_binomial_pvalues.py \
    snps_and_indels_filtered1.txt \
    1e-5 low \
    $PLANFILE \
    > snps_and_indels_filtered2.txt

# Annotate mutations.
python src/annotate_mutations.py \
    $CHROMFILE \
    src/genetic_code_table.txt \
    $REFPREFIX.gff \
    $REFPREFIX.fasta \
    < snps_and_indels_filtered2.txt \
    > snps_and_indels_filtered_annotated.txt
