# Coding: utf-8

_all_ = [ 'plot_differential_kl', 'plot_differential_c' ]

import numpy as np
import NonResonantModelNLO

import matplotlib; import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)

def plot_differential_kl(nbins, xmin, xmax):
    """Plot differential mHH distributions with varying k_lambda."""
    kt, c2, cg, c2g = 1, 0, 0, 0
    
    mymodel = NonResonantModelNLO.NonResonantModelNLO()
    mymodel.ReadCoefficients("../data/pm_pw_NLO_Ais_13TeV_V2.txt") # local copy of coefficients
    nbins, xmin, xmax = 100, 250, 800

    kls = (-5, 1, 2.45, 5, 9)
    masses = np.linspace(xmin, xmax, 5000)
    labels = []
    
    histos = [[] for _ in range(len(kls))]
    for ikl, kl in enumerate(kls):
        for mhh in masses:
            xsec_diff = mymodel.getDifferentialXSmHH(mhh, kl, kt, c2, cg, c2g)
            histos[ikl].append(xsec_diff)
        labels.append(r"$k_{\lambda}="+str(kl)+"$")

    plot(masses, histos, legend=labels, ylabel=r"$d\sigma/dm_{HH}$ [a.u.]", savename="kl")
    
def plot_differential_c(nbins, xmin, xmax):
    """Plot differential mHH distributions with varying EFT couplings."""
    mymodel = NonResonantModelNLO.NonResonantModelNLO()
    mymodel.ReadCoefficients("../data/pm_pw_NLO_Ais_13TeV_V2.txt") # local copy of coefficients
    masses = np.linspace(xmin, xmax, 5000)

    # one columns per line plot
    kls    = (1, 1, 1, 1)
    kts    = (1, 1, 1, 1)
    c2s    = (0, 1, 0, 0)
    cgs    = (0, 0, 1, 0)
    c2gs   = (0, 0, 0, 1)
    labels = ("SM", r"$c_{2}="+str(c2s[1])+"$", r"$c_{g}="+str(cgs[2])+"$", r"$c_{2g}="+str(c2gs[3])+"$")
    
    histos = [[] for _ in range(len(kls))]
    for idx, (kl, kt, c2, cg, c2g) in enumerate(zip(kls,kts,c2s,cgs,c2gs)):
        for mhh in masses:
            xsec_diff = mymodel.getDifferentialXSmHH(mhh, kl, kt, c2, cg, c2g)
            histos[idx].append(xsec_diff)

    plot(masses, histos, legend=labels, ylabel=r"$d\sigma/dm_{HH}$ [fb/25GeV]", savename="c")

def plot(masses, histos, legend, ylabel, savename):
    fig = plt.figure(figsize=(16, 16),)
    ax = plt.subplot(111)
    ax.title.set_size(100)
    ax.set_yscale('log')

    #ax.axhline(y=0., color='gray', linestyle='dashed')
    ax.set_xlabel(r"$m_{HH}$ [GeV]")
    ax.set_ylabel(ylabel)

    for h,l in zip(histos, legend):
        ax.plot(masses, h, "-", label=l, linewidth=5)

    plt.legend(loc='best')

    hep.cms.text(' Preliminary', fontsize=30)
    #hep.cms.lumitext(title, fontsize=25) # r"138 $fb^{-1}$ (13 TeV)"

    savename = "/eos/user/b/bfontana/www/HHReweighting/" + savename
    for ext in ('.png', '.pdf',):
        plt.savefig(savename + ext, dpi=600)
        print('Stored in {}'.format(savename + ext))
    plt.close()

if __name__ == "__main__":
    nbins, xmin, xmax = 100, 250, 800
    plot_differential_kl(nbins, xmin, xmax)
    plot_differential_c(nbins, xmin, xmax)
