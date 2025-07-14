import matplotlib.pyplot as plt


#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']
schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
x = [10, 20, 30, 40, 50]
costs = [
    [2.442, 2.457, 2.473, 2.494, 2.518],
    [4.264, 4.348, 4.496, 4.578, 4.790],
    [20.573, 38.742, 56.911, 75.157, 93.447],
    [5.864, 5.901, 5.935, 5.978, 6.033],
    [4.258, 4.392, 4.438, 4.481, 4.547]
]


mark = ['o', 's', '*', 'D', '^']

#colour = ['green', 'red', 'blue', 'teal', 'brown']
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


plt.savefig("Storage_react.pdf", format='pdf', bbox_inches='tight')


plt.show()
