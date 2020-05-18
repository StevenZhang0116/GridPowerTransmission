def transformation(place):
    global distribution
    global velocity
    global destination_set
    global total_min_cost
    
    travel_time = {}
    source = distribution[place][0]
    
    for index in range(place+1,len(distribution)):
        d = nx.dijkstra_path_length(G,source,target = distribution[index][0]) 
        time = d/velocity
        travel_time[distribution[index][0]] = time
    print("The starting point is at "+str(distribution[place][0]))
    
    unsorted_travel_time = travel_time
    travel_time = sorted(travel_time.items(), key=lambda obj: obj[1])
    #print(unsorted_travel_time)
    
    location = []
    for t in range(0,len(travel_time)):
        location.append(travel_time[t][0])
    #print(f"location:{location}")
    
    deltatime = []
    for index in range(place+1, len(distribution)):
        deltat = distribution[index][1] - distribution[place][1]
        deltatime.append(deltat)
    #print(f"deltatime:{deltatime}")
    
    time_worth = []
    for index in range(0,len(distribution)-place-1):
        worth = travel_time[index][1]/deltatime[index]
        time_worth.append(worth)
    #print(f"time_worth:{time_worth}\n")
    
    travel_worth = dict(zip(location, time_worth))
    #travel_worth = sorted(travel_worth.items(),key=lambda obj:obj[1])
    #print(f"travel_worth:{travel_worth}")
    time_worth_selection = {k:v for k, v in travel_worth.items() if 0<v<1}
    print(f"time_worth_selection:{time_worth_selection}")

    if time_worth_selection:
        secure_places = list(time_worth_selection.keys())
        #secure_crimes = []
        #secure_policemen = []
        overall_evaluation = {}
        for x in range(0, len(secure_places)):
            secure_cri = dist_location_criminals[secure_places[x]]
            source_pol = dist_location_policemen[source]
            secure_pol = dist_location_policemen[secure_places[x]]
            # print(f"unsorted_distribution[secure_places[x]]:
            # {unsorted_distribution[secure_places[x]]}")
            # print(f"unsorted_distribution[source]:
            # {unsorted_distribution[source]}")
            # print(f"unsorted_travel_time[secure_places[x]]:
            # {unsorted_travel_time[secure_places[x]]}")
            # print(f"secure_cri:{secure_cri}")
            
            remain_cri = ((unsorted_distribution[secure_places[x]] 
            - unsorted_distribution[source] - unsorted_travel_time[secure_places[x]])
            /unsorted_distribution[secure_places[x]])*secure_cri
            #print(f"remain_cri:{remain_cri}")
            work_time = (remain_cri**2)/(source_pol + secure_pol)
            saving_cost = abs(1*(unsorted_distribution[secure_places[x]] 
            - unsorted_distribution[source] 
            - unsorted_travel_time[secure_places[x]] - work_time))
            overall_evaluation[secure_places[x]] = saving_cost
            
        print(f"overall_evaluation:{overall_evaluation}")
        
        best_destination = max(overall_evaluation,
        key=lambda x:overall_evaluation[x])
        #print(f"best_destination:{best_destination}")
        
        while best_destination in destination_set: 
            
            print("The location has already been secured. Pick another one\n")
            overall_evaluation = remove_key(overall_evaluation,best_destination)
            print(f"overall_evaluation:{overall_evaluation}")
        
            if not overall_evaluation:
                print("Everything is settled. There is no need to transform\n")
                break
            else:
                best_destination = max(overall_evaluation,
                key=lambda x:overall_evaluation[x])
                print(best_destination)
                continue

        if overall_evaluation:
            saving_cost = overall_evaluation[best_destination]
            total_min_cost = total_min_cost - saving_cost
            #print(f"total_min_cost:{total_min_cost}")
            print(f"the best destination is :{best_destination}")
            print(f"saving cost:{overall_evaluation[best_destination]}\n")
                
            destination_set.append(best_destination)
        
        #print(best_destination)
        #print("The Best Location to secure is: " 
        + get_key(dist_location_work_time, best_destination))
        #print("\n")
        #print(secure_crimes)
        #print(secure_policemen)
    else:
        print("There is no need to transform\n")