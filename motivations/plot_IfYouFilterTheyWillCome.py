"""
Finding 'Oscillations' With Filters
===================================

Examining the results of filtering aperiodic signals.
"""

###################################################################################################
# Filtering Signals
# -----------------
#
# A common component of many analyses of neural time series is to filter them,
# typically to try to extract information from frequency bands of interest, that
# are chosen to reflect putative oscillations.
#
# However, one thing to keep in mind is that signals with broadband aperiodic activity
# will always contain power at all frequencies, and since this
#
# Filtering
#
# One of the corrolaries of thinking of neural signals of containing of aperiodic activity,
# with power at all frequencies is that there is always power within any arbitrarily defined
# frequency range. This power does not necessarily entail any periodic activity, but will look
# like periodic activity.
#
# In this notebook we will simulate purely aperiodic filters, and apply filters to them,
# exploring how this looks.
#

###################################################################################################

# Import numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Import the Bands object, for managing frequency band definitions
from fooof.bands import Bands

# Imports from NeuroDSP to simulate & plot time series
from neurodsp.sim import sim_powerlaw
from neurodsp.filt import filter_signal
from neurodsp.plts import plot_time_series
from neurodsp.utils import create_times, set_random_seed

###################################################################################################

# Define our bands of interest
bands = Bands({'delta' : [2, 4],
               'theta' : [4, 8],
               'alpha' : [8, 13],
               'beta' : [13, 30],
               'low_gamma' : [30, 50],
               'high_gamma' : [50, 150]})

###################################################################################################
# Simulating Data
# ~~~~~~~~~~~~~~~
#
# We will use simulated data for this example, simulating aperiodic signals,
# and filtering them into our bands of interest. First, let's simulate some data.
#

###################################################################################################

# Set random seed for the simulation
set_random_seed(21)

###################################################################################################

# Simulation settings
s_rate = 1000
n_seconds = 4
times = create_times(n_seconds, s_rate)

###################################################################################################

# Simulate a signal of aperiodic activity: pink noise
sig = sim_powerlaw(n_seconds, s_rate, exponent=-1)

###################################################################################################

# Plot our simulated time series
plot_time_series(times, sig)

###################################################################################################
# Filtering Aperiodic Signals
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Now that we have a simulated signal, let's filter it into each of our frequency bands.
#
# To do so, we will loop across our band definitions, and plot the filtered version
# of the signal.
#

###################################################################################################

# Check out Band-by-Band Filtering
_, axes = plt.subplots(len(bands), 1, figsize=(12, 15))
for ax, (label, f_range) in zip(axes, bands):

    # Filter the signal to the current band definition
    band_sig = filter_signal(sig, s_rate, 'bandpass', f_range)

    # Plot the time series of the current band, and adjust plot aesthetics
    plot_time_series(times, band_sig, title=label + ' ' + str(f_range), ax=ax)
    ax.set_xlim(0, n_seconds); ax.set_ylim(-1, 1); ax.set_xlabel('');

###################################################################################################
#
# As we can see, filtering a signal with aperiodic activity in it into arbitrary
# frequency ranges returns filtered signals that look like rhythmic components.
#
# Also, because our simulated signal has some random variation, the filtered components
# also exhibit some fluctuations.
#
# Overall, we can see from filtering this signal that:
#
# - narrowband filters will always rhythmic looking outputs
# - filtering a signal with aperiodic activity will always return non-zero outputs
# - there can be dynamics in the filtered results, due to variations of the
#   aperiodic properties of the input signal
#
# Altogether, this can be taken as another example of how just because time series
# can be represented as and decomposed into sinusoids, this does not indicate
# that these signals, or resulting decompositions, reflect rhythmic activity.
#

###################################################################################################
# Observing Changes in Filtered Signals
# -------------------------------------
#
# Next, let's consider what it looks like if you filter a signal that contains
# changes in the aperiodic activity.
#
# For this example, we will simulate a signal with aperiodic activity, with an abrupt
# change in the aperiodic activity, and then filter this signal into a narrow-band
# frequency range, to observe how this change appears in the filtered signal.
#

###################################################################################################

# Simulate a signal of with a change in aperiodic activity
sig_comp1 = sim_powerlaw(n_seconds/2, s_rate, exponent=-1.5, f_range=(None, 150))
sig_comp2 = sim_powerlaw(n_seconds/2, s_rate, exponent=-1, f_range=(None, 150))

# Combine each component signal to create a signal with a shift in aperiodic activity
sig_delta_ap = np.hstack([sig_comp1, sig_comp2])

###################################################################################################

# Plot our time series, with a shift in aperiodic activity
plot_time_series(times, sig_delta_ap)

###################################################################################################
#
# Let's first filter this signal in a low-frequency range that is typically
# examined for oscillatory activity, using the beta band as an example.
#

###################################################################################################

# Filter the signal to the current band definition
band_sig = filter_signal(sig_delta_ap, s_rate, 'bandpass', bands.beta)

# Plot the filtered time series
plot_time_series(times, band_sig)
plt.xlim(0, n_seconds); plt.ylim(-1, 1);

###################################################################################################
#
# In the above, we can see that this shift in the aperiodic component of the data
# exhibits as what looks to be change in beta band activity.
#
# We can also examine what this kind of shift looks like in high frequency regions that
# are sometimes analyzed, like our 'high-gamma' frequency band.
#

###################################################################################################

# Filter the signal to the current band definition
band_sig = filter_signal(sig_delta_ap, s_rate, 'bandpass', bands.high_gamma)

# Plot the filtered time series
plot_time_series(times, band_sig)
plt.xlim(0, n_seconds); plt.ylim(-1, 1);

###################################################################################################
#
# Collectively, what we can see here is that changes in aperiodic properties, that
# affect all frequencies, can look like band-specific changes when time series
# are analyzed with narrow-band filters.
#
# If individual bands are filtered and analyzed in isolation, without comparison
# either aperiodic measures, or other frequency bands, this kind of analysis could
# mis-interpret broadband aperiodic changes as oscillatory changes.
#
# Note that in real data, to what extent such aperiodic shifts occur is something
# of an open question. Within subject changes in aperiodic activity has been observed,
# and so this remains a possibility.
#

###################################################################################################
# Conclusions
# -----------
#
# Here we have seen that filtering signals to narrow band signals can return results
# that reflect aperiodic activity and dynamics. We therefore suggest that
# narrow band filtered signals should not be presumed to necessarily reflect periodic
# activity. In order to ascertain whether narrow band frequency regions reflect
# periodic and/or aperiodic activity and what features are changing in the data,
# additional analyses, such as parameterizing neural power spectra, are recommended.
#
