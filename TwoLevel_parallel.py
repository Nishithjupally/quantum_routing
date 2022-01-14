import random
import math
import copy
V = 25
fail = 0
ESP = [4]*25
dist = None
phyGraph = None
virtGraph = None
newDemNum = 20

swaps = 2
replenishment = 1

#Create n Random Demands
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

	return -3


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
        
#floyd algo on physical graph
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
    #resolving the string
    src, des = s1//100, s2//100
    c1, c2 = s1 % 100, s2 % 100
    return [src,des,c1,c2,demand]

#function resolves a list of raw demands
def resolveSet(demands):
    result = []
    for dem in demands:
        temp = resolve(dem[0],dem[1],dem[2])
        src = temp[0]
        #path array
        temp.append([src])
        #timestep of completion
        temp.append(0)
        result.append(temp)
    return result



#N = Number of Demands
def DM2(N):
    #paths array for building paths 

    #Each item would have 0-src, 1-des, 2-child_src, 3-child_src
    #4-demand. 5(or -2)-path, 6-timestep of completion(default 0)
    paths = []
    #Completed paths(global)
    completedPaths = []
    #Requests which loop(special case)
    incompletePaths = []
    #requests for whic replenishment is left
    replenishmentSet = []

    DemandsSoFar = 0
    timeStep = 1
    ExtraEntanglementSwaps = 0

    #add initial requests
    #generate random number
    num = random.randint(1, newDemNum)
    newDemands = createDemands(num)
    DemandsSoFar+=num
    #resolve string addressing
    newDemands = resolveSet(newDemands)
    #Add to paths array
    paths.extend(newDemands)


    print(paths)
    #Loops till any request left to serve completely
    #or till replenishment of request's path is left
    while(len(paths)) or len(replenishmentSet):
        #shuffle the paths list
        random.shuffle(paths)
        #arrays to store completed or incomplete(loop)
        #requests which are completed in this timestep
        #later merged into global array
        complete = []
        loop = []
        #go through requests one by one
        for req in paths:
            #req[-2] is path built so far
            #src is the last node in the path
            src = req[-2][-1]
            #des is req[1], the actual destination
            des = req[1]
            #number of links needed
            demand = req[4]
            #compute next hop
            nextHop = findpathLB_Mod(src,des,demand,dist,virtGraph,req[-2])
            
            #this indicates that destination is reached
            if nextHop == -3:
                #append des to the path
                req[-2].append(des)
                #compute extra generations swaps needed
                if virtGraph[src][des] < demand:
                    ExtraEntanglementSwaps += math.ceil(math.log((dist[src][des])))*(demand-virtGraph[src][des])

                #update virtual graph
                virtGraph[src][des] -= demand
                virtGraph[src][des] = max(0,virtGraph[src][des])
                virtGraph[des][src] -= demand
                virtGraph[des][src] = max(0,virtGraph[des][src])
                #update the time step of completion of the request 
                req[-1] = timeStep
                #add to complete array
                complete.append(req)

            #next node which is not destination
            elif nextHop!=-2:
                #appending next hop to the path (req[-2])
                req[-2].append(nextHop)

                #compute extra generations swaps needed
                if virtGraph[src][nextHop] < demand:
                    ExtraEntanglementSwaps += math.ceil(math.log((dist[src][nextHop])))*(demand-virtGraph[src][nextHop])

                #update virtual graph
                virtGraph[src][nextHop] -= demand
                virtGraph[src][nextHop] = max(0,virtGraph[src][nextHop])
                virtGraph[nextHop][src] -= demand
                virtGraph[nextHop][src] = max(0,virtGraph[nextHop][src])
            #loop condition (add it to incomplete array)
            elif nextHop==-2:
                req[-2].append(nextHop)
                req[-1] = -1
                loop.append(req)
        print("removed at {} {}".format(timeStep,len(complete)+len(loop)))

        #remove completed paths from paths array
        for req in complete:
            paths.remove(req)
        #add freshly completed requests to replenishmentSet
        replenishmentSet.extend(complete)

        #remove looped requests from paths array
        for req in loop:
            paths.remove(req)
        #add to global array
        incompletePaths.extend(loop)

        #replenishment
        removed = []
        #if its time for replenishment
        for item in replenishmentSet:
            #if its time to replenish
            if item[-1] + (replenishment+swaps) == timeStep:
                #go through the path
                for i in range(len(item[-2])-1):
                    #select adjacent nodes
                    u,v = item[-2][i], item[-2][i+1]
                    #add demand number of links to the virtGraph
                    virtGraph[u][v] += item[4]
                    virtGraph[v][u] += item[4]
                removed.append(item)
        #remove the replenished requests from replenishmentSet
        #add it to global completedPaths
        for item in removed:
            completedPaths.append(item)
            replenishmentSet.remove(item)

        #Add new demands if still left
        if DemandsSoFar<N:
            num = random.randint(1, newDemNum)
            newDemands = createDemands(min(num,N-DemandsSoFar))
            DemandsSoFar+=min(num,N-DemandsSoFar)
            newDemands = resolveSet(newDemands)
            paths.extend(newDemands)
            print("added at {} {}".format(timeStep,min(num,N-DemandsSoFar)))
        
        timeStep+=1
    # print("-"*25)
    # print(virtGraph)
    # print("{} {}".format(N,swaps))
    print(len(completedPaths))


#read graphs
phyGraph = readGraph('./phygraph.txt')
dist = readGraph("./phygraph.txt")
virtGraph = readGraph("./virtgraph.txt")
floyd(dist)
for i in range(25):
    for j in range(25):
        virtGraph[i][j] += phyGraph[i][j]//10

print("Enter the number demands:")
numberofdemands = int(input())
DM2(numberofdemands)
