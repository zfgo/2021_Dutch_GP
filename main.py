"""
comparing HAM and BOT fastest laps in the 2021 Dutch GP

Code shamelessly stolen from:
https://medium.com/@jaspervhat/analyzing-formula-1-data-using-python-2021-dutch-gp-hamilton-vs-bottas-145945eac278
"""

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# Setup plotting
plotting.setup_mpl()
# Enable the cache

path_file = "path.txt"

with open(path_file, 'r') as f:
    path = f.read()

# path = <INSERT YOUR CACHE PATH HERE>

ff1.Cache.enable_cache(cache_dir=path,
                       ignore_version=False,
                       force_renew=False,
                       use_requests_cache=True)

# Load the session data
race = ff1.get_session(2021, 'Zandvoort', 'R')

# Collect all race laps
laps = race.load_laps(with_telemetry=True)

# Get laps of the drivers (BOT and HAM)
laps_bot = laps.pick_driver('BOT')
laps_ham = laps.pick_driver('HAM')
# Extract the fastest laps
fastest_bot = laps_bot.pick_fastest()
fastest_ham = laps_ham.pick_fastest()

# Get telemetry from fastest laps
telemetry_bot = fastest_bot.get_car_data().add_distance()
telemetry_ham = fastest_ham.get_car_data().add_distance()

fig, ax = plt.subplots(3)
fig.suptitle("Fastest Race Lap Telemetry Comparison")

ax[0].plot(telemetry_bot['Distance'], telemetry_bot['Speed'], label='BOT')
ax[0].plot(telemetry_ham['Distance'], telemetry_ham['Speed'], label='HAM')
ax[0].set(ylabel='Speed')
ax[0].legend(loc="lower right")
ax[1].plot(telemetry_bot['Distance'], telemetry_bot['Throttle'], label='BOT')
ax[1].plot(telemetry_ham['Distance'], telemetry_ham['Throttle'], label='HAM')
ax[1].set(ylabel='Throttle')
ax[2].plot(telemetry_bot['Distance'], telemetry_bot['Brake'], label='BOT')
ax[2].plot(telemetry_ham['Distance'], telemetry_ham['Brake'], label='HAM')
ax[2].set(ylabel='Brakes')
# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()

plt.show()
