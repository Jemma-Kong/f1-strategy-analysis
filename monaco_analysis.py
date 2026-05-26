import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fastf1

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()

ver_laps = session.laps.pick_drivers('VER').copy()
# 过滤：必须有有效圈速，且圈速合理（< 200s），排除 Lap 1 的会前数据噪声
ver_laps = ver_laps[
    ver_laps['LapTime'].notna() &
    (ver_laps['LapTime'].dt.total_seconds() < 200) &
    (ver_laps['LapNumber'] > 1)
].reset_index(drop=True)

# 找进站圈和最快圈（跳过 LapNumber==1，那一圈的 PitInTime 是起步数据噪声）
pit_lap = ver_laps[(ver_laps['PitInTime'].notna()) & (ver_laps['LapNumber'] > 1)].iloc[0]
fastest_lap = ver_laps.loc[ver_laps['LapTime'].idxmin()]

print(f"Pit stop on lap: {int(pit_lap['LapNumber'])}, duration: {pit_lap['LapTime'].total_seconds():.2f}s")
print(f"Fastest lap: Lap {int(fastest_lap['LapNumber'])}, {fastest_lap['LapTime'].total_seconds():.2f}s")

# 画图
fig, ax = plt.subplots(figsize=(14, 6))

all_stints = sorted(ver_laps['Stint'].unique())
palette = ['#3671C6', '#E8002D', '#888888']
stint_colors = {s: palette[i] for i, s in enumerate(all_stints)}

for stint_num in sorted(ver_laps['Stint'].unique()):
    stint_data = ver_laps[ver_laps['Stint'] == stint_num]
    color = stint_colors.get(stint_num, '#888888')
    ax.plot(
        stint_data['LapNumber'],
        stint_data['LapTime'].dt.total_seconds(),
        marker='o', markersize=3, linewidth=1.5,
        color=color, label=f'Stint {stint_num}'
    )

# 标出进站圈（竖线）
ax.axvline(
    x=pit_lap['LapNumber'],
    color='orange', linestyle='--', linewidth=1.5,
    label=f'Pit Stop (Lap {int(pit_lap["LapNumber"])})'
)
ax.text(
    pit_lap['LapNumber'] + 0.5,
    ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 95,
    'PIT', color='orange', fontsize=9, va='top'
)

# 标出最快圈（星号）
ax.scatter(
    fastest_lap['LapNumber'],
    fastest_lap['LapTime'].total_seconds(),
    color='gold', s=250, marker='*', zorder=5,
    edgecolors='black', linewidths=0.5,
    label=f'Fastest Lap: {fastest_lap["LapTime"].total_seconds():.2f}s (Lap {int(fastest_lap["LapNumber"])})'
)

ax.set_xlabel('Lap Number', fontsize=12)
ax.set_ylabel('Lap Time (seconds)', fontsize=12)
ax.set_title('Verstappen — 2024 Monaco GP: Lap Times by Stint', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig('monaco_stints.png', dpi=150)
print("Done! 图已保存为 monaco_stints.png")
