import numpy as np
import pylab as pl

fig = pl.figure()
ax = fig.add_subplot(1, 1, 1, projection='hammer')

labels = ['40 h', '2.5 h', '7 m', 'Post-merger']

for i, label in zip([64, 16, 4, 1], labels):
    data = np.loadtxt('STP_09_lm55_t{:02d}_joint_resampled.dat'.format(i))
    ra, dec = data[:,8], data[:,9]
    ra -= np.pi

    ax.plot(ra, dec, 'o', markeredgewidth=0, markersize=2, label=label)

ax.grid()
ax.legend()
pl.savefig('skymap.png', dpi=200)
