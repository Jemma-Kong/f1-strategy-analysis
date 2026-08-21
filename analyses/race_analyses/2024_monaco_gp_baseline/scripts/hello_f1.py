import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SESSION_KEY = 9523  # 2024 Monaco GP - Race

# 获取Verstappen的驾驶员编号
drivers_r = requests.get(
    f'https://api.openf1.org/v1/drivers?session_key={SESSION_KEY}&name_acronym=VER',
    timeout=30
)
driver = drivers_r.json()[0]
driver_number = driver['driver_number']
print(f"Driver: {driver['full_name']} #{driver_number}")

# 获取圈速数据
laps_r = requests.get(
    f'https://api.openf1.org/v1/laps?session_key={SESSION_KEY}&driver_number={driver_number}',
    timeout=60
)
laps = laps_r.json()
print(f"Total laps loaded: {len(laps)}")

# 过滤有效圈速（排除进出站异常圈）
valid_laps = [
    lap for lap in laps
    if lap.get('lap_duration') and lap['lap_duration'] < 120
]

lap_numbers = [lap['lap_number'] for lap in valid_laps]
lap_times = [lap['lap_duration'] for lap in valid_laps]

# 画图
plt.figure(figsize=(12, 5))
plt.plot(lap_numbers, lap_times, marker='o', markersize=3, linewidth=1.2, color='#3671C6')
plt.xlabel('Lap Number', fontsize=12)
plt.ylabel('Lap Time (seconds)', fontsize=12)
plt.title('Verstappen - 2024 Monaco GP Race Lap Times', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('first_plot.png', dpi=150)

print("Done! 图已保存为 first_plot.png")
