# deficithawks
[![arXiv](https://img.shields.io/badge/arXiv-2204.03264-b31b1b.svg)](https://arxiv.org/abs/2204.03264)

This is the code used to produce the results in [Deficit hawks: robust new physics searches with unknown backgrounds](https://arxiv.org/abs/2204.03264).


  * Figure 1 / Example experiment: [cylinder.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/cylinder.ipynb)
  * Figure 2 / Neyman construction: [neyman_construction.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/neyman_construction.ipynb)
  * Figure 3 / Region sets comparison: [region_choice_plaw.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/region_choice_plaw.ipynb)
  * Figure 4 / $Q_\alpha(s)$  : [extra_scenarios.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/extra_scenarios.ipynb)
* Figures 5 and 6 / Statistic comparison : [statistic_choice.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/statistic_choice.ipynb)
 * Figure 7 / Known background: [known_bg.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/known_bg.ipynb)
 * Figure 8 / Known and unknown background: [mixed_bg.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/mixed_bg.ipynb)
 * Figure 9 / Detection claims: [discovery.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/discovery.ipynb)
 * Figure 11-14 / Additional Scenarios: [extra_scenarios.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/extra_scenarios.ipynb)

## Installation

This code depends on the [hypney](https://github.com/JelleAalbers/hypney) inference package. Until this appears on pypi, you can install it via
```
pip install git+https://github.com/JelleAalbers/hypney
```

Afterwards, you can run the notebooks in the repository folder.

## Caveats

If you want to play around with deficit hawks, this code may not be the ideal place to start. Although [cylinder.ipynb](https://github.com/JelleAalbers/deficithawks/blob/main/cylinder.ipynb) can be helpful, the other notebooks mainly test different scenarios in bulk.

Instead, you may prefer to use your favourite inference software (whether that is [RooFit](https://root.cern/manual/roofit/), [zfit](https://github.com/zfit/zfit), [pyhf](https://github.com/scikit-hep/pyhf), etc.) to brew your own deficit hawk. All you need is the ability to:

  * Do likelihood tests, and
  * Estimate the distribution of a test statistic through toy Monte Carlo.

These are both necessary anyway to do likelihood ratio inference -- unless you're in one of the lucky situations where you can use an asymptotic result like Wilks' theorem without worry..
