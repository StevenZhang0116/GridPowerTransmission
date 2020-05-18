nx.draw_networkx_nodes(G, posiList, nodelist = [t for t in range(1, len(g_los))], 
node_color = "y")
nx.draw_networkx_nodes(G, posiList, nodelist = [0], 
node_color = "b")

for (u,v,w) in G.edges(data=True):
    w['weight'] = random.randint(1,10)

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9',
    'A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

dist = []

for index in range(1,len(g_los)):
    
    path = nx.dijkstra_path(G, source = g_los[0], target = g_los[index])
    #print(f"The path for Criminal Place {index}")
    #print(path)
    length = nx.dijkstra_path_length(G, source = g_los[0], target = g_los[index])
    #print(length)
    cost = length + (g_cri_set[index-1])**2*(X2[index-1])**-1
    cost = round(cost, 3)
    dist.append(cost)
    
    path_edges = zip(path,path[1:])
    path_edges = set(path_edges)
    colors = []
    for a in range(1,len(g_los)):
        sval = '{c}'.format(c=randomcolor())
        colors.append(sval)
    nx.draw_networkx_edges(G,pos,edgelist=path_edges,
    edge_color=colors[index-1],width=3)
    plt.axis('equal')

distribution = dict(zip(g_los[1:],dist))