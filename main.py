from tkinter import *
import numpy as np
import tkinter as tk
from copy import deepcopy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

window = tk.Tk()
window.title("Clustering Application")
attribute_0 = IntVar()
attribute_1 = IntVar()
attribute_2 = IntVar()
filename = 'irys.tab'
groups_number_string = StringVar()
datas = np.ndarray(shape=(150, 3), dtype=int)
groups = np.ndarray(150, dtype=int)
colors = (['red', 'green', 'blue', 'brown', 'yellow', 'black', 'orange', 'purple'])
xs = np.ndarray(150, dtype=int)
ys = np.ndarray(150, dtype=int)
zs = np.ndarray(150, dtype=int)
is_step_by_step = False

def input_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('attr0')
    ax.set_ylabel('attr1')
    ax.set_zlabel('attr2')
    ax.scatter(xs, ys, zs)
    plt.show()

def step_by_step():
    global is_step_by_step
    is_step_by_step = True
    preparing(False)

def clustering():
    global is_step_by_step
    is_step_by_step = False
    preparing(False)

def clustering_with_weights():
    global is_step_by_step
    is_step_by_step = False
    preparing(True)

def step_by_step_with_weights():
    global is_step_by_step
    is_step_by_step = True
    preparing(True)

def plot():
    if(is_step_by_step):
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('attr0')
        ax.set_ylabel('attr1')
        ax.set_zlabel('attr2')
        for x, y, z, group in zip(xs, ys, zs, groups):
            ax.scatter(x, y, z, c=colors[group])
            plt.pause(0.05)
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('attr0')
        ax.set_ylabel('attr1')
        ax.set_zlabel('attr2')
        for x, y, z, group in zip(xs, ys, zs, groups):
            ax.scatter(x, y, z, c=colors[group])
        plt.show()

def preparing(is_with_weight):
    groups_number = int(groups_number_string.get())
    least = [100,100,100]
    big = [0,0,0]
    difference = [0,0,0]
    centroids = np.ndarray(shape=(groups_number, 3), dtype=float)
    for data in datas:
        if(data[0] > big[0]):
            big[0] = data[0]
        if(data[0] < least[0]):
            least[0] = data[0]
        if(data[1] > big[1]):
            big[1] = data[1]
        if(data[1] < least[1]):
            least[1] = data[1]
        if(data[2] > big[2]):
            big[2] = data[2]
        if(data[2] < least[2]):
            least[2] = data[2]
    for i in range(0,3):
        difference[i] = (big[i]-least[i])/(groups_number-1)
    for i in range(0,groups_number):
        centroids[i][0] = least[0]+((i)*difference[0])
        centroids[i][1] = least[1]+((i)*difference[1])
        centroids[i][2] = least[2]+((i)*difference[2])
    print('First Centroids')
    print(centroids)
    if(is_with_weight == True):
        da = big[0] - least[0]
        db = big[1] - least[1]
        dc = big[2] - least[2]
        maxd = 0
        if(da >= db):
            if(da >= dc):
                maxd = da
            else:
                maxd = dc
        else:
            if(db >= dc):
                maxd = db
            else:
                maxd = dc
        weight_1 = da / maxd
        weight_2 = db / maxd
        weight_3 = dc / maxd
        determine_groups(centroids, groups_number, 0, weight_1, weight_2, weight_3)
    else:
        determine_groups(centroids, groups_number, 0, 1, 1, 1)

def determine_groups(centroids, groups_number, counter, weight_1, weight_2, weight_3):
    counter = counter + 1
    group = -1
    for i in range(0, 150):
        least_distance = -1
        for j in range(0, groups_number):
            distance = np.sqrt(((datas[i][0] - centroids[j][0])**2)*attribute_0.get()*weight_1 + ((datas[i][1] - centroids[j][1])**2)*attribute_1.get()*weight_2 + ((datas[i][2] - centroids[j][2])**2)*attribute_2.get()*weight_3)
            if(np.all(least_distance == -1)):
                least_distance = distance
                group = j
            elif(np.all(distance < least_distance)):
                least_distance = distance
                group = j
        if(group == -1):
            print("Error while determining groups")
        else:
            groups[i] = group
    print('Iteration '+str(counter))
    print('Groups')
    print(groups)
    if(update_centroids(centroids, groups_number) & (counter < 100)):
        determine_groups(centroids, groups_number, counter, weight_1, weight_2, weight_3)
    else:
        print('Clustering operation is completed with '+str(counter)+' iteration')
        print(groups)
        plot()

def update_centroids(centroids, groups_number):
    is_change = False
    old_centroids = deepcopy(centroids)
    counts = np.zeros(groups_number)
    sum = np.zeros(shape=(groups_number,3))
    for i in range(0,150):
        for j in range(0,3):
            sum[groups[i]][j] = sum[groups[i]][j]+datas[i][j]
        counts[groups[i]] += 1
    print('Sums')
    print(sum)
    print('Counts')
    print(counts)
    for i in range(0,groups_number):
        for j in range(0,3):
                    centroids[i][j] = sum[i][j] / counts[i]
    for i in range(0, groups_number):
        for j in range(0,3):
            if(centroids[i][j] != old_centroids[i][j]):
                is_change = True
                break
    print('Updated Centroids')
    print(centroids)
    return is_change

def click_weight():
    print('click')

def read_file():
    file = open(filename, 'r')
    state = 'start'
    count = 0
    for line in file:
        if (line.startswith('OBJECTS')):
            state = 'objects'
            continue
        elif (state == 'objects'):
            a,b,c = line.split(' ')
            datas[count][0] = a
            datas[count][1] = b
            datas[count][2] = c
            count = count + 1;
    for i in range(0, 150):
        xs[i] = datas[i][0]
        ys[i] = datas[i][1]
        zs[i] = datas[i][2]

file = open(filename, 'r')
text_box = Text(window)
text_box.grid(row=0, column=0)
text_box.insert(INSERT, file.read())
button_1 = Button(window, text='Step By Step', command=step_by_step)
button_1.grid(row=1, column=2)
button_2 = Button(window, text='Clustering', command=clustering)
button_2.grid(row=1, column=1)
button_3 = Button(window, text='Clustering With Weights', command=clustering_with_weights)
button_3.grid(row=1, column=3)
button_4 = Button(window, text='Step By Step With Weights', command=step_by_step_with_weights)
button_4.grid(row=1, column=4)
button_5 = Button(window, text='Inputs Plot', command=input_plot)
button_5.grid(row=1, column=5)
groups_label = Label(window, text='Groups Number')
groups_label.grid(row=0,column=1)
groups_entry = Entry(window, textvariable=groups_number_string)
groups_entry.grid(row=0, column=2)
check_attribute_0 = Checkbutton(window, text="attr0", variable=attribute_0)
check_attribute_0.grid(row=0, column=3)
check_attribute_1 = Checkbutton(window, text="attr1", variable=attribute_1)
check_attribute_1.grid(row=0, column=4)
check_attribute_2 = Checkbutton(window, text="attr2", variable=attribute_2)
check_attribute_2.grid(row=0, column=5)
text_box.grid(row=2, column=0)

read_file()
mainloop()
