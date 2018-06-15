import numpy as np
from sys import argv

def autocorrelation(freqs):
    masked_freqs = np.ma.masked_array(freqs, np.isnan(freqs))
    first =  masked_freqs[:-1]
    second = masked_freqs[1:]
    if np.var(first) == 0 or np.var(second) == 0:
        return 0
    else:
        return np.ma.corrcoef(first, second)[0,1]

script, candidate_fn, plan_fn = argv

# The number of columns to take to identify the mutation
# (default takes: chrom, position, ref, alt)
len_mutid = 4

# Set up a dictionary organizing the samples by population.
with open(plan_fn) as planfile:
    samples = ['-'.join(line.split()[-2:]) for line in planfile]
pop_dict = {}
for sample in samples:
    pop = sample.split('-')[0]
    try:
        pop_dict[pop].append(sample)
    except KeyError:
        pop_dict[pop] = [sample]

with open(candidate_fn) as infile:
    header = infile.readline()

    print "Pop\t" + header.strip()

    sheader = header.split()
    sample_indices = {pop:[sheader.index(sample)
                                for sample in pop_dict[pop]]
                        for pop in pop_dict}

    for line in infile:
        sline  = line.split()
        mut_id = sline[:len_mutid]
        altlist = mut_id[3].split(',')
        n_alts = len(altlist)

        sline = ["0" + ",0"*n_alts if entry in ["0",'.'] else entry for entry in sline]

        ##### DELETE THIS TO ALLOW FOR MULTIPLE ALTs #####
        if n_alts > 1:
            continue
        #######################

        for pop in pop_dict:
            insample = np.array([map(float, sline[i].split(','))
                                for i in sample_indices[pop]])
            outsample = np.array([map(float, sline[i].split(','))
                                for i in range(len_mutid,len(sline)) if i not in sample_indices[pop]])

            ref_counts = insample[:,0]
            os_ref = outsample[:,0]
            for i in range(1, n_alts + 1):
                alt_counts = insample[:,i]
                #Filter on total read supporting the mutation
                if np.sum(alt_counts) < 10:
                    continue

                coverage  = ref_counts + alt_counts
                #Filter on total coverage within the population
                if np.mean(coverage) < 10:
                    continue

                frequency = alt_counts / coverage
                #Filter on maximum frequency
                if (frequency > 0.10).sum() < 1:
                    continue

                #Filter on frequency outside of the focal pop
                os_alt = outsample[:,i]
                os_cov = os_alt + os_ref
                os_freq = os_alt / os_cov
                os_freq = np.ma.masked_array(os_freq, np.isnan(os_freq))
                out_freq = np.mean(os_freq)
                if out_freq > 0.05:
                    continue

                ac = autocorrelation(frequency)
                #Filter on autocorrelation
                if ac < 0.2:
                    continue
                elif str(ac) == '--':
                    continue

                print pop + '\t' + line.strip()
