from matplotlib import pyplot
from matplotlib import animation

class _23Painter():
    FrameCount = 30
    FrameInterval = 20
    ACDCTime = 0.2
    KeyWidth = 0.2

    def __init__(self, model):
        self.model = model
        self.fig = pyplot.figure()
        pyplot.xlim(0,5)
        pyplot.ylim(0,5)
        self.key2obj = {}
        self.modelStatLast = 0
        pass

    @staticmethod
    def _animfunc(frame_idx, objs, objinfos):
        for obj in objs:
            objinfo = objinfos[obj]
            target = objinfo['targets'][frame_idx]
            objtype = objinfo['type']
            if objtype == 'text':
                obj.set_position(target['pos'])
            elif objtype == 'line':
                x0,y0 = target['pos0']
                x1,y1 = target['pos1']
                obj.set_data([x0,x1],[y0,y1])
            else:
                assert False
        return objs

    @staticmethod
    def gen1DTrajectory(x0,x1):
        """
        Generate the trajectory for a linear motion.

        The Velocity-Time graph is like this:
        v
        |
        |   _________
        |  /         \
        | /           \
        |/             \
        ----------------------- t(ms)
            ^        ^  ^
           200      800 1k

        Params:
            x0(float)   starting point
            x1(float)   finishing point

        Returns:
            (list of float) the trajectory
        """
        T = _23Painter.FrameCount * _23Painter.FrameInterval
        AVT = T * (1-_23Painter.ACDCTime)
        D = x1-x0
        TRI_AREA = D * _23Painter.ACDCTime / (1-_23Painter.ACDCTime) / 2
        BRECT_AREA = D * (1-_23Painter.ACDCTime*2) / (1-_23Painter.ACDCTime)
        
        positions = []
        for i in range(_23Painter.FrameCount):
            t = (i+1)/_23Painter.FrameCount
            pos = None
            if t < _23Painter.ACDCTime:
                pos = TRI_AREA * t * t / _23Painter.ACDCTime / _23Painter.ACDCTime
            elif t < 1-_23Painter.ACDCTime:
                pos = TRI_AREA + BRECT_AREA * (t - _23Painter.ACDCTime) / (1-_23Painter.ACDCTime*2)
            else:
                pos = D - TRI_AREA * (1-t) * (1-t) / _23Painter.ACDCTime / _23Painter.ACDCTime
            positions.append(pos)
            pass
        return positions

    def genObjChanges(self, newobjmap):
        """
        Compare new generated objmap with the current one,
        and generate the differences, used in animation.
        """
        pass

    @staticmethod
    def genNodeInfoFromBrief(brief):
        """
        Generate node library.

        We use (i,j) to identify the node in row i col j in tree structure.

        We compute the following for each node:
        {
            'pos': (x,y) # Where in data space should the node be
            'keys': ('a','b','c') # keys
        }
        """
        ret = {}
        layer_count = len(brief)
        x = 0
        y = 0
        for i in range(layer_count-1,-1,-1):
            layeri = brief[i]
            node_count = len(layeri)
            y += 1
            subj = 0
            for j in range(node_count):
                nodeij = layeri[j]
                if i == layer_count-1:
                    x += 1
                else:
                    chld_count = len(nodeij)
                    x = (ret[(i+1,subj)][0] + ret[(i+1,subj+chld_count)][0]) / 2
                    subj += chld_count+1
                ret[(i,j)] = (x,y)
        return ret

    @staticmethod
    def genKeysInfo(brief, nodeinfo, extra):
        ret = {}
        layer_count = len(brief)
        for i in range(layer_count-1,-1,-1):
            layeri = brief[i]
            node_count = len(layeri)
            for j in range(node_count):
                nodeij = layeri[j]
                key_count = len(nodeij)
                for k in range(key_count):
                    key = nodeij[k]
                    nodex,nodey = nodeinfo[(i,j)]
                    keypos = _23Painter.calcKeyPosFromNodePos(nodex,nodey,k,key_count)
                    #ret[k] = {'row':i,'col':j,'idx':k,'totbro':key_count,'pos':keypos}
                    ret[key] = keypos

        if extra['op'] == 1:
            nodex,nodey = nodeinfo[extra['focus']]
            ret[extra['newkey']] = (nodex,nodey+0.3)
        return ret

    @staticmethod
    def calcKeyPosFromNodePos(nodex, nodey, keyidx, keycount):
        assert keyidx >= 0
        assert keyidx < keycount
        keyx = nodex + (keyidx-(keycount-1)/2) * _23Painter.KeyWidth
        keyy = nodey
        return (keyx, keyy)

    @staticmethod
    def genKey2oldpos(key2obj):
        ret = dict(map(lambda X: (X[0],X[1].get_position()), key2obj.items()))
        return ret

    @staticmethod
    def compareKeyPoses(key2oldpos, key2newpos):
        oldset = set(key2oldpos.keys())
        newset = set(key2newpos.keys())
        newkeys = newset.difference()
        animkeys = oldset.intersection(newset)
        key2anim = {}
        for key in animkeys:
            x0,y0 = key2oldpos[key]
            x1,y1 = key2newpos[key]
            trxs = _23Painter.gen1DTrajectory(x0,x1)
            trys = _23Painter.gen1DTrajectory(y0,y1)
            tpos = zip(trxs, trys)
            targets = list(map(lambda x:{'pos':x}, tpos))
            key2anim[key] = {
                                'targets':targets,
                                'type':'text'}
        return newkeys, key2anim

    @staticmethod
    def genObj2Anim(key2obj, key2anim):
        return dict(map(lambda x:(key2obj[x[0]],x[1]), key2anim.items()))

    def update(self, useAnim):
        """
        Check what's new in data model and update the view.

        Params:
            useAnim(bool)   whether to use animation to illustrate the update
        """
        #print("CrtModelStat={0}, useAnim={1}".format(self.model.stat, useAnim))

        tree,extra = self.model.genTreeStat()
        nodes = _23Painter.genNodeInfoFromBrief(tree)
        key2newpos = _23Painter.genKeysInfo(tree, nodes, extra)
        
        keynewcount = len(key2newpos)
        objkeycount = len(self.key2obj)
        
        key2oldpos = _23Painter.genKey2oldpos(self.key2obj)
        newkeys,key2Anim = _23Painter.compareKeyPoses(key2oldpos, key2newpos)

        obj2anim = _23Painter.genObj2Anim(self.key2obj, key2Anim)

        oldobjs = list(self.key2obj.values())
        ### Pre-anim phase
        #   Get all the drawable objects ready.
        if len(newkeys)>0:
            for newkey in newkeys:
                assert type(newkey)==str
                x,y = key2newpos[newkey]
                keyobj = pyplot.text(x,y,newkey, fontsize=12)
                self.key2obj[newkey] = keyobj
            pyplot.show()

        ### Animate phase
        #   Play the animation.
        if len(key2Anim) > 0:
            animation.FuncAnimation(self.fig,
                                    self._animfunc,
                                    _23Painter.FrameCount,
                                    interval=20,
                                    fargs=(oldobjs, obj2anim),
                                    repeat=False,
                                    blit=True)
            pyplot.show()

        ### Post-anim phase
        #   abandon some useless objects.
        pass
    pass


