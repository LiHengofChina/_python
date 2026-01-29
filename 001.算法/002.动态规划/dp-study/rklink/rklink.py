import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(15, 10))

# ===== 1️⃣ 加载中国地图背景 =====
china_img = mpimg.imread('china_map.jpg')


ax.imshow(
    china_img,
    extent=[76, 138, 18, 54],
    aspect='auto'
)



# ===== 2️⃣ 标题 =====
plt.title(
    '四川融科智联科技有限公司全国分支机构分布图',
    fontsize=20,
    fontweight='bold',
    color='#0066cc',
    pad=20
)

# ===== 3️⃣ 城市坐标 =====
cities = {
    '成都': (103.6, 30.),
    '北京': (115., 38.5),
    '上海': (121.0, 31.230416),

    '深圳': (114.057868, 22.543099),
    '重庆': (105.8, 29.1),
    '贵阳': (106.1, 26.2),
    '兰州': (103.2, 35.0),
    '西安': (108.939621, 34.343147),
    '昆明': (101.5, 24.880095)
}



# ===== 4️⃣ 画点 =====
for city, (lon, lat) in cities.items():
    ax.plot(
        lon, lat, 'o',
        markersize=12,
        color='#0066cc',
        markeredgecolor='white',
        markeredgewidth=3
    )

    ax.text(
        lon - 0.6,  # ← 向左
        lat + 0.2,  # 轻微上移，防止压住点
        f'{city}',
        fontsize=12,
        fontweight='bold',
        ha='right'  # ← 文字右对齐，更贴合点
    )

# ===== 5️⃣ 图例 =====
legend_elements = [
    mpatches.Circle(
        (0, 0),
        radius=5,
        facecolor='#0066cc',
        edgecolor='white',
        linewidth=3,
        label='分支机构'
    )
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=12)

# ===== 6️⃣ 坐标范围 & 样式 =====
ax.set_xlim(76, 138)
ax.set_ylim(18, 54)
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.grid(False)

plt.tight_layout()
plt.savefig('branches_with_china_map.png', dpi=300)
print('✅ 已生成：branches_with_china_map.png')
