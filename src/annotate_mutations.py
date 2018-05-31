import sys
import string
complem = string.maketrans('GATC','CTAG')

#This code takes a .gff file, a .fasta file, and a tab-separated text file with mutations, and outputs a tab-separated text file where the mutations have been annotated.

script, genetic_code_fn, gene_list_file, fasta_file = sys.argv

# Read in genetic code dictionary
genetic_code = {}
with open(genetic_code_fn) as genetic_code_file:
    for line in genetic_code_file:
	    linelist = line.strip().split('\t')
	    codons = linelist[3].split(', ')
	    for i in range(len(codons)):
		    genetic_code[codons[i]] = linelist[0].strip()

chrom_labels = ['chr' + i for i in ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI']]

gene_dict = {chrom:[] for chrom in chrom_labels}
with open(gene_list_file) as file_genes:
    for line in file_genes:
        if line.startswith('#'):
            continue

        else:
            linelist = line.split('\t')

            if linelist[2] == 'CDS':
                gene_chrom = linelist[0]
                gene_start = int(linelist[3])
                gene_stop  = int(linelist[4])

                note=linelist[8].strip().split(';')
                if note[0].split('=')[1].split('%')[0] == "Dubious":
                    dubious=True
                else:
                    dubious=False

                if len(note[1].split('=')[1]) < .5:
	                gene_name = note[2].split('=')[1]
                else:
	                gene_name = note[1].split('=')[1]
                gene_strand = linelist[6]
                gene_phase  = int(linelist[7])
                if dubious:
                    gene_name += "(Dubious)"
                gene_tup   = (gene_name, gene_start, gene_stop, gene_strand, gene_phase)
                try:
                    gene_dict[gene_chrom].append(gene_tup)
                except KeyError:
                    continue

sequence_dict = {}
with open(fasta_file) as fasta:
    for line in fasta:
        if line.startswith('>'):
            chrom = line.strip()[1:]
        else:
            try:
                sequence_dict[chrom] += line.strip()
            except KeyError:
                sequence_dict[chrom] = line.strip()


header = sys.stdin.readline()
sys.stdout.write(header.strip() + "\tGene\tBroad_type\tNarrow_type\n")

for line in sys.stdin:
	if line.startswith('#'):
		sys.stdout.write(line)
	else:
		line_list = line.split()
		read_loc = int(line_list[2])
		chrom = line_list[1]
		ref = line_list[3]
		alt = line_list[4]

        mutated_genes = []
        chrom_genes = gene_dict[chrom]
        for gene in chrom_genes:
            gene_start = gene[1]
            gene_stop  = gene[2]

            if gene_start <= read_loc <= gene_stop:
                mutated_genes.append(gene)

        if mutated_genes:
            gene_names   = []
            broad_types  = []
            narrow_types = []
            for gene in mutated_genes:
                gene_name, gene_start, gene_stop, gene_strand, gene_phase = gene
                gene_names.append(gene_name)
                #SNPS
                if len(ref) == 1 and len(alt) == 1:
                    flanking_region = sequence_dict[chrom][read_loc-11:read_loc+10]

                    if gene_strand == '+':
                        loc_in_codon = (read_loc - gene_start - gene_phase)%3
                        codon = flanking_region[10 - loc_in_codon:13 - loc_in_codon]
                        new_codon = flanking_region[10-loc_in_codon:10] + alt + flanking_region[11:13-loc_in_codon]
                    elif gene_strand == '-':
                        loc_in_codon = (gene_stop - read_loc - gene_phase)%3

                        codon = flanking_region[10-(2-loc_in_codon):13-(2-loc_in_codon)]
                        codon = string.translate(codon[::-1], complem)

                        new_codon = flanking_region[10-(2-loc_in_codon):10] + alt + flanking_region[11:13-(2-loc_in_codon)]
                        new_codon = string.translate(new_codon[::-1], complem)
                    else:
                        print "Gene strand error"

                    amino_acid = genetic_code[codon]
                    new_amino_acid = genetic_code[new_codon]
                    if amino_acid == new_amino_acid:
                        broad_types.append("Syn")
                        narrow_types.append("NA")
                    else:
                        broad_types.append("Non")
                        nt = "{}->{}".format(amino_acid, new_amino_acid)
                        narrow_types.append(nt)

                elif len(ref) == len(alt):
                    broad_types.append("Complex")
                    narrow_types.append("NA")
                elif (len(ref) - len(alt)) % 3 == 0:
                    broad_types.append("Non")
                    narrow_types.append("inframe_indel")
                else:
                    broad_types.append("Non")
                    narrow_types.append("frameshift")

            gene_name   = ','.join(gene_names)
            broad_type  = ','.join(broad_types)
            narrow_type = ','.join(narrow_types)
        else:
            gene_name   = "NA"
            broad_type  = "Intergenic"
            narrow_type = "NA"

        annot_string = "\t{}\t{}\t{}".format(gene_name, broad_type, narrow_type)
        sys.stdout.write(line.strip() + annot_string + '\n')
