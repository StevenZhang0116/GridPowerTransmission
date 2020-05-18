import networkx as nx
import random
import itertools
import numpy as np
from scipy.optimize import fsolve

print("----------------------The following are Premises------------------------------")
g_side = 10

def read_int(prompt):
    while True:
        ret = int(input(prompt))
        if ret <=0:
            print("The input is not valid")
        else:
            break
    return ret
    
police_count = read_int("How many policemen do you want: ")
velocity = read_int("What is the speed of the policemen: ")
locations_count = read_int("How many criminal locations are allocated in that region: ")

print("----------------------Program Starts---------------------------------------\n")
    
random_n_list = list(itertools.product(range(0, g_side), range(0, g_side)))
locations_set = random.sample(random_n_list, locations_count+1)
g_los = locations_set

po = g_los[0]

G=nx.grid_2d_graph(g_side,g_side)

g_cri_set = [random.randint(3,10) for _ in range(locations_count)]
#print(g_cri_set)

list2 = []
for index in range(0,len(g_los)):
    list2.append(index)

posiList = dict(zip(list2,g_los))
#print(pos2)

def func(X):
    
    ret = 0
    clen = len(g_cri_set)
    
    for index in range(0,clen):
        y = (g_cri_set[index]**2)*(X[index])**-1
        ret = ret + y
        
    ret = ret + X[-1]*(np.sum(X[0:clen]) - police_count)

    return ret

gLambda = []


def dfunc(X):
    global gLambda
    dLambda = np.zeros(len(X))
    h = 1e-4 # step size used in the finite differences
    for i in range(len(X)):
        dX = np.zeros(len(X))
        dX[i] = h
        dLambda[i] = (func(X + dX) - func(X - dX))/(2*h)

    #print(f'X:{X}')
    #print(f'R:{dLambda}')
    gLambda = dLambda
    return dLambda

#print('The distribution of criminals are:',g_cri_set)

pas = np.ones(len(g_cri_set))
#print(pas)
pas[0] = 101-len(g_cri_set)
pas = np.append(pas,0)
X2 = fsolve(dfunc, pas)

X2=np.round(X2[0:-1])
#print('The distribution of policemen:',X2)

dist_location_criminals = dict(zip(g_los[1:],g_cri_set))
dist_location_policemen = dict(zip(g_los[1:], X2))

print(f"dist_location_criminals:{dist_location_criminals}")
print(f"dist_location_policemen:{dist_location_policemen}")

time_list = []
cost_list = []

for index in range(1,len(g_los)):
    path = nx.dijkstra_path(G, source = g_los[0], target = g_los[index])
    #print(f"The path for Criminal Place {index}")
    #print(path)
    length = nx.dijkstra_path_length(G, source = g_los[0], target = g_los[index])
    #print(length)
    time = length + (g_cri_set[index-1])**2*(X2[index-1])**-1
    time = round(time, 3)
    cost = 2 * length / velocity + (g_cri_set[index-1])**2*(X2[index-1])**-1
    cost = round(cost, 3)
    time_list.append(time)
    cost_list.append(cost)

time_distribution = dict(zip(g_los[1:],time_list))
unsorted_time_distribution = time_distribution
unchanged_time_distribution = time_distribution

print(f"time_distribution:{time_distribution}")

total_dist = 0

for index in range(1,len(g_los)):
    to = g_los[index]
    dist = nx.dijkstra_path_length(G,po,to)
    total_dist = total_dist + dist
print(f"the total distance is:{total_dist}")

total_min_cost = 0
for index in range(1,len(X2)):
    min_cost = g_cri_set[index-1]**2/X2[index-1]
    total_min_cost = total_min_cost + min_cost

total_min_cost = total_min_cost + total_dist

print(f"total_min_cost:{total_min_cost}\n\n")

calc_result = []
min_cost = -9999999999999
min_transformation_police_set = None

def remove_key(dic, key):
    del dic[key]
    return dic

def calc_police(ma,sindex,max1, list1, list2, list3, list4, t1):
    
    ov = ma[sindex]
            
    for n in range(0,int(max1)+1):
        ma[sindex]=n
        sa = sum(ma)
        #print(f"ma:{ma} sa:{sa}")
        if sa > max1:
            break
        if sa == max1:
            calc_gain(ma, list1, list2, list3, list4, t1)

        for i in range(sindex+1,len(ma)):
            calc_police(ma,i,max1, list1, list2, list3, list4, t1)
        
    ma[sindex] = ov

def calc_gain(ma, list1, list2, list3, list4, t1):
    global min_cost
    global min_transformation_police_set
    
    least_cost = 0
    for i in range(0, len(list1)-1):
        least_cost = least_cost 
        + np.square((list3[i]-t1-list4[i])/list3[i]*list2[i])/list1[i] 
        - np.square((list3[i]-t1-list4[i])/list3[i]*list2[i])/(list1[i]+ma[i])
    #print(f"least_cost:{least_cost}")
    calc_result.append(least_cost)
    if least_cost > min_cost:
        min_cost = least_cost
        min_transformation_police_set = np.array(ma)
    #print(f"min_transformation_police_set:{min_transformation_police_set}")

all_destination = []
for key in unsorted_time_distribution.keys():
    all_destination.append(key)
    
#print(f"all_destination:{all_destination}")

def transformation(place):

    global velocity
    global destination_set
    global total_min_cost
    global all_destination
    
    time_distribution = sorted(unsorted_time_distribution.items(), key=lambda obj: obj[1])
    #print(time_distribution)
    
    travel_time = {}
    source = time_distribution[place][0]

    starting_time = unsorted_time_distribution[source]
    

        
    print(f"all_destination:{all_destination}")

    for index in range(place+1,len(time_distribution)):
        d = nx.dijkstra_path_length(G,source,target = time_distribution[index][0]) 
        time = d/velocity
        travel_time[time_distribution[index][0]] = time
            
    print("The starting point is at "+str(source))
    
    if len(all_destination) >= 1:
       all_destination.remove(source)
    
    unsorted_travel_time = travel_time
    #print(f"unsorted_travel_time:{unsorted_travel_time}")
    
    travel_time = sorted(travel_time.items(), key=lambda obj: obj[1])
    #print(unsorted_travel_time)
    
    location = []
    for t in range(0,len(travel_time)):
        location.append(travel_time[t][0])
    #print(f"location:{location}")
    
    deltatime = []
    for index in range(place+1, len(time_distribution)):
        deltat = time_distribution[index][1] - time_distribution[place][1]
        deltatime.append(deltat)
    #print(f"deltatime:{deltatime}")
    
    time_worth = []
    for index in range(0,len(time_distribution)-place-1):
        worth = travel_time[index][1]/deltatime[index]
        time_worth.append(worth)
    
    travel_worth = dict(zip(location, time_worth))
    #travel_worth = sorted(travel_worth.items(),key=lambda obj:obj[1])
    #print(f"travel_worth:{travel_worth}")
    time_worth_selection = {k:v for k, v in travel_worth.items() if 0<v<1}
    #print(f"time_worth_selection:{time_worth_selection}")
    
    if len(time_worth_selection) == 0:
        print("Transformation is not needed. \n")
        
    else:
        time_worth_key = []
        location_police = []
        location_criminal = []
        location_time = []
        travel_time_selection = []
        for key in time_worth_selection.keys():
            time_worth_key.append(key)
            location_police.append(dist_location_policemen[key])
            location_criminal.append(dist_location_criminals[key])
            location_time.append(unsorted_time_distribution[key])
            travel_time_selection.append(unsorted_travel_time[key])
         
        #print(type(time_worth_key))
        
        for key in time_worth_key:
            if dist_location_criminals[key] == 0:
                time_worth_key.remove(key)
                
        print(f"time_worth_key:{time_worth_key}")
        #print(location_police)
        #print(location_criminal)
        #print(location_time)
        #print(travel_time_selection)
    
        dist_location_travel_time = dict(zip(time_worth_key,travel_time_selection))
        #print(f"dist_location_travel_time:{dist_location_travel_time}")
        
        transform_police_set = [0 for i in range(len(time_worth_key))]
    
        transform_sum = dist_location_policemen[source]
        print(f"transform_sum:{transform_sum}")
        
        calc_police(transform_police_set, 0, transform_sum, location_police, 
        location_criminal, location_time, travel_time_selection, starting_time)
        print(f"min_transformation_police_set:{min_transformation_police_set}")
        print(f"max_gain:{min_cost}")
        
        total_min_cost = total_min_cost - min_cost
        
        transform_location_police = dict(zip(time_worth_key, min_transformation_police_set))
        for i in transform_location_police.keys():
            dist_location_policemen[i] = dist_location_policemen[i] 
            + transform_location_police[i]
        dist_location_policemen[source] = 0.0
        print(f"updated distribution of policemen:{dist_location_policemen}")
        
        next_source = time_distribution[place+1][0]
        next_starting_time = unsorted_time_distribution[next_source]
        
        print(f"next_starting_time:{next_starting_time}")
    
        for i in time_worth_key:
            if starting_time + dist_location_travel_time[i] < next_starting_time:
                dist_location_criminals[i] = dist_location_criminals[i]
                - (starting_time + dist_location_travel_time[i]) 
                * dist_location_criminals[i] / unsorted_time_distribution[i]
                - (next_starting_time - (starting_time + dist_location_travel_time[i])) 
                * (dist_location_policemen[i]) / (dist_location_criminals[i] 
                - (starting_time + dist_location_travel_time[i]) 
                * dist_location_criminals[i] / unsorted_time_distribution[i])
            else:
                dist_location_criminals[i] = dist_location_criminals[i] 
                - (next_starting_time - starting_time) 
                * dist_location_policemen[i] / dist_location_criminals[i]
        
        retD = list(set(all_destination).difference(set(time_worth_key)))
        
        for i in retD:
            dist_location_criminals[i] = dist_location_criminals[i] 
            - next_starting_time / unsorted_time_distribution[i] 
            * dist_location_criminals[i]
        
        dist_location_criminals[source] = 0
        
        for i in time_worth_key:
            if dist_location_criminals[i] < 0:
                dist_location_criminals[i] = 0
        
        print(f"updated distribution of criminals:{dist_location_criminals}")
                
        for i in time_worth_key:
            t1 = (dist_location_criminals[i])**2 / (dist_location_policemen[i])
            unsorted_time_distribution[i] = t1
        
        unsorted_time_distribution[source] = 0
        
        print(f"updated distribution of time: {unsorted_time_distribution}\n")
        
if __name__ == "__main__":
    for i in range(0, locations_count - 1):
        transformation(i)
        i += 1
    
print(f"The final total cost is: {total_min_cost}")