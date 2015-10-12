#include <vector>
#include <cassert>
#include <algorithm>
#include <unordered_set>

#include "FMCB.h"
#include "2-SAT.h"

using namespace std;

inline int neg(int x)
{
    return x ^ 1;
}


/**
 * \param n             How many nodes.
 * \param vid2nxts      Graph.
 * \param vid           Current node.
 * \param timer         Current Time.
 * \param vid2arrtime   Will put arrtime here.
 * \param vid2lowtime   Will put lowtime here.
 * \param lateStack     Will use a stack.
 * \param cn            How many components determined?
 * \param vid2cid       Will put map vid => cid here.
 */
void tarjan_dfs(
    int n,
    const vector<unordered_set<int>> &vid2nxts,
    int vid,
    int &timer,
    vector<int> &vid2arrtime,
    vector<int> &vid2lowtime,
    vector<int> &lateStack,
    int &cn,
    vector<int> &vid2cid)
{
    assert(vid >= 0 && vid < n);
    assert(vid2arrtime[vid] == -1);
    vid2arrtime[vid] = vid2lowtime[vid] = timer++;
    lateStack.push_back(vid);

    for (auto nxt : vid2nxts[vid])
    {
        if (vid2cid[nxt] != -1) continue;
        if (vid2arrtime[nxt] != -1)
        {
            vid2lowtime[vid] = min(vid2lowtime[vid], vid2arrtime[nxt]);
        }
        else
        {
            tarjan_dfs(n, vid2nxts, nxt, timer, vid2arrtime, vid2lowtime, lateStack, cn, vid2cid);
            vid2lowtime[vid] = min(vid2lowtime[vid], vid2lowtime[nxt]);
        }
    }
    
    if (vid2lowtime[vid] < vid2arrtime[vid]) return;

    for (;;)
    {
        int top = lateStack.back();
        lateStack.pop_back();
        assert(vid2cid[top] == -1);
        assert(top == vid || vid2lowtime[top] < vid2arrtime[top]);
        vid2cid[top] = cn;
        if (top == vid) break;
    }
    ++cn;
}

/**
 * \param n             How many nodes.
 * \param vid2nxts      The graph.
 * \param ret_vid2cid   We put the map vid => cid here.
 * \param ret_cid2nxts  We put the condensed graph here.
 * \param ret_cid2vids  We put the map cid => vids here.
 *
 * \return  How many component generated.
 */
int FMCB::TarjanCondense(int n,
    vector<unordered_set<int>> &vid2nxts,
    vector<int> &ret_vid2cid,
    vector<unordered_set<int>> &ret_cid2nxts,
    vector<unordered_set<int>> &ret_cid2vids)
{
    vector<int> vid2arrtime(n, -1);
    vector<int> vid2lowtime(n, -1);
    vector<int> lateStack;

    int timer = 0;
    int componentCounter = 0;
    //Condense and assign component id.
    {
        int i;
        for (i = 0; i < n; ++i)
        {
            if (vid2arrtime[i] >= 0) continue;
            tarjan_dfs(n, vid2nxts, i, timer,
                vid2arrtime, vid2lowtime,
                lateStack,
                componentCounter, ret_vid2cid);
        }
    }

    for (int i = 0; i < n; i++)
        assert(ret_vid2cid[i] != -1);

    //Compute component edges.
    {
        ret_cid2nxts.resize(componentCounter);
        for (int i = 0; i < n; i++)
        {
            int eifrom = ret_vid2cid[i];
            for (auto &nxt : vid2nxts[i])
            {
                int eito = ret_vid2cid[nxt];
                if (eito == eifrom) continue;
                ret_cid2nxts[eifrom].insert(eito);
            }
        }
    }
    
    // Compute cid => vids
    {
        ret_cid2vids.resize(componentCounter);
        for (int i = 0; i < n; i++)
        {
            int cid = ret_vid2cid[i];
            ret_cid2vids[cid].insert(i);
        }
    }

    return componentCounter;
}

int getOneFromSet(unordered_set<int> &many)
{
    for (const auto &i : many)
    {
        return i;
    }
    assert(false);
}

/**
 * Solve 2-SAT, return a feasible assignment if possible.
 *
 * Rename your n variables to x_0, x_1, ..., x_{n-1}.
 * Rename your m clauses to clause_0, clause_1, ..., clause_{m-1}.
 * Your clause_i should be like x_i or not x_j.
 *
 * To invoke this function, describe the clauses like this:
 *   If clause_i = x_j or not x_k,
 *     set clause_0[i] to j*2+1 and set clause_1[i] to k*2.
 *
 * If a feasible assignment {x_0=b_0, x_1=b_1, ...} is found,
 * ret[i] will be set to b_i.
 * Otherwise ret[i] will remain unmodified.
 *
 * \param n         How many variables?
 * \param m         How many clauses?
 * \param clause_0  len=m array, clauses' 1st arguments.
 * \param clause_1  len=m array, clauses' 2nd arguments.
 *
 * \param ret       len=n array, place to put feasible assignment.
 *
 * \return          0 if feasible assignment found, or -1 if no solution.
 */
int FMCB::solve2SAT(int n,
    int m, int clause_0[], int clause_1[],
    int ret[])
{
    vector<unordered_set<int>> vid2nxts(n*2);

    // Build graph.
    {
        int i, en;
        for (en = 0, i = 0; i < m; i++)
        {
            int e0from = neg(clause_0[i]);
            int e0to = clause_1[i];

            if (e0from == e0to) continue;

            vid2nxts[e0from].insert(e0to);

            if (e0from == neg(e0to)) continue;

            int e1from = neg(clause_1[i]);
            int e1to = clause_0[i];
            
            vid2nxts[e1from].insert(e1to);
        }
    }

    vector<int> vid2cid(n*2, -1);
    vector<unordered_set<int>> cid2nxts;
    vector<unordered_set<int>> cid2vids;

    // Condense to compoments.
    int cn = TarjanCondense(n*2, vid2nxts, vid2cid, cid2nxts, cid2vids);

    // Check if conflicting nodes in the same compoment.
    {
        int i;
        for (i = 0; i < n; i++)
        {
            int v0 = i * 2;
            int v1 = v0 + 1;
            assert(vid2cid[v0] >= 0);
            assert(vid2cid[v1] >= 0);
            if (vid2cid[v0] == vid2cid[v1]) return -1;
        }
    }

    vector<int> topoidx2cid;

    // Topo-sort the compoment graph.
    {
        vector<int> cid2deg(cn, 0);

        for (auto &nxts : cid2nxts)
            for (auto &nxt : nxts)
                cid2deg[nxt]++;

        int i, j = 0;
        for (i = 0; i < cn; ++i)
            if (cid2deg[i] == 0)
            {
                topoidx2cid.push_back(i);
                ++j;
            }

        assert(j > 0);

        for (i = 0; i < j; ++i)
        {
            int cid = topoidx2cid[i];
            for (auto &nxt : cid2nxts[cid])
            {
                int tmpdeg = --cid2deg[nxt];
                if (tmpdeg > 0) continue;
                topoidx2cid.push_back(nxt);
                ++j;
            }
        }
        assert(j == cn);
    }

    vector<int> cid2assign(cn, -1);

    // Assign 0/1 to compoments.
    {
        for (auto &cid : topoidx2cid)
        {
            if (cid2assign[cid] != -1) continue;
            cid2assign[cid] = 0;
            int vid = getOneFromSet(cid2vids[cid]);
            int vjd = neg(vid);
            int cjd = vid2cid[vjd];
            assert(cid2assign[cjd] == -1);
            cid2assign[cjd] = 1;
        }
    }

    // Compute vid => assignment.
    {
        for (int i = 0; i < n; i++)
        {
            int vid = i * 2 + 1;
            int cid = vid2cid[vid];
            ret[i] = cid2assign[cid];
        }
    }
    return 0;

}

