import numpy as np
scores = [55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
np.percentile(scores, 25)   # 25th percentile
np.percentile(scores, 50)   # 50th percentile = median
np.percentile(scores, 90)   # 90th percentile

from scipy.stats import binom

# Probability of exactly 7 heads in 10 flips
print(binom.pmf(7, n=10, p=0.5))

print(binom.cdf(7, n=10, p=0.5))


import numpy as np
from scipy import stats

sample = np.array([72, 68, 75, 71, 69, 74, 70, 73, 67, 76])
mean = np.mean(sample)
sem = stats.sem(sample)   # standard error of the mean
ci = stats.t.interval(0.95, len(sample)-1, loc=mean, scale=sem)
print(mean, ci)