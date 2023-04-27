from matplotlib import pyplot as plt
import config as cf
import numpy as np
import math

figure, axes = plt.subplots()
'''
for i in range(cf.NUM_microBS[0]):
    for j in range(cf.NUM_microBS[1]):
        pos_x = (i+1)*cf.AREA_WIDTH/(cf.NUM_microBS[0]+1)
        pos_y = (j+1)*cf.AREA_LENGTH/(cf.NUM_microBS[1]+1)
        plt.scatter(pos_x, pos_y, color='b')
        circle = plt.Circle((pos_x, pos_y), 150, fill=False)
        axes.add_artist(circle)
'''
NUM_MBS = 5
NUM_sBS = 7
NUM_UE = 25

MBS_position = []
sBS_position = []

BS_x = 0
BS_y = 0

# https://www.wilsonamplifiers.com/blog/small-cells-picocells-and-microcells-the-complete-guide/
# https://dgtlinfra.com/small-cells-microcell-picocell-femtocell/
BS_range = 3
MBS_range = 1
sBS_range = 0.5

#plt.scatter(BS_x,BS_y, marker='+', s=150, color='orange', label='BS')
#circle = plt.Circle((BS_x, BS_y), BS_range, fill=True, color='orange', alpha=0.2, label='BS_Coverage')
#axes.add_artist(circle)

#MBS
for i in range(NUM_MBS):
    t = np.random.uniform(0, 360)
    d = np.random.uniform(BS_range/10, BS_range)
    x = d * math.cos(t) + BS_x
    y = d * math.sin(t) + BS_y
    MBS_position.append([x,y])
    plt.scatter(x,y, s=40, marker='o', color='green', label='MBS')
    circle = plt.Circle((x, y), MBS_range, fill=True, color='green', alpha=0.08, label='MBS_Coverage')
    axes.add_artist(circle)


#sBS
for i in range(NUM_sBS):
    selected_MBS = np.random.randint(0, NUM_MBS)
    MBS_x = MBS_position[selected_MBS][0]
    MBS_y = MBS_position[selected_MBS][1]

    t = np.random.uniform(0, 360)
    d = np.random.uniform(MBS_range/50, MBS_range)
    x = d * math.cos(t) + MBS_x
    y = d * math.sin(t) + MBS_y
    sBS_position.append([x,y])
    plt.scatter(x, y, s=80, marker='^', color='blue', label='sBS')
    circle = plt.Circle((x, y), sBS_range, fill=True, color='blue', alpha=0.2, label='sBS_Coverage')
    axes.add_artist(circle)

#UE
for i in range(NUM_UE):
    selected_sBS = np.random.randint(0, NUM_sBS)
    sBS_x = sBS_position[selected_sBS][0]
    sBS_y = sBS_position[selected_sBS][1]

    t = np.random.uniform(0, 360)
    d = np.random.uniform(sBS_range/20, sBS_range)
    x = d * math.cos(t) + sBS_x
    y = d * math.sin(t) + sBS_y
    plt.scatter(x, y, s=120, marker='*', color='red', label='UE')

handles, labels = axes.get_legend_handles_labels()
unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
axes.legend(*zip(*unique), loc='upper left', fontsize=20)

plt.xlim(-(BS_range+1),BS_range+1)
plt.ylim(-(BS_range+1),BS_range+1)
plt.show()
