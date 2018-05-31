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

script, candidate_fn, setup_fn = argv
execfile(setup_fn)

len_mutid = 4

with open(candidate_fn) as infile:
    header = infile.readline()

    print "Pop\t" + header.strip()

    sheader = header.split()
    insample_indices = {pop:[sheader.index(tp) for tp in insample_dict[pop]] for pop in populations}
    metapop_indices = {}
    for pop in populations:
        metapop_indices[pop] = []
        for i, tp in enumerate(sheader):
            if tp.split('-')[0] in metapop_dict[pop]:
                metapop_indices[pop].append(i)

    for line in infile:
        sline  = line.split()
        mut_id = sline[:len_mutid]
        altlist = mut_id[3].split(',')
        n_alts = len(altlist)

        sline = ["0" + ",0"*n_alts if entry == "0" else entry for entry in sline]

        ##### DELETE THIS TO ALLOW FOR MULTIPLE ALTs #####
        if n_alts > 1:
            continue
        #######################

        for pop in populations:
            insample = np.array([map(float, sline[i].split(',')) for i in insample_indices[pop]])
            metapop  = np.array([map(float, sline[i].split(',')) for i in metapop_indices[pop]])
#            alldata  = np.array([map(float, entry.split(',')) for entry in sline[len_mutid:]])

            outsample = np.array([map(float, sline[i].split(',')) for i in range(len_mutid,len(sline)) if i not in metapop_indices[pop]])
#            outsample_freq = map(float, [freq_line[j] for j in range(4,len(freq_line)) if j not in metapop_indices])

            ref_counts = insample[:,0]
            os_ref = outsample[:,0]
            mp_ref  = metapop[:,0]
#            all_ref = np.sum(alldata[:,0])
            for i in range(1, n_alts + 1):
                alt_counts = insample[:,i]
                #Filter on total read supporting the mutation
#                if np.sum(alt_counts) < 10:
#                    continue
                mp_alt_counts = metapop[:,i]
                if np.sum(mp_alt_counts) < 10:
                    continue

                coverage  = ref_counts + alt_counts
                #Filter on total coverage within the population
                if np.mean(coverage) < 10:
                    continue

                frequency = alt_counts / coverage
                mp_coverage = mp_ref + mp_alt_counts
                mp_freq = mp_alt_counts / mp_coverage
                #Filter on maximum frequency
#                if (frequency > 0.10).sum() < 2:
                if (mp_freq > 0.10).sum() < 2:
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
#                if ac < 0.15:
                    continue
                elif str(ac) == '--':
                    continue

                print pop + '\t' + line.strip()
#                statstring = "{0:.2f}\t{1:.2f}\t".format(ac, out_freq)
#                print pop + '\t' + line.strip() + '\t' + statstring


