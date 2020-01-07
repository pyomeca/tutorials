# preparation
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from pyomeca import Analogs3d

data_path = Path("..") / ".." / "data" / "markers_analogs.c3d"

raw = Analogs3d.from_c3d(data_path)["Delt_ant.EMG1"].abs()
moving_average = raw.moving_average(window_size=100)


def create_plots(data, labels):
    _, ax = plt.subplots(figsize=(12, 6))
    for datum, label in zip(data, labels):
        datum.plot(label=label, lw=3, ax=ax)
    plt.legend()
    sns.despine()


# solution
moving_median = raw.moving_median(window_size=99)
create_plots(data=[raw, moving_median], labels=["raw", "moving median"])
plt.show()

moving_rms = raw.moving_rms(window_size=100)
create_plots(data=[raw, moving_rms], labels=["raw", "moving rms"])
plt.show()

create_plots(
    data=[moving_average, moving_median, moving_rms],
    labels=["moving average", "moving median", "moving rms"],
)
plt.show()

# ---
band_pass = raw.band_pass(freq=raw.get_rate, order=4, cutoff=[10, 200])
create_plots(data=[raw, band_pass], labels=["raw", "band-pass @ 10-200Hz"])
plt.show()

band_stop = raw.band_stop(freq=raw.get_rate, order=2, cutoff=[40, 60])
create_plots(data=[raw, band_stop], labels=["raw", "band-stop @ 40-60Hz"])
plt.show()

high_pass = raw.high_pass(freq=raw.get_rate, order=2, cutoff=100)
create_plots(data=[raw, high_pass], labels=["raw", "high-pass @ 100Hz"])
plt.show()

# ---
mvc = 0.0005562179366360516
emg = (
    raw.band_pass(freq=raw.get_rate, order=4, cutoff=[10, 425])
    .center()
    .rectify()
    .low_pass(freq=raw.get_rate, order=4, cutoff=5)
    .normalization(mvc)
    .time_normalization()
)
emg.plot()
plt.show()
