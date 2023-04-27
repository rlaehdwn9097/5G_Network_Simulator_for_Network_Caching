from matplotlib import pyplot as plt


contentList = []

for m in range(1,58100 + 1):
    contentList.append(m)

weightList = []
n = len(contentList)
a = 0
result = 0
for i in range(1,n+1):
    #print(i)
    result += i**-a

for k in range(1, n+1):
    weightList.append((1/k**a)/result)


print(sum(weightList))
plt.plot(weightList)
plt.show()