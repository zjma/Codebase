#include <unordered_set>
#include <vector>
#include <fstream>

#include "FMCB.h"
using namespace std;

#define NMAX 8000
#define MMAX 20000

int c0[MMAX], c1[MMAX];
int var2assign[NMAX];

int solve()
{
    ifstream fin("spo.in");
    ofstream fot("spo.out");
    int m, n;
    fin >> n >> m;

    int i;
    for (i = 0; i < m; i++)
    {
        int x, y;
        fin >> x >> y;
        x--;y--;

        c0[i] = x^1;
        c1[i] = y^1;
    }

    int ret = FMCB::solve2SAT(n, m, c0, c1, var2assign);
    if (ret < 0)
    {
        fot << "NIE" << endl;
    }
    else
    {
        for (int i = 0; i < n; i++)
            fot << (i*2+var2assign[i]+1) << endl;
    }
    return 0;
}

void testTarjan()
{
    vector<unordered_set<int>> vid2nxts(6);
    vid2nxts[0].insert(5);
    vid2nxts[0].insert(1);
    vid2nxts[1].insert(2);
    vid2nxts[2].insert(3);
    vid2nxts[3].insert(1);
    vid2nxts[4].insert(2);
    vid2nxts[5].insert(4);
    vid2nxts[5].insert(0);
    vid2nxts[5].insert(1);
    vid2nxts[3].insert(5);
    vector<int> vid2cid(6, -1);
    vector<unordered_set<int>> cid2nxts;
    vector<unordered_set<int>> cid2vids;
    int cn = FMCB::TarjanCondense(6, vid2nxts, vid2cid, cid2nxts, cid2vids);

    return;
}

void test2SAT()
{
    int n = 3;
    int m = 2;
    int c0[] = { 0,1 };
    int c1[] = { 0,2 };
    int ret[3];
    int res = FMCB::solve2SAT(n, m, c0, c1, ret);
    return;
}

int main()
{
    solve();
}