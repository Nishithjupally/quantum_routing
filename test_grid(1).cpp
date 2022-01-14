#include <vector>
#include <unordered_set>
#include <iostream>
#include <stdlib.h>
#include <bits/stdc++.h>

using namespace std;
int fail = 0;
int V = 25;
int C = 100;
//Both Physical & virtual graph is adjacency matrix.
// struct ESP
// {
//     int ESP_id;
//     vector<int> children;
// };

// //i->ESP_id
// map<int, ESP *> m;

// vector<vector<ESP *>> graph;

void print_matrix(vector<vector<int>> &m)
{
    for (int i = 0; i < V; i++)
    {
        for (int j = 0; j < V; j++)
        {
            cout << m[i][j] << " ";
        }
        cout << endl;
    }
}
//MG
//798, 1680, 2474, 3285, 1095, 4910, 5776, 6576, 7671, 8512, 9107, 10210, 10977, 11927, 12761, 13615, 14535, 15584, 16558, 17364, 18185, 19174, 19912, 21484, 25157, 26689, 27764, 28745, 29742, 30775, 31878, 32825, 33859, 34912, 35950, 36928, 37990, 39026, 39997, 41074, 42042, 43106, 41068, 45169, 46251, 47207, 48277, 49284, 50338, 51316
//798, 1680, 2474, 3285, 1095, 4910, 5776, 6538, 7494, 8334, 9205, 10010, 10741, 11630, 12474, 13273, 14137, 15079, 16033, 16864, 17613, 18608, 19287, 20842, 24481, 26000, 27000, 28000, 29000, 30000, 310, 32000, 33000, 31000, 35000, 36000, 37000, 38000, 39000, 10000, 410, 42000, 43000, 41000, 45000, 46000, 47000, 48000, 49000, 50000
//4221, 8868, 13086, 17364, 21622, 26007, 30472, 34691, 10172, 44671, 49265, 53728, 57534, 62435, 66839, 71286, 76079, 81366, 86537, 90826, 95028, 100295, 101048, 111633, 128111, 135349, 110774, 145757, 151155, 156200, 161633, 166456, 171711, 177029, 182220, 187306, 192773, 197797, 202870, 208527, 213095, 218641, 223500, 229088, 234671, 239362, 244914, 249830, 255318, 260213

void floyd(vector<vector<int>> &phygraph, vector<vector<int>> &dist)
{
    for (int i = 0; i < V; i++)
    {
        for (int j = 0; j < V; j++)
        {
            dist[i][j] = phygraph[i][j];
            if (dist[i][j] == 0 && i != j)
                dist[i][j] = 2000;
        }
    }

    for (int k = 0; k < V; k++)
    {
        for (int i = 0; i < V; i++)
        {
            for (int j = 0; j < V; j++)
            {
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
            }
        }
    }
}

vector<vector<int>> generateMatrix(int d)
{
    //printf("Hello!");
    int N = (C * (C - 1)) / 2;
    vector<int> arr(N, 0);
    for (int i = 0; i < d; i++)
        arr[i] = rand() % 2;
    random_shuffle(arr.begin(), arr.end());

    int c = 0;
    vector<vector<int>> result(C, vector<int>(C, 0));
    for (int i = 0; i < C; i++)
    {
        for (int j = i + 1; j < C; j++)
        {
            result[i][j] = arr[c++];
        }
    }

    return result;
}
//1-0-0-0-0-0-0-0-1
void find_metrics(vector<int> &path, int d, vector<vector<int>> &virtgraph, vector<int> &res, vector<vector<int>> &dist)
{
    res[0] = 0, res[1] = d, res[2] = 0;
    for (int i = 0; i + 1 < path.size(); i++)
    {
        res[1] = min(res[1], virtgraph[path[i]][path[i + 1]]);
        //cout << virtgraph[path[i]][path[i+1]] << endl;
        if (virtgraph[path[i]][path[i + 1]] >= d)
        {
            virtgraph[path[i]][path[i + 1]] -= d;
            virtgraph[path[i + 1]][path[i]] -= d;
        }
        else
        {
            int x = d - virtgraph[path[i]][path[i + 1]], y = dist[path[i]][path[i + 1]];
            virtgraph[path[i]][path[i + 1]] = 0;
            virtgraph[path[i + 1]][path[i]] = 0;
            res[0] = res[0] + x;
            res[2] = res[2] + (log(y) * x);
        }
    }
    res[1] = d - res[1];
}

vector<int> findpathMG(int src, int dest, int demand, vector<vector<int>> &dist, vector<vector<int>> &virtgraph)
{
    int u_curr = src;

    vector<int> result;
    result.push_back(src);
    unordered_set<int> st;
    st.insert(src);
    //print_matrix(virtgraph);
    //printf("%d %d\n", src, dest);
    while (u_curr != dest)
    {
        //cout<<"HI"<<endl;
        int d = INT_MAX;
        int u;
        for (int i = 0; i < V; i++)
        {
            if (st.find(i) == st.end() && (virtgraph[u_curr][i] > 0 || dist[i][u_curr] == 100) && d > dist[i][dest])
            {
                u = i;
                d = dist[i][dest];
            }
        }
        if (virtgraph[u][u_curr] < demand && dist[u_curr][u] + dist[u][dest] > dist[u_curr][dest])
        {
            d = INT_MAX;
            for (int i = 0; i < V; i++)
            {
                if (st.find(i) == st.end() && dist[i][u_curr] == 100 && d > dist[i][dest])
                {
                    u = i;
                    d = dist[i][dest];
                }
            }
        }

        result.push_back(u);
        st.insert(u);
        u_curr = u;
    }
    return result;
}

vector<int> findpathLB(int src, int dest, int demand, vector<vector<int>> &dist, vector<vector<int>> &virtgraph)
{
    int u_curr = src;
    vector<int> result;
    result.push_back(src);
    unordered_set<int> st;
    st.insert(src);
    int count = 0;
    while (u_curr != dest)
    {
        int temp = u_curr;
        int d = INT_MAX;
        int u = -1;
        for (int i = 0; i < V; i++)
        {
            if (st.find(i) == st.end() && virtgraph[i][u_curr] >= demand && d > dist[i][dest])
            {
                u = i;
                d = dist[i][dest];
            }
        }
        if (u == -1 || dist[u_curr][dest] > dist[u][dest])
        {
            d = INT_MAX;
            for (int i = 0; i < V; i++)
            {
                if (virtgraph[u_curr][i] >= 0 && dist[i][u_curr] == 100 && d > dist[i][dest])
                {
                    u = i;
                    d = dist[i][dest];
                }
            }
        }

        //cout << src << " " << dest << "    " << u << endl;
        result.push_back(u);
        st.insert(u);
        u_curr = u;
        if (temp == u_curr)
            count++;
        else
            count = 0;
        if (count > 25)
        {
            fail = 1;
            break;
        }
    }
    return result;
}

vector<int> findpathLB_Mod(int src, int dest, int demand, vector<vector<int>> &dist, vector<vector<int>> &virtgraph)
{
    int u_curr = src;
    vector<int> result;
    //cout<<"HI MOD L"<<endl;
    result.push_back(src);
    unordered_set<int> st;
    st.insert(src);
    // cout<<"HI MOD L"<<endl;
    int count = 0;
    while (u_curr != dest)
    {
        int temp = u_curr;

        // cout<<"HI MOD bL"<<endl;
        int d = INT_MAX;
        int u = -1;

        for (int i = 0; i < V; i++)
        {
            if (st.find(i) == st.end() && virtgraph[i][u_curr] >= demand && d > dist[i][dest])
            {
                u = i;
                // cout<<"HI MOD 1L"<<endl;
                d = dist[i][dest];
            }
        }
        // cout << "---" << u << endl;
        if (u == -1 || dist[u_curr][dest] < dist[u][dest])
        {
            d = INT_MAX;
            for (int i = 0; i < V; i++)
            {
                // cout<<"HI MOD 2L"<<endl;
                // cout<<u_curr<<" "<<i<<" "<<V<<" "<<endl;
                // cout<<virtgraph[u_curr][i]<<endl;
                // cout<<"HI MOD 3L"<<endl;
                if (virtgraph[u_curr][i] >= 0 && dist[i][u_curr] == 100 && d > dist[i][dest])
                {
                    u = i;
                    //		cout<<"HI MOD e1L"<<endl;
                    d = dist[i][dest];
                    //	cout<<"HI MOD e2L"<<endl;
                }
            }
        }
        // cout<<u<<" "<<"HI MOD eL"<<endl;
        //cout << src << " " << dest << "    " << u << endl;
        result.push_back(u);
        st.insert(u);
        u_curr = u;
        if (temp == u_curr)
            count++;
        else
            count = 0;
        if (count > 25)
        {
            fail = 1;
            break;
        }
    }
    return result;
}
void take_input(vector<vector<int>> &phygraph, vector<vector<int>> &virtgraph, int n)
{

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            int x;
            cin >> x;
            virtgraph[i][j] = x * 10;
        }
    }

    printf("taken input!");
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            int x;
            cin >> x;
            phygraph[i][j] = x * 625;
            virtgraph[i][j] = x * 10;
        }
    }
}
void take_input_d(vector<vector<int>> &dem, int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            int x;
            cin >> x;
            dem[i][j] = x;
        }
    }
}

int main()
{
    //cout << "Hello!";
    int n = V;
    //cin> >n> >demand;
    //cout << "Hello!";
    vector<vector<int>> dist(n, vector<int>(n, 0));
    vector<vector<int>> dem(C, vector<int>(C, 0));
    //cout << "Hello!";

    //take_input(phygraph,virtgraph,n);
    //take_input_d(dem,n);

    vector<vector<int>> buffer{
        {0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 10},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0}};

    vector<vector<int>> phygraph{
        {0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 100, 0, 0, 0, 100, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0, 0, 100, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0, 100},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, 0}};

    for (int i = 0; i < 25; i++)
    {
        for (int j = 0; j < 25; j++)
        {
            buffer[i][j] += (phygraph[i][j] / 10);
            buffer[i][j] *= 1;
        }
    }

    vector<vector<int>> virtgraph, virt1, virt2;

    floyd(phygraph, dist);
    vector<vector<int>> metrics, metrics1, metrics2;
    vector<int> sums(3, 0), sums1(3, 0), sums2(3, 0);
    vector<int> res, res1, res2;
    vector<int> met(3, 0), met1(3, 0), met2(3, 0);
    vector<int> temp = findpathLB(2, 5, 1, dist, buffer);
    for (auto i : temp)
        cout << i << " ";
    // for (int d = 300; d <= 500; d++)
    // {
    //     sums[0] = 0;
    //     sums[1] = 0;
    //     sums[2] = 0;
    //     sums1[0] = 0;
    //     sums1[1] = 0;
    //     sums1[2] = 0;
    //     sums2[0] = 0;
    //     sums2[1] = 0;
    //     sums2[2] = 0;
    //     //cout<<"-----------------"<<d<<"---------------"<<endl;
    //     for (int T = 0; T < 100; T++)
    //     {
    //             cout<<"-----------------"<<100*d+ T<<"---------------"<<endl;
    //         virtgraph = virt2 = virt1 = buffer;
    //         dem = generateMatrix(d);
    //         //dem[0][4]=2;
    //         for (int i = 0; i < C; i++)
    //         {
    //             for (int j = i + 1; j < C; j++)
    //             {
    //                 if (dem[i][j] == 1)
    //                 {
    //                     int src = i / 4, dest = j / 4;
    //                     res = findpathMG(src, dest, dem[i][j], dist, virtgraph);
    //                     fail=0;
    //                     res1 = findpathLB(src, dest, dem[i][j], dist, virt1);
    //                     if(fail==1){
    //                    	fail =0;
    //                    	for (int i = 0; i < 25; i++)
    // 			    {
    // 				for (int j = 0; j < 25; j++)
    // 				{
    // 				    virt1[i][j] *= 0;
    // 				}
    // 			    }
    //                    }
    //                     fail=0;
    //                    res2 = findpathLB_Mod(src, dest, dem[i][j], dist, virt2);
    //                    if(fail==1){
    //                    	fail =0;
    //                    	for (int i = 0; i < 25; i++)
    // 			    {
    // 				for (int j = 0; j < 25; j++)
    // 				{
    // 				    virt2[i][j] *= 0;
    // 				}
    // 			    }
    //                    }
    //                    find_metrics(res, dem[i][j], virtgraph, met, dist);
    //                    find_metrics(res1, dem[i][j], virt1, met1, dist);
    //                     find_metrics(res2, dem[i][j], virt2, met2, dist);
    //                     sums[0] += met[0];
    //                     sums[1] += met[1];
    //                     sums[2] += met[2];
    //                     sums1[0] += met1[0];
    //                     sums1[1] += met1[1];
    //                     sums1[2] += met1[2];
    //                     sums2[0] += met2[0];
    //                     sums2[1] += met2[1];
    //                     //if(met2[1]>1)
    //                     //cout << dem[i][j] << " " << met2[1] << " " << src << " " << dest << " " << T << " " << d << endl;
    //                     sums2[2] += met2[2];
    //                 }
    //             }
    //         }
    //         // sums[0] /= d;
    //         // sums[1] /= d;
    //         // sums[2] /= d;
    //     }
    //     // sums[0] /= d;
    //     // sums[1] /= d;
    //     // sums[2] /= d;
    //     metrics.push_back(sums);
    //     metrics1.push_back(sums1);
    //     metrics2.push_back(sums2);
    // }
    // cout << "Modified Greedy\n";
    // for (int j = 0; j < 3; j++)
    // {
    //     for (int i = 0; i < metrics.size(); i++)
    //     {
    //         cout << metrics[i][j];
    //         if (i + 1 != metrics.size())
    //             cout << ", ";
    //     }
    //     cout << "\n";
    // }
    // cout << "Local Best\n";
    // for (int j = 0; j < 3; j++)
    // {
    //     for (int i = 0; i < metrics1.size(); i++)
    //     {
    //         cout << metrics1[i][j];
    //         if (i + 1 != metrics1.size())
    //             cout << ", ";
    //     }
    //     cout << "\n";
    // }
    // cout << "Local Best Modified\n";
    // for (int j = 0; j < 3; j++)
    // {
    //     for (int i = 0; i < metrics2.size(); i++)
    //     {
    //         cout << metrics2[i][j];
    //         if (i + 1 != metrics2.size())
    //             cout << ", ";
    //     }
    //     cout << "\n";
    // }

    return 0;
}
