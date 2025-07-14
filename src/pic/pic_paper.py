import matplotlib.pyplot as plt

# 数据
#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']
schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
x = [10, 20, 30, 40, 50]
costs = [
    [1.244, 1.309, 1.362, 1.550, 2.986],
    [2.105, 2.948, 3.682, 4.414, 7.268],
    [8.348, 16.148, 24.279, 32.755, 46.630],
    [2.162, 2.341, 2.507, 2.797, 5.836],
    [2.000, 2.245, 2.473, 2.886, 5.978]
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
plt.savefig("Storage_paper.pdf", format='pdf', bbox_inches='tight')

# 显示图表
plt.show()
