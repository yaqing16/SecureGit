import matplotlib.pyplot as plt


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


plt.savefig("Storage_DocRepo.pdf", format='pdf', bbox_inches='tight')


plt.show()
