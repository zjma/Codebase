#pragma once
using namespace std;
namespace FMCB
{
    /**
    * Condense a graph.
    * Your graph nodes should be numbered 0..n-1.
    * We will return a new graph to you,
    * as well as the num of components and the mapping.
    * 
    * \param n             How many nodes.
    * \param vid2nxts      The graph.
    * \param ret_vid2cid   We put the map vid => cid here.
    * \param ret_cid2nxts  We put the condensed graph here.
    * \param ret_cid2vids  We put the map cid => vids here.
    *
    * \return  How many component generated.
    */
    int TarjanCondense(int n,
        vector<unordered_set<int>> &vid2nxts,
        vector<int> &ret_vid2cid,
        vector<unordered_set<int>> &ret_cid2nxts,
        vector<unordered_set<int>> &ret_cid2vids);


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
	int solve2SAT(int n,
		int m, int clause_0[], int clause_1[],
		int ret[]);
}