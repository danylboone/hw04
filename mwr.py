import math
import matplotlib.pyplot as plt

# constants
K_B = 1.3807e-23       # Boltzmann constant [J/K]
C   = 2.99792458e8     # speed of light [m/s]

# channels: (f_GHz, a, b, d, depth, F_obs)
channels = [
    (0.6,  2.0e-04, 1.15, 0.0025,   0.0,   7.59342e-21),
    (1.2,  4.0e-04, 1.18, 0.0027,  50.0,   6.15189e-20),
    (2.4,  8.0e-04, 1.20, 0.0030, 100.0,   3.90419e-19),
    (4.8,  1.6e-03, 1.23, 0.0033, 170.0,   1.86758e-18),
    (9.6,  3.2e-03, 1.26, 0.0036, 250.0,   8.12656e-18),
    (22.0, 7.0e-03, 1.30, 0.0040, 375.0,   4.14506e-17),
]

def F_model(T, f_GHz, a, b, d):
    if T <= 0:
        return 0.0
    f_hz = f_GHz * 1e9
    prefactor   = 2.0 * K_B * (f_hz ** 2) / (C ** 2)
    denominator = 1.0 + d * math.sqrt(T)
    absorption  = 1.0 - math.exp(-a * (T ** b))
    return prefactor * (T / denominator) * absorption

def bisection(F_target, f, a, b, d):
    low  = 10.0
    high = 5000.0

    for _ in range(10):
        f_low  = F_model(low,  f, a, b, d) - F_target
        f_high = F_model(high, f, a, b, d) - F_target
        if f_low * f_high <= 0:
            break
        low  = max(1e-6, low / 2.0)
        high = high * 2.0

    steps = 0
    while (high - low) > 1e-6 and steps < 300:
        mid = 0.5 * (low + high)
        f_mid = F_model(mid, f, a, b, d) - F_target
        if f_mid == 0.0:
            low = high = mid
            break
        if f_low * f_mid < 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
        steps += 1

    return 0.5 * (low + high)

temps  = []
depths = []

for idx, (f, a, b, d, depth, F_obs) in enumerate(channels, start=1):
    T = bisection(F_obs, f, a, b, d)
    temps.append(T)
    depths.append(depth)
    print("Channel", idx, "| f(GHz) =", f, "| depth(km) =", depth, "| T(K) =", f"{T:.6f}")

# T (x) vs depth (y), deeper is lower
plt.figure()
plt.plot(temps, depths, marker='o')
plt.xlabel("Temperature T [K]")
plt.ylabel("Depth from 1 bar level [km]")
plt.gca().invert_yaxis()
plt.title("Juno MWR: Retrieved Temperature vs Depth")
plt.grid(True)
plt.tight_layout()
plt.savefig("mwrTemperature1.png", dpi=150)
print("Saved plot: mwrTemperature.png")