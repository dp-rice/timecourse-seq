# timecourse-seq

This repository contains a series of scripts for calling and annotating mutations from whole-population Illumina sequencing data from multiple time points of an evolution experiment. It is a simplified version of the pipeline used by McDonald, Rice, and Desai (2016). The pipeline takes a set of `.fastq` files containing raw sequencing reads, aligns them to a reference genome, calls candidate mutations, and filters them for likely mutations. The file `pipeline.sh` contains a series of `bash` commands, which submit `Slurm` jobs, run software, and execute scripts contained in the `src/` directory. Because it contains many steps, some of which are resource-intensive and submitted as batch jobs, this script should be executed line-by-line rather than all at once.

## Prerequisites
Batch jobs are submitted to the `Slurm` scheduler. If using `LSF` or another scheduler, you will have to write new submission scripts. If using `Slurm`, please make sure that the partition and other Slurm variables are appropriate for your cluster. You can find these variables in the various .slurm scripts.

The following software is used in the pipeline.
- `python-2.7`
- `bowtie2-2.1.0`: align reads to reference sequence
- `samtools-0.1.19`: handling .bam files
- `picard-tools-1.44`: marking duplicate reads
- GATK `UnifiedGenotyper`: run on permissive settings to call candidate mutations

## Authors
Daniel P. Rice created the pipeline and wrote all scripts - [dp-rice](https://github.com/dp-rice).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
