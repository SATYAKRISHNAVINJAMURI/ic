import matplotlib.pyplot as plt


lena = [37.1019957209,
        42.9957946193,
        45.4197820733,
        46.6307519775,
        49.0251043666,
        50.0488484697,
        52.9053025884]



pepper = [14.1518912585,
19.0089996895,
22.2706351747,
24.4555569359,
27.1006709945,
29.1793964607,
30.2594952282
]
baboon= [12.9389105211,
19.7240143809,
25.004822878,
28.7963050899,
34.1990379194,
37.2572262505,
39.2582024829
]
noofclusters = [8,12,16,20,24,28,32]

plt.title("No of Clusters vs PSNR")
plt.plot(noofclusters,lena,'ro')
plt.plot(noofclusters,pepper,'bx')
plt.plot(noofclusters,baboon,'g*')
plt.xlabel("No of Clusters.")
plt.ylabel("PSNR.")
plt.legend(('Lena', 'Pepper', 'Baboon'),
           loc='upper right')

plt.axis([0,40, 10, 60])
plt.show()