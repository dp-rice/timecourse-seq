#!/bin/bash

### bash variables ###

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

# Unzip and rename fastq files according to population and generation.
# Creates new files, does not modify source files.
# WARNING: Make sure that your fastq filenames match the format in unzip_and_rename.slurm
# WARNING: Make sure that you have a slurm/ directory in your working directory or specify a different location for slurm output and error files.
sbatch -J unzip -o slurm/unzip.out -e slurm/unzip.err \
    src/unzip_and_rename.slurm \
    $PLANFILE \
    $SOURCEDIR/ \
    $DATADIR/fastq/

# Trim adaptor sequences from fastq files.

# Align reads to reference sequence with bowtie2.

# Call candidate variants with GATK.

# Parse and vcf files.

### Locally or interactively ###

# Filter candidate mutations.

# Identify founder mutations.

# Identify mutations that are physically close to one another.

# Manually curate false-positives.

# Annotate mutations.

# Mark nearby "compound" mutations.
