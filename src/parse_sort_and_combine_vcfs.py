from sys import argv
import numpy as np

def get_read_count(string, idex):
    if string == '.':
        count = '0'
    else:
        count = string.split(':')[idex]
    return count

chrom_fn = argv[1]
prefix = argv[2]
planfile_fn = argv[3]

with open(chrom_fn) as chromfile:
    CHROMS = [line.strip() for line in chromfile]

with open(planfile_fn) as planfile:
    sample_list = ['-'.join(line.split()[-2:]) for line in planfile]

COLS_TO_GET = ['#CHROM', 'POS', 'REF', 'ALT']

header = ['CHROM', 'POS', 'REF', 'ALT'] + sample_list
header = '\t'.join(header)
print header

for chrom in CHROMS:
    vcf_fn = '{}-{}.vcf'.format(prefix, chrom)
    with open(vcf_fn) as vcf_file:
        for line in vcf_file:
            split_line = line.strip().split('\t')

            #Skip all the header lines with ##
            if split_line[0].startswith('##'):
                continue

            #From the header line with the column descriptions, get the indices of the columns that we want to output plus the format column
            if split_line[0].startswith('#'):
                vcf_header = split_line
                i_format = vcf_header.index('FORMAT')
                mut_label_indices = [vcf_header.index(col) for col in COLS_TO_GET]

                order = []
                for sample in sample_list:
                    i_sample = vcf_header.index(sample)
                    order.append(i_sample)
                continue

            #From the format entry, get the position of the allele depth (if there are alternate alleles) or total read depth (if there are not)
            line_format = split_line[i_format].split(':')
            if 'AD' in line_format:
                i_data = line_format.index('AD')
            elif 'DP' in line_format:
                i_data = line_format.index('DP')
            else:
                continue

            #Get the read counts and sort them according to the plan file
            sorted_data = [get_read_count(split_line[i], i_data) for i in order]

            mut_label = [split_line[i] for i in mut_label_indices]
            new_line = '\t'.join(mut_label + sorted_data)
            print new_line
