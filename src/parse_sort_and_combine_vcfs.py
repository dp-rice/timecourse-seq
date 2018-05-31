from sys import argv
import numpy as np

def get_read_count(string, idex):
    if string == '.':
        count = '0'
    else:
        count = string.split(':')[idex]
    return count

prefix = argv[1]
missing_tp_fn = argv[2]
readgroups_fn = argv[3]

# NOTE: Make sure these are appropriate for your organism.
CHROMS = ['chrI', 'chrII', 'chrIII', 'chrIV', 'chrV', 'chrVI', 'chrVII', 'chrVIII', 'chrIX', 'chrX', 'chrXI', 'chrXII', 'chrXIII', 'chrXIV', 'chrXV', 'chrXVI', 'chrMito']
COLS_TO_GET = ['#CHROM', 'POS', 'REF', 'ALT']

with open(missing_tp_fn) as missingfile:
    missing_tps = ['-'.join(line.split()) for line in missingfile]
with open(readgroups_fn) as rgfile:
    readgroups = {line.split()[0]:line.split()[1]
                    for line in rgfile.readlines()}

populations = sorted(list({key.split('-')[0] for key in readgroups.keys()}))
generations = np.arange(0,1000,90)
sample_list = ['{}-{}'.format(p,g) for p in populations for g in generations]

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
                    if sample in missing_tps:
                        i_sample = -1
                    else:
                        i_sample = vcf_header.index(readgroups[sample])
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
            sorted_data = ['0' if i<0 else get_read_count(split_line[i], i_data) for i in order]

            mut_label = [split_line[i] for i in mut_label_indices]
            new_line = '\t'.join(mut_label + sorted_data)
            print new_line
