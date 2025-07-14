import matplotlib.pyplot as plt


#schemes = ['Trivial-enc-sign', 'Git-crypt', 'SGitLine', 'SGitChar', 'Git']
schemes = ['Git', 'Git-crypt', 'Trivial-enc-sign', 'SGitLine', 'SGitChar']
x = [10, 20, 30, 40, 50]
costs = [
    [0.076, 0.082, 0.089, 0.097, 0.105],
    [0.275, 0.507, 0.685, 0.947, 1.212],
    [0.349, 0.662, 0.976, 1.291, 1.611],
    [0.176, 0.190, 0.205, 0.222, 0.239],
    [0.256, 0.276, 0.292, 0.314, 0.331]
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


plt.savefig("Storage_FPB.pdf", format='pdf', bbox_inches='tight')


plt.show()
