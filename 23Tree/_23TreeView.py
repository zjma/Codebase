from matplotlib import pyplot
from matplotlib import animation

class _23Painter():
    FrameCount = 10
    FrameInterval = 60
    ACDCTime = 0.2
    KeyWidth = 0.2

    def __init__(self, model):
        self.model = model
        self.fig = pyplot.figure()
        pyplot.xlim(0,5)
        pyplot.ylim(0,5)
        self.modelStatLast = 0
        
        #self.rootobj, = pyplot.plot(2.5,2.5)
        self.key2obj = {}

        # A circle showing the current node.
        self.focusMarkerObj = pyplot.scatter(2.5,2.5,s=[800], edgecolor='none', facecolor='none')
        #TODO

        self.keysFocused = None

        self.rootPos = (2.5,2.5)
        self.key2pos = {}
        self.winPos = (0,5,0,5)
        self.focusMarkerPos = (2.5,2.5)
        pass

    @staticmethod
    def _animfunc(frame_idx, key2obj, focusmarkerobj, key2traj, winTraj, focusMarkerTraj):
        """
        Reposition drawable objects and camera.

        Params:
            frame_idx(int)
            key2obj(dict)           key => drawable object
            key2traj(dict)          key => trajectory of the key
            winTraj(list)           window trajectory
            focusMarkerTraj(list)   focus marker trajectory
        """
        ### move the keys on data plane
        for key,txt in key2obj.items():
            tmpDatPos = key2traj[key][frame_idx]
            txt.set_position(tmpDatPos)

        ### move the camera
        x0,x1,y0,y1 = winTraj[frame_idx]
        pyplot.xlim(x0,x1)
        pyplot.ylim(y0,y1)

        ### move the focus marker
        #x,y = focusMarkerTraj[frame_idx]
        #focusmarkerobj.set_data([x,],[y,])
        #TODO

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
            positions.append(x0+pos)
            pass
        return positions

    @staticmethod
    def genNdimTrajectory(p0,p1):
        pst = zip(p0,p1)
        trajs = list(map(lambda tp:_23Painter.gen1DTrajectory(tp[0],tp[1]), pst))
        return list(zip(*trajs))

    @staticmethod
    def genNode2RawPos(brief):
        """
        We compute raw position for each node:

        Returns:
            (dict of (float,float)):    raw positions
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
    def genKey2RawPos(treeStruct, node2RawPos, extra):
        ret = {}
        layer_count = len(treeStruct)
        for i in range(layer_count-1,-1,-1):
            layeri = treeStruct[i]
            node_count = len(layeri)
            for j in range(node_count):
                nodeij = layeri[j]
                key_count = len(nodeij)
                for k in range(key_count):
                    key = nodeij[k]
                    nodex,nodey = node2RawPos[(i,j)]
                    keypos = _23Painter.calcKeyPosFromNodePos(nodex,nodey,k,key_count)
                    ret[key] = keypos
        if extra['op']==1:
            newkey = extra['newkey']
            bnode = extra['focus']
            nodex,nodey = node2RawPos[bnode]
            ret[newkey] = (nodex,nodey+_23Painter.KeyWidth)
        return ret

    @staticmethod
    def calcKeyPosFromNodePos(nodex, nodey, keyidx, keycount):
        assert keyidx >= 0
        assert keyidx < keycount
        keyx = nodex + (keyidx-(keycount-1)/2) * _23Painter.KeyWidth
        keyy = nodey
        return (keyx, keyy)

    @staticmethod
    def getNewKeys(key2OldDatPos, key2NewDatPos):
        oldset = set(key2OldDatPos.keys())
        newset = set(key2NewDatPos.keys())
        return newset.difference(oldset)

    @staticmethod
    def genKey2Traj(key2OldDatPos, key2NewDatPos):
        key2traj = {}
        for key in key2NewDatPos.keys():
            x1,y1 = key2NewDatPos[key]
            x0,y0 = key2OldDatPos.get(key, (x1,y1))
            trxs = _23Painter.gen1DTrajectory(x0,x1)
            trys = _23Painter.gen1DTrajectory(y0,y1)
            tpos = list(zip(trxs, trys))
            key2traj[key] = tpos
        return key2traj

    @staticmethod
    def genNewFocus(oldFocus, treeStruct, extra):
        if 'focus' not in extra:
            return oldFocus
        i,j = extra['focus']
        return treeStruct[i][j]

    _SUB2D = staticmethod(lambda a,b: tuple([v0-v1 for v0,v1 in zip(a,b)]))
    _ADD2D = staticmethod(lambda a,b: tuple([v0+v1 for v0,v1 in zip(a,b)]))

    @staticmethod
    def applyDeltaToKey2pos(key2pos, delta):
        movekey = lambda kp: (kp[0],_23Painter._ADD2D(kp[1],delta))
        return dict(map(movekey, key2pos.items()))

    @staticmethod
    def genFocusPos2(keysFocused, key2pos, rootpos):
        if keysFocused==None or len(keysFocused)==0:
            return rootpos
        isFoced = lambda kv: kv[0] in keysFocused
        getPos = lambda kv: kv[1]
        involvedItems = list(filter(isFoced, key2pos.items()))
        poses = list(map(getPos, involvedItems))
        xs = [p[0] for p in poses]
        ys = [p[1] for p in poses]
        fx = sum(xs)/len(xs)
        fy = sum(ys)/len(ys)
        return (fx,fy)


    @staticmethod
    def resizeRect(winpos, ratio):
        x0,x1,y0,y1 = winpos
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        dx = (x1-x0)*ratio/2
        dy = (y1-y0)*ratio/2
        return (cx-dx,cx+dx,cy-dy,cy+dy)

    @staticmethod
    def pointInRect(point, rect):
        x0,x1,y0,y1 = rect
        px,py = point
        return px>x0 and px<x1 and py>y0 and py<y1

    @staticmethod
    def genNewWinPos(oldWinPos, oldFocusPos, newFocusPos):
        oldActWinPos = _23Painter.resizeRect(oldWinPos, .9)
        if _23Painter.pointInRect(newFocusPos, oldActWinPos):
            return oldWinPos
        dx,dy = _23Painter._SUB2D(newFocusPos, oldFocusPos)
        delta = (abs(dx),abs(dy))
        newWidth = newHeight = max(delta)*2
        center = newFocusPos
        x0,y0 = _23Painter._SUB2D(center, delta)
        x1,y1 = _23Painter._ADD2D(center, delta)

        newActWinPos = (x0,x1,y0,y1)
        return _23Painter.resizeRect(newActWinPos, 1.2)

    def update(self, useAnim):
        """
        Check what's new in data model and update the view.

        Params:
            useAnim(bool)   whether to use animation to illustrate the update
        """
        oldWinPos = self.winPos
        oldFocus = self.keysFocused
        key2OldDatPos = self.key2pos
        rootOldPos = self.rootPos
        oldFocusMarkerPos = self.focusMarkerPos

        treeStruct,extra = self.model.genTreeStat()
        
        newFocus = self.genNewFocus(oldFocus, treeStruct, extra)

        node2NewRawPos = self.genNode2RawPos(treeStruct)
        key2NewRawPos = self.genKey2RawPos(treeStruct, node2NewRawPos, extra)
        rootRawPos = node2NewRawPos[(0,0)]

        oldFocusPos = self.genFocusPos2(oldFocus, key2OldDatPos, rootOldPos)
        rawFocusPos = self.genFocusPos2(oldFocus, key2NewRawPos, rootRawPos)

        vecR2D = self._SUB2D(oldFocusPos, rawFocusPos)

        key2NewDatPos = self.applyDeltaToKey2pos(key2NewRawPos, vecR2D)
        rootNewPos = self._ADD2D(rootRawPos, vecR2D)

        newkeys = self.getNewKeys(key2OldDatPos, key2NewDatPos)
        key2traj = self.genKey2Traj(key2OldDatPos, key2NewDatPos)

        rootNewPos = self._ADD2D(rootRawPos, vecR2D)
        newFocusPos = self.genFocusPos2(newFocus, key2NewDatPos, rootNewPos)
        newFocusMarkerPos = newFocusPos

        newWinPos = self.genNewWinPos(oldWinPos, oldFocusPos, newFocusPos)
        winTraj = self.genNdimTrajectory(oldWinPos, newWinPos)
        focusMarkerTraj = self.genNdimTrajectory(oldFocusMarkerPos, newFocusMarkerPos)

        ### Add drawable objects.
        for newkey in newkeys:
            x,y = key2NewDatPos[newkey]
            txt = pyplot.text(x, y, newkey, fontsize=12, ha='center', va='center')
            self.key2obj[newkey] = txt
        pyplot.show()
        
        ### Repaint the marker.
        #TODO

        ### Play animation.
        animation.FuncAnimation(self.fig,
                                self._animfunc,
                                _23Painter.FrameCount,
                                interval=20,
                                fargs=(
                                    self.key2obj,
                                    self.focusMarkerObj,
                                    key2traj,
                                    winTraj,
                                    focusMarkerTraj),
                                repeat=False)
        pyplot.show()

        ### Update arguments
        self.key2pos = key2NewDatPos
        self.rootPos = rootNewPos
        self.winPos = newWinPos
        self.keysFocused = newFocus
        self.focusMarkerPos = newFocusMarkerPos
    pass


