import matplotlib.pyplot as plt


schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']
#schemes = ['Git', 'SGitLine', 'SGitChar', 'Keybase-git', 'Git-crypt']
x = [10, 20, 30, 40, 50]
costs = [
    [0.038, 2.199, 2.107, 2.260, 2.925],
    [0.508, 4.519, 4.425, 4.791, 5.834],
    [1.485, 8.614, 22.076, 36.403, 53.262],
    [0.588, 6.430, 6.238, 6.871, 7.908],
    [0.559, 4.848, 4.760, 5.114, 6.139]
]


mark = ['o', 's', '*', 'D', '^']

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


plt.savefig("Storage_FCC.pdf", format='pdf', bbox_inches='tight')


plt.show()
