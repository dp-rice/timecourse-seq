#!/bin/bash

# WARNING: Do not execute this file all at once.
# Several commands submit batch jobs and need to be run sequentially.

### bash variables ###

# Prefix for reference genome files.
# For example, if your reference genome is in the file `/Users/username/reference/ref_sequence.fasta`,
# REFPREFIX should be `/Users/username/reference/ref_sequence`
REFPREFIX=path_to_reference_genome

# Text file containing metadata for your sequenced timepoints
# The first four columns specify nextera tag information.
# Column 5 gives the population name.
# Column 6 gives the generation number.
PLANFILE=planfile.txt

# Directory containing your zipped original fastq files
SOURCEDIR=path_to_raw_fastq_files/

# Directory to store large intermediate files (e.g. .fastq, .bam)
DATADIR=path_to_intermediate_data_files/

### Batch jobs on computing cluster ###

# Create a log directory for slurm log files
mkdir -p log/

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
bash src/submit_bowtie_and_picard_jobs.sh \
    $PLANFILE \
    $DATADIR/fastq/ \
    $DATADIR/bam \
    $REFPREFIX

# Call candidate variants with GATK.

# Parse and vcf files.

### Locally or interactively ###

# Filter candidate mutations.

# Identify founder mutations.

# Identify mutations that are physically close to one another.

# Manually curate false-positives.

# Annotate mutations.

# Mark nearby "compound" mutations.
