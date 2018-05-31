from sys import argv
import numpy as np
from scipy.stats import binom

if len(argv) == 4:
    script, data_fn, p_cutoff, filterstyle = argv
    execfile("set_up_populations.py")
elif len(argv) == 5:
    script, data_fn, p_cutoff, filterstyle, setup_fn = argv
    execfile(setup_fn)


p_cutoff = float(p_cutoff)

#populations = ['3D', '6D', '10A', '2A', '5A', '2D', '5D', '8A']
#metapop_dict = {pop:[pop] for pop in populations}
#metapop_dict['2A'].append('5A')
#metapop_dict['5A'].append('2A')
#metapop_dict['2D'].append('5D')
#metapop_dict['5D'].append('2D')

#generations = np.arange(0,1000,90)

#insample_dict = {pop:["{0}-{1:d}".format(pop, gen) for gen in generations] for pop in populations}
##6D and 8A have no timepoint zero
#insample_dict['6D'].pop(0)
#insample_dict['8A'].pop(0)

with open(data_fn) as infile:
    header = infile.readline()
#    print header.strip() + "\tBinomPval"
    print header.strip()
    sheader = header.split()
    insample_indices = {pop:[sheader.index(tp) for tp in insample_dict[pop]] for pop in populations}

    for line in infile:
        sline = line.split()
        sline = ["0,0" if entry=="0" else entry for entry in sline]

        pop = sline[0]

        focal_total  = np.array([0.,0.])
        other_total = np.array([0.,0.])
        for p in populations:
            data = np.array([map(float, sline[i].split(',')) for i in insample_indices[p]])

            if p in metapop_dict[pop]:
                focal_total += np.sum(data, axis=0)
            else:
                other_total += np.sum(data, axis=0)

        ref_other, alt_other = other_total
        other_mean = alt_other / (alt_other + ref_other)
        ref_focal, alt_focal = focal_total
        pval = 1 - binom.cdf(alt_focal, ref_focal + alt_focal, other_mean)

#        outputstring = '\t'.join(sline) + '\t' + str(pval)
        outputstring = '\t'.join(sline)
        if filterstyle == "high":
            if pval > p_cutoff:
                print outputstring
        elif filterstyle == "low":
            if pval < p_cutoff:
                print outputstring
        else:
            print "Bad filterstyle!"

