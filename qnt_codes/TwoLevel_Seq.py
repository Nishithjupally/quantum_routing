import random
V = 25
fail = 0
ESP = [4]*25

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
        #to make the string length as 4
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
        demands.append([a, b, item])
    return demands

#Path finding algorithms

#Modified greedy algorithm
def findpathMG(src, des, demand, dist, virtGraph):
	uc=src
	result = [uc]
	st = {src}
	while uc != des:
		d = 1e9
		u = -1
		for i in range(V):
			if i not in st and (virtGraph[uc][i] > 0 or dist[i][uc] == 100) and d>dist[i][des]:
				u = i
				d = dist[i][des]
		if virtGraph[u][uc] < demand and dist[uc][u] + dist[u][des] > dist[uc][des] :
			d=1e9
			for i in range(V):
				if i not in st and dist[i][uc] == 100 and d > dist[i][dest]:
					u = i
					d = dist[i][des]
		result.append(u)
		st.add(u)
		uc = u

	return result

#local best algorithm
def findpathLB(src, des, demand, dist, virtGraph):
    uc, count = src, 0
    result = [uc]
    st = {src}
    while uc != des:
        temp = uc
        d, u = 1e9, -1
        for i in range(V):
            if i not in st and virtGraph[i][uc] >= demand and d > dist[i][des]:
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
            fail = 1
            break
    return result

# modified local best algorithm
def findpathLB_Mod(src, des, demand, dist, virtGraph):
    uc, count = src, 0
    result = [uc]
    st = {src}
    while uc != des:
        temp = uc
        d, u = 1e9, -1
        for i in range(V):
            if i not in st and virtGraph[i][uc] >= demand and d > dist[i][des]:
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
            fail = 1
            break
    return result

#floyd algo on physical graph
def floyd(phyGraph, dist):
    for i in range(V):
        for j in range(V):
            dist[i][j] = phyGraph[i][j]
            if dist[i][j] == 0 and i != j:
                dist[i][j] = 2000
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k]+dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k]+dist[k][j]


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

#Sequential execution 
def DM(demands,n):
    destinations = {}
    paths = []
    for i in range(0,len(demands)):
        request = resolve(demands[i][0], demands[i][1], demands[i][2])
        destinations[i] = request[1]
        paths.append([request[0]])
    while len(paths):
        order = [i for i in range(0,n)]
        random.shuffle(order)
        for j in range(0,len(order)):
            pass




phyGraph = readGraph('./phygraph.txt')
virtGraph = readGraph("./virtgraph.txt")
for i in range(25):
    for j in range(25):
        virtGraph[i][j] += phyGraph[i][j]//10
dist = [[0]*25]*25
floyd(phyGraph, dist)
demands = createDemands(10)
print(demands)
# for item in demands:
#     resolve(item[0], item[1], item[2])
res = findpathLB(2, 5, 1, dist, virtGraph)
print(res)
res = findpathMG(2, 5, 1, dist, virtGraph)
print(res)
res = findpathLB_Mod(2, 5, 1, dist, virtGraph)
print(res)


