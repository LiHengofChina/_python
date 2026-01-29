# 必须放在最前面：使用无 GUI 后端（不依赖 Tk）
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 中文支持
plt.rcParams['font.sans-serif'] = ['SimHei']   # Windows 常见中文字体
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(15, 10))

# 标题
plt.title(
    '四川融科智联科技有限公司全国分支机构分布图',
    fontsize=20,
    fontweight='bold',
    color='#0066cc',
    pad=20
)

# 城市坐标（经度, 纬度）
cities = {
    '成都': (104.06, 30.67),
    '北京': (116.41, 39.91),
    '上海': (121.47, 31.23),
    '深圳': (114.07, 22.55),
    '广州': (113.23, 23.16),
    '武汉': (114.31, 30.52),
    '西安': (108.95, 34.27),
    '杭州': (120.19, 30.26)
}

# 绘制城市点
for city, (lon, lat) in cities.items():
    ax.plot(
        lon, lat, 'o',
        markersize=12,
        color='#0066cc',
        markeredgecolor='white',
        markeredgewidth=3
    )
    ax.text(
        lon + 0.5,
        lat + 0.5,
        f'融科智联·{city}',
        fontsize=12,
        fontweight='bold'
    )

# 图例
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
ax.legend(handles=legend_elements, loc='upper right', fontsize=12)

# 样式
ax.set_facecolor('#f8f9fa')
ax.grid(True, alpha=0.3)
ax.set_xlabel('经度', fontsize=12)
ax.set_ylabel('纬度', fontsize=12)

# 保存图片（关键）
plt.tight_layout()
plt.savefig('branches.png', dpi=300)
print('✅ 图片已生成：branches.png')
