import matplotlib.pyplot as plt


schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']
x = [10, 20, 30, 40, 50]
costs = [
    [0.037, 0.044, 0.052, 0.059, 0.066],
    [0.054, 0.086, 0.122, 0.164, 0.205],
    [0.059, 0.094, 0.137, 0.187, 0.241],
    [0.049, 0.063, 0.082, 0.099, 0.114],
    [0.050, 0.066, 0.092, 0.118, 0.135]
]


mark = ['o', 's', '*', 'D', '^']

#colour = ['brown', 'purple', 'green', 'blue', 'red']
colour = ['brown', 'green', 'orange', 'blue', 'red']

plt.figure(figsize=(6, 4))


for i, scheme in enumerate(schemes):
    plt.plot(x, costs[i], marker=mark[i], label=scheme, linewidth=1.5, color=colour[i])

# plt.title('Cost (MB) vs Scheme')


plt.xlabel('# of updates', fontsize=18)
plt.ylabel('Local storage costs (MB)', fontsize=18)
plt.xticks(x, fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True)
plt.legend(fontsize=16)


plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.gca().spines['left'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)

plt.savefig("Storage_awesome.pdf", format='pdf', bbox_inches='tight')


plt.show()
