import numpy as np

populations = ['3D', '6D', '10A', '2A', '5A', '2D', '5D', '8A']
populations += ['10F', '2C', '5C', '6C', '8F']
populations += ['8B', '10C', '10D', '10E']
metapop_dict = {pop:[pop] for pop in populations}
metapop_dict['2A'].append('5A')
metapop_dict['5A'].append('2A')
metapop_dict['2D'].append('5D')
metapop_dict['5D'].append('2D')
metapop_dict['2C'].append('5C')
metapop_dict['5C'].append('2C')

generations = np.arange(0,1000,90)

insample_dict = {pop:["{0}-{1:d}".format(pop, gen) for gen in generations] for pop in populations}
