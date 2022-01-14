import random
V = 25
fail = 0
ESP = [4]*25


def createDemands(n):
    nums = []
    demands = []
    for i in range(n):
        nums.append(random.randint(1, 10))
    for item in nums:
        a = random.randint(0, 24)
        b = random.randint(0, 24)
        while a == b:
            a = random.randint(0, 24)
            b = random.randint(0, 24)
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
        demands.append([a, b, item])
    return demands


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

# s -> "1204" 12th ESP, 4th child


def request(s1, s2, demand):
    s1 = int(s1)
    s2 = int(s2)
    src, des = s1//100, s2//100
    c1, c2 = s1 % 100, s2 % 100
    print(src, des, c1, c2)
    # call path detection here


phyGraph = readGraph('./phygraph.txt')
virtGraph = readGraph("./virtgraph.txt")
for i in range(25):
    for j in range(25):
        virtGraph[i][j] += phyGraph[i][j]//10
dist = [[0]*25]*25
floyd(phyGraph, dist)
demands = createDemands(10)
print(demands)
for item in demands:
    request(item[0], item[1], item[2])
res = findpathLB(2, 5, 1, dist, virtGraph)
print(res)
# print(fail)
