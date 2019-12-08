import numpy as np

log_R = np.array([1, 2 * np.sqrt(3) / 3, np.sqrt(2), 2])
log_V = np.array([2132.9, 2130.0, 2124.5, 2119.6])
log_S = np.array([14.8, 16.1, 14.9, 14.1])

A = np.sum(log_R / log_S ** 2)
B = np.sum(1 / log_S ** 2)
C = np.sum(log_V / log_S ** 2)
D = np.sum(log_R ** 2 / log_S ** 2)
E = np.sum(log_R * log_V / log_S ** 2)
print(A, B, C, D, E)
print((E * B - C * A) / (B * D - A ** 2))
print((D * C - E * A) / (B * D - A ** 2))