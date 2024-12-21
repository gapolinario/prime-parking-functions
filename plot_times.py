import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def frexp_base10(x):
    if x == 0:
        return 0.0, 0  # Handle zero separately
    e = int(np.floor(np.log10(abs(x))))  # Find the base-10 exponent
    m = x / (10**e)  # Normalize the fraction
    return m, e

def print_pow10(x):

    m, e = frexp_base10(x)

    return rf"$\left( {{{m:.2f}}} \times 10^{{{e}}} \right)$"

def fit_xpowx(x, a, b):
    return a * np.power(x, b * x)

def fit_powx(x, a, b):
    return a * np.power(b, x)

def main():

    datBF = "data/timeBF.dat"
    datTR = "data/timeTR.dat"

    all_times = np.loadtxt(datBF,delimiter=',')
    nmaxBF = int(max(all_times[:,0]))
    timeBF = np.empty(nmaxBF)

    for n in range(1,nmaxBF+1):
        filter = all_times[np.isclose(all_times[:,0],n)]
        timeBF[n-1] = np.mean(filter[:,1])

    all_times = np.loadtxt(datTR,delimiter=',')
    nmaxTR = int(max(all_times[:,0]))
    timeTR = np.empty(nmaxTR)

    for n in range(1,nmaxTR+1):
        filter = all_times[np.isclose(all_times[:,0],n)]
        timeTR[n-1] = np.mean(filter[:,1])

    xBF = np.arange(1, nmaxBF+1)
    xTR = np.arange(1, nmaxTR+1)

    optBF, _ = curve_fit(fit_xpowx, xBF, timeBF)
    optTR, _ = curve_fit(fit_xpowx, xTR, timeTR)
    #optTR2, _ = curve_fit(fit_powx, xTR, timeTR)

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    ax.plot(xBF, timeBF, label="Brute force", lw=3)
    ax.plot(
        xBF,
        fit_xpowx(xBF, *optBF),
        ls="dashed",
        color="k",
        label=rf"fit: "+print_pow10(optBF[0])+rf" $\times \, n^{{{optBF[1]:5.3f}}}$",
        lw=2,
    )
    ax.plot(xTR, timeTR, label="Tree", lw=3)
    ax.plot(
        xTR,
        fit_xpowx(xTR, *optTR),
        ls="dashed",
        color="k",
        label=rf"fit: "+print_pow10(optTR[0])+rf" $\times \, n^{{{optTR[1]:5.3f}}}$",
        lw=2,
    )
    ax.grid(visible=True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_title(r"Time to enumerate $|\mathrm{PF}'(n)|$", fontsize=20, color='darkgreen')
    ax.set_ylabel(f"T(n)", fontsize=18, labelpad=10)
    ax.set_xlabel(f"n", fontsize=18, labelpad=10)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(bottom=1e-6)
    ax.legend(fontsize=14, loc='upper left', frameon=True, shadow=True, borderpad=1, facecolor='white')


    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()
