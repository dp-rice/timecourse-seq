# timecourse-seq

This repository contains a series of scripts for calling and annotating mutations from whole-population Illumina sequencing data from multiple time points of an evolution experiment. It is a simplified version of the pipeline used in McDonald et al. 2016. The pipeline takes a set of `.fastq` files containing raw sequencing reads, aligns them to a reference genome, calls candidate mutations, and filters them for likely mutations. The file `pipeline.sh` contains a series of `bash` commands, which submit `Slurm` jobs, run software, and execute scripts contained in the `src/` directory. Because it contains many steps, some of which are resource-intensive and submitted as batch jobs, this script should not be executed line-by-line rather than all at once.

## Prerequisites
- Batch jobs are submitted to the `Slurm` scheduler. If using `LSF` or another scheduler, you will have to write new submission scripts.
## Authors

## License
