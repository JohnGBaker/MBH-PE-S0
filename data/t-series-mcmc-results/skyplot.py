import numpy as np
import pylab as pl
from sklearn.neighbors.kde import KernelDensity


fig = pl.figure()
ax = fig.add_subplot(1, 1, 1, projection='hammer')

labels = ['40 h', '2.5 h', '7 m', 'Post-merger']
colors = ['g', 'b', 'r', 'k']
bandwidths = [0.2, 0.05, 0.01, 0.005]

for i, label, color, bw in zip([64, 16, 4, 1], labels, colors, bandwidths):
    print(i)
    data = np.loadtxt('STP_09_lm55_t{:02d}_joint_resampled.dat'.format(i))
    ra, dec = data[:,8], data[:,9]
    ra -= np.pi

    # create the KDE estimator
    # we could use grid-search cross validation to estimate the bandwidth here
    radec = np.vstack((dec, ra)).T
    kde = KernelDensity(kernel='tophat', bandwidth=bw, metric='haversine').fit(radec)

    # find the density levels corresponding to 1, 2, 3 sigmas
    n = 10000
    sample = kde.sample(n)
    sample_densities = np.sort(np.exp(kde.score_samples(sample)))
    levels = [sample_densities[int(n * (1 - p))] for p in [0.9973, 0.9545, 0.6827]]

    gra = np.linspace(-np.pi, np.pi, 300)
    gdec = np.linspace(-np.pi/2, np.pi/2, 300)
    ggra, ggdec = np.meshgrid(gra, gdec)
    d = np.exp(kde.score_samples(np.vstack((ggdec.ravel(), ggra.ravel())).T))
    d = np.reshape(d, ggra.shape)
    cs = ax.contour(gra, gdec, d, colors=color, linewidths=[0.5, 1, 1.5], levels=levels)
    cs.collections[0].set_label(label)

ax.grid()
ax.legend()
pl.savefig('skymap.png', dpi=200)
