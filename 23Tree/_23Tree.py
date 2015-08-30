
class _23Node:
    def __init__(self, keys, childs):
        assert len(keys) <= 3
        assert len(keys)+1==len(childs)
        self.keys = keys
        self.childs = childs

    def __str__(self):
        isleaf = self.isLeaf()
        keycnt = len(self.keys)
        items = []
        i = 0
        while True:
            if not isleaf:
                items.append(str(self.childs[i]))
            if i >= keycnt: break
            items.append(str(self.keys[i]))
            i += 1
        return ','.join(items)
        
    def _split(self):
        '''
        Assume this node have 3 keys now,
        in which case we should split it.
        @return popkey  
        @return newnode0
        @return newnode1
        '''
        newnode0 = _23Node([self.keys[0]], self.childs[:2])
        newnode1 = _23Node([self.keys[2]], self.childs[2:])
        popkey = self.keys[1]
        return popkey,newnode0,newnode1
    
    def _chooseNext(self, x):
        assert(len(self.keys)+1==len(self.childs))
        cmp_to_keys = [x<key for key in self.keys]+[True]
        sel_chld_i = cmp_to_keys.index(True)
        return sel_chld_i
    
    def isLeaf(self):
        return self.childs[0] == None

    def search(self, x):
        if x in self.keys: return True
        chld_i = self._chooseNext(x)
        selchld = self.childs[chld_i]
        if selchld == None: return False
        return selchld.search(x)
        
    def insert(self, x):
        '''
        Assume that key x does not exists in this tree.
        Insert x into this tree.
        '''
        if self.isLeaf():
            self.keys.append(x)
            self.keys.sort()
            self.childs.append(None)
        else:
            sel_chld_i = self._chooseNext(x)
            sel_chld = self.childs[sel_chld_i]
            sel_chld.insert(x)
            
            if len(sel_chld.keys) >= 3:
                self.popUpKey(sel_chld_i, self)

    def contains(self, x):
        if x in self.keys: return True
        sel_chld_i = self._chooseNext(x)
        return self.childs[sel_chld_i].contains(x)
    
    def findUnderMaxThenReplace(self, x):
        '''
        Search down this node for the largest key less than x.
        Once located, do a swap with key x in current node.

        We assume this node is not a leaf, and x is in this node.

        Returns:
            (int): which way did we go in the first step?
        '''
        assert not self.isLeaf()
        sel_chld_idx = self.keys.index(x)
        crtnode = self.childs[sel_chld_idx]
        while not crtnode.isLeaf():
            crtnode = crtnode.childs[-1]
        cand = crtnode.keys[-1]
        crtnode.keys[-1] = x
        self.keys[sel_chld_idx] = cand

        return sel_chld_idx

    def delete(self, x):
        '''
        Delete key x from the 2-3 tree rooted at this node,
        assuming the target key exists.

        The keys in this node might change.
        The height of this 2-3 tree might decrease.
        
        Params:
            x(int): the key to delete.

        Returns:
            (_23Node): The new root of this 2-3 tree.
            (boolean): whether the height of this 2-3 tree decreased.
        '''
        if self.isLeaf():
            xidx = self.keys.index(x)
            self.keys.pop(xidx)
            assert self.childs in [[None,None],[None,None,None]]
            self.childs.pop()
            if len(self.keys) == 0:
                return None,True
            return self,False

        if x in self.keys:
            sel_chld_idx = self.findUnderMaxThenReplace(x)
        else:
            sel_chld_idx = self._chooseNext(x)

        newchld,height_deced = self.childs[sel_chld_idx].delete(x)
        self.childs[sel_chld_idx] = newchld
        if not height_deced:
            return self,False
            
        res = self.fixHeight(self, sel_chld_idx)
        if res == -1:
            if len(self.keys) <= 2: return self,True
            popkey,newnode0,newnode1 = self._split()
            newthis = _23Node([popkey],[newnode0,newnode1])
            return newthis,False
        else:
            if len(self.childs[res].keys) == 3:
                self.popUpKey(res, self)
                assert len(self.keys)<=2
            return self,False

    def insertKeyInLeaf(self, x):
        assert self.isLeaf()
        self.keys.append(x)
        self.keys.sort()
        self.childs.append(None)

    def isFat(self):
        return len(self.keys) >= 3

    @staticmethod
    def popUpKey(fatChldIdx, parent):
        '''
        The fatChldIdx-th child of parent has 3 keys now.
        Split it and update the parent.
        NOTE: parent may become fat.

        Params:
            fatChldIdx(int): which child is fat?
            parent(_23Node): the node whose has one fat child.
        '''
        assert not parent.isLeaf()
        popkey,newnode0,newnode1 = parent.childs[fatChldIdx]._split()
        parent.keys.insert(fatChldIdx, popkey)
        parent.childs.pop(fatChldIdx)
        parent.childs.insert(fatChldIdx, newnode1)
        parent.childs.insert(fatChldIdx, newnode0)

    @staticmethod
    def fixHeight(parent, child_idx):
        '''
        Assuming the child_idx-th child of parent
        is 1 layer shorter than the other children,
        modify both parent and the child to make all children equally tall.

        NOTE: after this operation, the parent or some child can be fat.
        
        NOTE: if parent has 1 key only, after this operation,
        the parent height may decrease.
        
        Returns:
            (int):  -1,
                    if the parents had 2 children before
                        (in this case parent height decreased), or
                    idx of the updated child,
                    if the parent had 3 children before.
        '''
        keycnt = len(parent.keys)
        if keycnt == 1:
            '''
            In a 2-child case, merge the taller child into parent.
            NOTE: 3-key parent may appear.
            '''
            if child_idx == 0:
                taller_chld = parent.childs[1]
                parent.keys += taller_chld.keys
                parent.childs = [parent.childs[0]] + taller_chld.childs
            elif child_idx == 1:
                taller_chld = parent.childs[0]
                parent.keys = taller_chld.keys + parent.keys
                parent.childs = taller_chld.childs + [parent.childs[1]]
            else:
                assert False
            return -1
        elif keycnt == 2:
            '''
            In a 3-child case,
            merge the shorter tree to a neighbor child,
            and pull down a victim key from parent.
            NOTE: 3-key child may appear.
            '''
            dst_chld_idx = child_idx-1
            if dst_chld_idx < 0: dst_chld_idx = child_idx+1
            
            toHead = child_idx < dst_chld_idx
            dst_chld = parent.childs[dst_chld_idx]

            victim_key_idx = min(dst_chld_idx, child_idx)
            victim_key = parent.keys[victim_key_idx]
            shorter_chld = parent.childs[child_idx]

            if child_idx < dst_chld_idx:
                dst_chld.keys.insert(0, victim_key)
                dst_chld.childs.insert(0, shorter_chld)
            else:
                dst_chld.keys.append(victim_key)
                dst_chld.childs.append(shorter_chld)

            parent.keys.pop(victim_key_idx)
            parent.childs.pop(child_idx)

            return parent.childs.index(dst_chld)
        else:
            assert False


class _23Set:
    def __init__(self):
        self.root = None
    
    def __str__(self):
        if self.isEmpty(): return ''
        return str(self.root)

    def insert(self, x):
        if self.root == None:
            self.root = _23Node([x],[None,None])
        else:
            self.root.insert(x)
            if len(self.root.keys) >= 3:
                popkey,newnode0,newnode1 = self.root._split()
                self.root = _23Node([popkey],[newnode0,newnode1])
    
    def contains(self, x):
        if self.isEmpty(): return False
        return self.root.search(x)
        
    def delete(self, x):
        if not self.contains(x): return False
        self.root,_ = self.root.delete(x)
        return True

    def isEmpty(self):
        return self.root == None or len(self.root.keys)==0

