## Dyadic Strategic Inference in the International Arms Trade in Europe
#### David Masad

Code for 2013 Qualifying Paper, Department of Computational Social Science, George Mason University

This repository contains the code and data needed to replicate the paper's results, organized as follows:

**fast_calc/**: Cython code to accelerate the conditional probability calculation

**src/**: Main code and analyses

*Main tools*

**Eventseries.py**: Main class to handle the event series and calculations on it, particularly finding the correlation network.

**GenerativeModel.py**: Code for the generative model, including the null model and several goodness-of-fit tests.

*Analyses and results* 


**SIPRI Analysis Europe.ipynb**: The initial pass on the analysis; generates the initial correlation network **probs_n_100.pickle** and some first pass goodness-of-fit measures that are not used in the final paper.

**SIPRI Analysis Europe - v2.ipynb**: Main analysis for the in-sample prediction test.

**SIPRI Analysis Europe 90s.ipynb**: Out of sample prediction, using **probs-91_n_100.pickle** correlation network data.

**Correlation network drawing.ipynb**: Drawing the correlation network (paper Fig. 1).