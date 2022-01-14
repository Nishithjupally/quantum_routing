import random
import math
import copy
V = 25
fail = 0
ESP = [4]*25
dist = None
phyGraph = None
virtGraph = None


#Create Random Demands
def createDemands(n):
    nums = []
    demands = []
    for i in range(n):
        nums.append(random.randint(1, 10))
    for item in nums:
        #select random parents
        a = random.randint(0, 24)
        b = random.randint(0, 24)
        #select random children
        c = random.randint(0, ESP[a]-1)
        d = random.randint(0, ESP[b]-1)
        a, b, c, d = str(a), str(b), str(c), str(d)
        if len(a) == 1:
            a = '0'+a
        if len(b) == 1:
            b = '0'+b
        if len(c) == 1:
            c = '0'+c
        if len(d) == 1:
            d = '0'+d
        a += c
        b += d
        demands.append([a, b, 1])
    return demands

#Path finding algorithms

def findpathMG(src, des, demand, dist, virtGraph):
	uc=src
	result = [uc]
	st = {src}
	if uc != des:
		d = 1e9
		u = -1
		for i in range(V):
			if i not in st and (virtGraph[uc][i] > 0 or dist[i][uc] == 100) and d>dist[i][des]:
				u = i
				d = dist[i][des]
		if virtGraph[u][uc] < demand and dist[uc][u] + dist[u][des] > dist[uc][des] :
			d=1e9
			for i in range(V):
				if i not in st and dist[i][uc] == 100 and d > dist[i][des]:
					u = i
					d = dist[i][des]
		result.append(u)
		st.add(u)
		return u

	return -1

# def findpathLB(src, des, demand, dist, virtGraph):
#     uc, count = src, 0
#     result = [uc]
#     st = {src}
#     while uc != des:
#         temp = uc
#         d, u = 1e9, -1
#         for i in range(V):
#             if i not in st and virtGraph[i][uc] >= demand and d > dist[i][des]:
#                 u = i
#                 d = dist[i][des]
#         if u == -1 or dist[uc][des] > dist[u][des]:
#             d = 1e9
#             for i in range(V):
#                 if virtGraph[uc][i] >= 0 and dist[i][uc] == 100 and d > dist[i][des]:
#                     u = i
#                     d = dist[i][des]    
#         result.append(u)
#         st.add(u)
#         uc = u
#         if temp == uc:
#             count += 1
#         else:
#             count = 0
#         if count > 25:
#             fail = 1
#             break
#     return result

def findpathLB(src, des, demand, dist, virtGraph,path):
    uc, count = src, 0
    result = [uc]
    st = {src}
    temp = uc
    while uc == temp:
        d, u = 1e9, -1
        for i in range(V):
            if i not in st and i not in path and virtGraph[i][uc] >= demand and d > dist[i][des]:
                u = i
                d = dist[i][des]
        if u == -1 or dist[uc][des] > dist[u][des]:
            d = 1e9
            for i in range(V):
                if virtGraph[uc][i] >= 0 and dist[i][uc] == 100 and d > dist[i][des]:
                    u = i
                    d = dist[i][des]
        result.append(u)
        st.add(u)
        uc = u
        if temp == uc:
            count += 1
        else:
            count = 0
        if count > 25:
            return -2
    if uc==des:
        return -3
    return uc

def findpathLB_Mod(src, des, demand, dist, virtGraph,path):
    uc, count = src, 0
    result = [uc]
    st = {src}
    temp = uc
    while uc == temp:
        d, u = 1e9, -1
        for i in range(V):
            if i not in st and i not in path and virtGraph[i][uc] >= demand and d > dist[i][des]:
                u = i
                d = dist[i][des]
        if u == -1 or dist[uc][des] < dist[u][des]:
            d = 1e9
            for i in range(V):
                if virtGraph[uc][i] >= 0 and dist[i][uc] == 100 and d > dist[i][des]:
                    u = i
                    d = dist[i][des]
        result.append(u)
        st.add(u)
        uc = u
        if temp == uc:
            count += 1
        else:
            count = 0
        if count > 25:
            return -2
    if uc==des:
        return -3
    return uc
        

def floyd(dist):
    for i in range(0,V):
        for j in range(0,V):
            if dist[i][j] == 0 and i != j:
                dist[i][j] = 2000
    for k in range(0,V):
        for i in range(0,V):
            for j in range(0,V):
                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j]
                                 )

#Reading graphs from file input
def readGraph(s):
    graph = []

    f = open(s, 'r')
    lines = f.readlines()
    for line in lines:
        temp = list(line.split(", "))
        temp[-1] = temp[-1].replace("\n", "")
        temp = list(map(int, temp))
        graph.append(temp)
    return graph

# s -> "1204" 12th ESP, 4th child
def resolve(s1, s2, demand):
    s1 = int(s1)
    s2 = int(s2)
    src, des = s1//100, s2//100
    c1, c2 = s1 % 100, s2 % 100
    return [src,des,c1,c2,demand]
    # call path detection here

def DM(demands):
    n = len(demands)
    destinations = []
    links = []
    incompletePaths = []
    paths = []
    completedPaths = [0]*n
    for i in range(0,len(demands)):
        request = resolve(demands[i][0], demands[i][1], demands[i][2])
        destinations.append(request[1])
        links.append(request[-1])
        paths.append([request[0]])
    completed = False
    count = 0
    swaps = 0
    generations = 0
    while not completed:
        order = [i for i in range(0,n)]
        random.shuffle(order)
        sources = []
        # count+=1
        # if count==100:
        #     break
        for j in range(0,len(order)):
            # print("here")
            if not completedPaths[order[j]]:
                src = paths[order[j]][-1]
                if src in sources:
                    continue    
                sources.append(src)
                des = destinations[order[j]]
                demand = links[order[j]]
                nextHop = findpathLB(src,des,demand,dist,virtGraph,paths[order[j]])
                # print(nextHop)
                if nextHop == -3:
                    completedPaths[order[j]] = 1
                    paths[order[j]].append(des)
                    if virtGraph[src][des] <demand:
                        swaps += math.ceil(math.log((dist[src][des])))*(demand-virtGraph[src][des])
                        generations += demand-virtGraph[src][des]
                    virtGraph[src][des] -= demand
                    virtGraph[src][des] = max(0,virtGraph[src][des])
                    virtGraph[des][src] -= demand
                    virtGraph[des][src] = max(0,virtGraph[des][src])
                else:
                    paths[order[j]].append(nextHop)
                    if virtGraph[src][nextHop] <demand:
                        swaps += math.ceil(math.log(dist[src][nextHop]))*(demand-virtGraph[src][nextHop])
                        generations += demand-virtGraph[src][nextHop]
                    virtGraph[src][nextHop] -= demand
                    virtGraph[src][nextHop] = max(0,virtGraph[src][nextHop])
                    virtGraph[nextHop][src] -= demand
                    virtGraph[nextHop][src] = max(0,virtGraph[nextHop][src])
                if nextHop == -2:
                    completedPaths[order[j]] = 2
                    paths[order[j]].append(-2)
                    incompletePaths.append(order[j])
        completed = all(completedPaths)
    # print(paths)
    # print(completedPaths)
    print(str(swaps)+"\t"+str(generations))

phyGraph = readGraph('./phygraph.txt')
dist = readGraph("./phygraph.txt")
virtGraph = readGraph("./virtgraph.txt")
floyd(dist)
for i in range(25):
    for j in range(25):
        virtGraph[i][j] += phyGraph[i][j]//10
demands = createDemands(10)
CloneGraph = copy.deepcopy(virtGraph)
for i in range(100,501):
    demands = createDemands(i)
    virtGraph = copy.deepcopy(CloneGraph)
    DM(demands)
    
