import matplotlib
matplotlib.use('Agg')
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()

drivers = ['VER', 'LEC', 'SAI', 'NOR', 'HAM', 'PER']

# ---- detect red flag lap: lap with highest median time across all drivers ----
all_laps = session.laps[session.laps['LapTime'].notna()].copy()
all_laps['LapTimeSec'] = all_laps['LapTime'].dt.total_seconds()
median_by_lap = all_laps.groupby('LapNumber')['LapTimeSec'].median()
red_flag_lap = int(median_by_lap.idxmax())
print(f"Red flag lap detected: Lap {red_flag_lap}  (median={median_by_lap[red_flag_lap]:.1f}s)")

# Also confirm via race control messages if available
rcm = session.race_control_messages
rf_msgs = rcm[rcm['Message'].str.contains('RED FLAG', case=False, na=False)]
if not rf_msgs.empty:
    print("Race control red flag messages:")
    print(rf_msgs[['Time', 'Message']].to_string())

# ---- plot ----
fig, ax = plt.subplots(figsize=(14, 7))

for drv in drivers:
    drv_laps = session.laps.pick_drivers(drv).copy()
    drv_laps = drv_laps[drv_laps['LapTime'].notna()].copy()
    drv_laps['LapTimeSec'] = drv_laps['LapTime'].dt.total_seconds()

    # Exclude the red-flag lap itself — it's an outlier (41 min wait baked in)
    # We annotate it via axvline instead of plotting the raw spike
    drv_laps = drv_laps[drv_laps['LapTimeSec'] < 300]

    # driver colour — try modern API first, fall back to legacy
    try:
        color = fastf1.plotting.get_driver_color(drv, session=session)
    except TypeError:
        try:
            color = fastf1.plotting.driver_color(drv)
        except Exception:
            color = None

    ax.plot(
        drv_laps['LapNumber'],
        drv_laps['LapTimeSec'],
        color=color, label=drv,
        marker='o', markersize=3, linewidth=1.5,
    )

# red flag vertical line
ax.axvline(
    x=red_flag_lap,
    color='red', linestyle='--', linewidth=2, alpha=0.8,
    label=f'Red Flag (Lap {red_flag_lap})',
)
# Place text inside the y-axis range after data is plotted
ymin, ymax = ax.get_ylim()
ax.text(
    red_flag_lap + 0.4, ymax - (ymax - ymin) * 0.04,
    f'RED FLAG\nLap {red_flag_lap}',
    color='red', fontsize=9, va='top',
)

ax.set_xlabel('Lap Number', fontsize=12)
ax.set_ylabel('Lap Time (seconds)', fontsize=12)
ax.set_title('2024 Monaco GP — Top 6 Drivers Lap Times', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('monaco_top6.png', dpi=150)
print("Saved monaco_top6.png")
