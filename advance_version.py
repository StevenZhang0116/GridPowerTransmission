
import numpy as np
import pandas as pd
import networkx as nx
import itertools
import random
import re
import matplotlib.pyplot as plt


g_side = 10
locations_count = 6
cost = 700
gain = 100
refill = 200
v_low = 30
v_high = 50

times = 1000

random_n_list = list(itertools.product(range(0, g_side), range(0, g_side)))
locations_set = random.sample(random_n_list, locations_count+1)
g_los = locations_set

po = g_los[0]


G = nx.grid_2d_graph(g_side,g_side)
pos = dict( (n, n) for n in G.nodes() )
labels = dict( ((i, j), i * 0 + j * 0) for i, j in G.nodes() )
nx.draw_networkx(G, pos=pos, labels = labels, node_color = "r", node_size = 0)

list2 = []
for index in range(0,len(g_los)):
    list2.append(index)
    
    
posiList = dict(zip(list2,g_los))
#print(posiList)

g_overload_set = [random.randint(v_low,v_high) for _ in range(locations_count)]
location_overload_set = dict(zip(g_los[1:], g_overload_set))


nx.draw_networkx_nodes(G, posiList, nodelist = [t for t in range(1, len(g_los))], 
node_color = "y")
nx.draw_networkx_nodes(G, posiList, nodelist = [0], node_color = "b")

broke_num = 0

for (u,v,w) in G.edges(data=True):
    w['weight'] = random.randint(1,10)
    
    #设置断路
    if w["weight"] == 10:
        w["weight"] = 999999
        broke_num += 1


length_matrix = np.zeros(locations_count+1)



for x in range (0,len(g_los)):
    length_list = []
    for index in range(0,len(g_los)):
        length = nx.dijkstra_path_length(G, source = g_los[x], target = g_los[index])
        length_list.append(length)
    length_list = np.mat(length_list)
    #print(length_list)
    
    length_matrix = np.vstack((length_matrix, length_list))

length_matrix = np.delete(length_matrix, 0, 0)
# print(f"The Shortest Distance from the starter 
# to different locations are:{length_matrix[0]}")
length_matrix_set = pd.DataFrame(length_matrix)
length_matrix_set = length_matrix_set / 60
print(length_matrix_set)

time_needed = []
for index in range(1, len(g_los)):
    time0 = nx.dijkstra_path_length(G, source = g_los[0], target = g_los[index])
    time_needed.append(time0)
time_needed = np.array(time_needed) / 60

location_time_set = dict(zip(g_los[1:], time_needed))


length_matrix = length_matrix - np.ones([locations_count+1, locations_count+1])

path_dict = {}

_=inf=999999
 
def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]



def Dijkstra_all_minpath(start,matrix):
    global path_dict
    length=len(matrix)
    path_array=[]
    temp_array=[]
    path_array.extend(matrix[start])
    temp_array.extend(matrix[start])
    temp_array[start] = inf
    already_traversal=[start]
    path_parent=[start]*length
    while(len(already_traversal)<length):
        i= temp_array.index(min(temp_array))
        temp_array[i]=inf
        path=[]
        path.append(str(i))
        k=i
        while(path_parent[k]!=start):
            path.append(str(path_parent[k]))
            k=path_parent[k]
        path.append(str(start))
        path.reverse()
        path_dict[int(i)] = ",".join(path)
        #print(str(i)+':','->'.join(path))
        already_traversal.append(i)
        for j in range(length):
            if j not in already_traversal:
                if (path_array[i]+matrix[i][j])<path_array[j]:
                    path_array[j] = temp_array[j] =path_array[i]+matrix[i][j]
                    path_parent[j]=i
    return path_dict



adjacency_matrix=length_matrix.tolist()
print(Dijkstra_all_minpath(0,adjacency_matrix))

lengths = list(path_dict.values())
lengths.sort(key = lambda i:len(i),reverse=True)

lengths_numbers = []
for i in range(0,len(lengths)):
    lengths_numbers.append(re.findall(r"\d+\.?\d*",lengths[i]))

all_numbers = []
for i in range(0,len(lengths_numbers)):
    for x in range(0,len(lengths_numbers[i])):
        all_numbers.append(lengths_numbers[i][x])

cars = 0
paths = []
for i in all_numbers:
    if all_numbers.count(i) == 1:
        cars +=1
        for x in range(0, len(lengths)):
            if i in lengths_numbers[x]:
                paths.append(lengths_numbers[x])
                
                
for x in range(len(paths)):
    for i in paths[x]:
        for t in range(x+1,len(paths)):
            if i in paths[t]:
                if int(i)>0:
                    paths[t].remove(i)

print(f"{cars} cars are needed! ")

cost_all = []
for i in range(0,len(paths)):
    cost = length_matrix_set.iat[0,int(paths[i][-1])]
    print(f"The path for the {i+1}st car is {paths[i]}, the needed time is {cost}")
    cost_all.append(cost)
    
#print(f"cost_all:{cost_all}")
    
    
elarge = [(u,v) for (u,v,w) in G.edges(data=True) if w["weight"] > 10]
esmall = [(u,v) for (u,v,w) in G.edges(data=True) if w["weight"] < 10]
nx.draw_networkx_edges(G,pos,edgelist=elarge,width=6,alpha=0.5,
edge_color='b',style='solid')
nx.draw_networkx_edges(G,pos,edgelist=esmall,width=6,alpha=0.5,
edge_color='g',style='dotted')

#print(f"The number of broke roads are {broke_num}\n")

plt.show()

print(f"location_overload_set:{location_overload_set}")

index_set = {}
for i in range (1, len(g_los)):
    index_set[i] = g_los[i]
#print(f"index_set:{index_set}")
    
    
for x in range(len(paths)):
    for i in paths[x]:
        if int(i) > 0:
            dest = int(paths[x][-1])
            location_time_set[index_set[int(i)]] = location_time_set[index_set[dest]]
        else:
            continue

print(f"location_time_set:{location_time_set}")
print(f"paths:{paths}\n")


dist_battery = []

for x in g_los[1:]:
    init_battery = 2 * location_time_set[x] * location_overload_set[x]
    dist_battery.append(init_battery)

dist_battery = pd.DataFrame(dist_battery, index = g_los[1:], columns = [1]).T

initial_values = dist_battery.values.tolist()



def battery_transform(dist):
    sum0 = np.zeros(len(paths))
    for x in range(len(paths)):
        for i in paths[x]:
            if int(i) > 0: 
                los = index_set[int(i)]
                sum0[x] += dist[los]
            else:
                continue
        
    
    for x in range(len(paths)):
        for i in paths[x]:
            if int(i) > 0:
                los = index_set[int(i)]
                dist[los] = (2 * location_time_set[los] 
                + sum0[x] / refill) * location_overload_set[los]

    return dist

total_battery = np.zeros(len(g_los)-1)



index0 = []
for i in range (1,times):
    index0.append(i)
 
for i in range(2,times):
    battery_transform(dist_battery)
    total_battery = np.vstack((total_battery, dist_battery))
    i += 1

total_battery = np.delete(total_battery,0,0)
total_battery = np.mat(total_battery)

a = np.array(initial_values)
total_battery = np.r_[a, total_battery]
total_battery = pd.DataFrame(total_battery, columns = g_los[1:], index = index0)
print(total_battery)

total_sum = np.sum(total_battery, axis = 1)
#print(total_sum)

plt.plot(total_sum)
plt.show()


for x in location_time_set.values():
    x_multiples = []
    for i in range(0,50):
        x_multiples.append(2*x*i)
    plt.scatter(x_multiples,np.zeros(len(x_multiples)))
    plt.axis([0,2,-0.005,0.005])

plt.show()

all_multiples = pd.DataFrame()




for x in location_time_set.keys():
    t = location_time_set[x]
    t_multiples = []
    for i in range(0,times):
        t_multiples.append(2*i*t)
    all_multiples[x] = t_multiples


all_multiples = pd.DataFrame(all_multiples, index = [i for i in range(1, times)])

#print(f"all_multiples:{all_multiples}")
#print(np.array(all_multiples)[1])


x_multiples = []
for x in cost_all:
    for i in range(1,times):
        x_multiples.append(2*x*i)
result = x_multiples.sort()

#print(f"x_multiples:{x_multiples}")
#print(len(x_multiples))


#data1为total_battery, list0为all_locations, value0与find_location中的参数一致，
#value1为value0后的一个参数（在x_multiples中）
def find_remaining(data,list0, value0, value1):
    global refill
    total_charge = 0
    for location in list0:
        charge = data.iat[location[0],location[1]]
        total_charge += charge
    remain_charge = total_charge - (value1 - value0) * refill
    if remain_charge<0:
        remain_charge = 0
    remaining_battery.append(remain_charge)
    return remain_charge
 
all_location_set = []
#data0为all_multiples, value0为x_multiples中不同位置的值
def find_location_remaining(data0, data1, value0, value1):
    all_locations = []
    for x in range(times-1):
        for y in range(locations_count):
            if value0 == data0.iat[x,y]:
                t = [x,y]
                all_locations.append(t)
    find_remaining(data1, all_locations, value0, value1)
    all_location_set.append(all_locations)
    

remaining_battery = []
for i in range(0, len(x_multiples)-1):
    find_location_remaining(all_multiples, total_battery, x_multiples[i], x_multiples[i+1])

#print(f"remaining_battery:{remaining_battery}")
#print(f"all_location_set:{all_location_set}")
#print(len(remaining_battery))
#print(len(all_location_set))

shape = (times-1, locations_count)
remaining_battery_set = pd.DataFrame(np.zeros(shape))
#print(remaining_battery_set)

for x in range(len(all_location_set)):
    for i in range(len(all_location_set[x])):
        remaining_battery_set.iloc[all_location_set[x][i][0], 
        all_location_set[x][i][1]] = remaining_battery[x] 

remaining_battery_set = pd.DataFrame(remaining_battery_set, 
index = [i for i in range(1, times)])
print(remaining_battery_set)


df3 = pd.DataFrame(np.zeros(shape))

for x in range(times-1):
    for y in range(locations_count):
        df3.iloc[x,y] = total_battery.iloc[x,y] 
        * (1 + remaining_battery_set.iloc[x,y] / refill)
df3 = pd.DataFrame(df3, index = [i for i in range(1, times)])
print(df3)

total_sum2 = np.sum(df3, axis = 1)
plt.plot(total_sum2)
plt.show()


total_sum2 = np.array(total_sum2)

sum_selection = []
for x in range(len(total_sum2)-1):
    sum1 = total_sum2[x] + total_sum2[x+1]
    sum_selection.append(sum1)
print(np.max(sum_selection))



