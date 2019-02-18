from sys import argv
import numpy as np
from scipy.stats import binom

script, data_fn, p_cutoff, filterstyle, plan_fn = argv
p_cutoff = float(p_cutoff)

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

with open(data_fn) as infile:
    header = infile.readline()
    print header.strip()
    sheader = header.split()
    sample_indices = {pop:[sheader.index(sample) for sample in pop_dict[pop]]
                        for pop in pop_dict}

    for line in infile:
        sline = line.split()
        sline = ["0,0" if entry=="0" else entry for entry in sline]

        pop = sline[0]

        focal_total  = np.array([0.,0.])
        other_total = np.array([0.,0.])
        for p in pop_dict:
            data = np.array([map(float, sline[i].split(','))
                                for i in sample_indices[p]])
            p == pop:
                focal_total += np.sum(data, axis=0)
            else:
                other_total += np.sum(data, axis=0)

        ref_other, alt_other = other_total
        other_mean = alt_other / (alt_other + ref_other)
        ref_focal, alt_focal = focal_total
        pval = 1 - binom.cdf(alt_focal, ref_focal + alt_focal, other_mean)

        outputstring = '\t'.join(sline)
        if filterstyle == "high":
            if pval > p_cutoff:
                print outputstring
        elif filterstyle == "low":
            if pval < p_cutoff:
                print outputstring
        else:
            print "Bad filterstyle!"
