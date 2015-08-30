from _23Tree import _23Node

class _23TreeModel():
    def __init__(self, **kwargs):
        self.stat = 0
        #node0 = _23Node([66],[None,None])
        #node1 = _23Node([88,99],[None,None,None])
        #self.root = _23Node([77],[node0,node1])
        self.root = _23Node([],[None])
        self.insertSearchPath = None
        self.insertSearchChoice = None
        self.newkey = None
        pass

    def step(self):
        """
        Continue the current operation for 1 step.

        Returns:
            (bool)  Whether the operation is finished
        """
        if self.stat == 0:
            raise Exception("No operation in progress")
        
        if self.stat == 1:
            ### Look for a place to insert.
            assert len(self.insertSearchPath) > 0
            crtnode = self.insertSearchPath[-1]
            if not crtnode.isLeaf():
                ### We are at an interior node. Keep going.
                sel_chld_i = crtnode._chooseNext(self.newkey)
                self.insertSearchChoice.append(sel_chld_i)
                self.insertSearchPath.append(crtnode.childs[sel_chld_i])
                return False
            
            ### We are at a leaf. Do the insertion.
            crtnode.insertKeyInLeaf(self.newkey)
            if crtnode.isFat():
                ### Got extra work: split fat node.
                self.stat = 2
                return False
            ### Finished!
            self.newkey = None
            self.insertSearchChoice = None
            self.insertSearchPath = None
            self.stat = 0
            return True
            
        if self.stat == 2:
            ### We gotta deal with a fat node, in the tail of path.
            if len(self.insertSearchPath) >= 2:
                ### The fat node has a parent.
                pchoice = self.insertSearchChoice.pop()
                parent = self.insertSearchPath[-2]
                self.insertSearchPath.pop()
                _23Node.popUpKey(pchoice, parent)
                if parent.isFat():
                    ### Parent got fat. Solve it in the next step.
                    return False
                ### Finished!
                self.newkey = None
                self.insertSearchChoice = None
                self.insertSearchPath = None
                self.stat = 0
                return True

            ### Root is fat. Just split and finish.
            root = self.insertSearchPath.pop()
            popkey, newnode0, newnode1 = root._split()
            self.root = _23Node([popkey],[newnode0,newnode1])
            self.newkey = None
            self.insertSearchChoice = None
            self.insertSearchPath = None
            self.stat = 0
            return True
        
        raise Exception('Unimplemented')
        pass

    def startInsert(self, newkey):
        """
        Start an insertion.
        
        Params:
            newkey(object)  the key you wanna insert
        """
        assert self.stat == 0
        self.stat = 1
        self.insertSearchPath = [self.root]
        self.insertSearchChoice = []
        self.newkey = newkey

    def startDelete(self, oldkey):
        """
        Start an deletion.

        Params:
            oldkey(object)  the key you wanna delete
        """
        assert self.stat == 0
        self.stat = -1
        raise Exception('Unimplemented')
        pass

    def genTreeStat(self):
        """
        Generate the current state of the tree.

        A state includes tree structure.

        A structure is something like a BFS trace.
        If the tree is like this:
                 A
               /   \
             B C    D
            / | \   | \
           E  F  G  H  IJ
        then the structure should be:
        [
            [(A)],
            [(B,C),(D)],
            [(E),(F),(G),(H),(IJ)]
        ]
        
        Returns:
            (list of list of tuple of key)  just see the example above
        """
        BFSQ = [(self.root,0)]
        structure = []
        nodestruc = []
        while BFSQ:
            crtnode,crtdepth = BFSQ.pop(0)
            for chld in crtnode.childs:
                if chld != None: BFSQ.append((chld,crtdepth+1))
            if crtdepth == len(structure):
                structure.append([])
                nodestruc.append([])
            structure[-1].append(tuple(map(str, crtnode.keys)))
            nodestruc[-1].append(crtnode)
        
        extra = {'op':self.stat}
        if self.stat == 1:
            extra['newkey'] = str(self.newkey)
            extra['focus'] = _23TreeModel.findInNodeStructure(nodestruc, self.insertSearchPath[-1])
        elif self.stat == 2:
            extra['focus'] = _23TreeModel.findInNodeStructure(nodestruc, self.insertSearchPath[-1])
        return structure, extra

    @staticmethod
    def findInNodeStructure(nodestruc, node):
        for i in range(len(nodestruc)):
            layer = nodestruc[i]
            for j in range(len(layer)):
                if id(layer[j])==id(node):
                    return (i,j)
        assert False
        return None
    pass

