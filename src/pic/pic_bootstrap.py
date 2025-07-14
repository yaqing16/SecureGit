import matplotlib.pyplot as plt

# 数据
schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']

#schemes = ['Git', 'SGitLine', 'SGitChar', 'Keybase-git', 'Git-crypt']
x = [10, 20, 30, 40, 50]
costs = [
    [0.769, 0.831, 0.820, 0.838, 0.858],
    [1.484, 2.080, 2.555, 3.407, 4.191],
    [4.845, 9.747, 14.550, 19.277, 24.025],
    [1.375, 1.710, 1.750, 1.826, 1.904],
    [1.213, 1.610, 1.708, 1.855, 1.979]
]


mark = ['o', 's', '*', 'D', '^']

#colour = ['brown', 'purple', 'green', 'blue', 'red']
colour = ['brown', 'green', 'orange', 'blue', 'red']
# 调整长宽比例为 8x6
plt.figure(figsize=(6, 4))

# 重新绘制图表，并为每条线使用不同的label
for i, scheme in enumerate(schemes):
    plt.plot(x, costs[i], marker=mark[i], label=scheme, linewidth=1.5, color=colour[i])

# 去掉标题（不设置标题）
# plt.title('Cost (MB) vs Scheme')

# 设置轴标签和图例
plt.xlabel('# of updates', fontsize=18)
plt.ylabel('Local storage costs (MB)', fontsize=18)
plt.xticks(x, fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True)
plt.legend(fontsize=16)

# 添加完整的边框
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.gca().spines['left'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)

# 保存图表为PDF文件
plt.savefig("Storage_bootstrap.pdf", format='pdf', bbox_inches='tight')

# 显示图表
plt.show()
