from matplotlib import pyplot
from _23Tree import _23Set


class _23Painter:
    ArrowStartOffsets = {
        1:{
            0:-0.25,
            1:+0.25,},
        2:{
            0:-0.5,
            1:+0.0,
            2:+0.5,}}

    @staticmethod
    def drawKeys(keys, bx, by):
        keycount = len(keys)
        strkeys = [str(k) for k in keys]
        if keycount == 2:
            pyplot.text(bx-0.175, by, strkeys[0], fontsize='12', ha='center', va='center')
            pyplot.text(bx, by, ',', fontsize='12', ha='center', va='center')
            pyplot.text(bx+0.175, by, strkeys[1], fontsize='12', ha='center', va='center')
        elif keycount == 1:
            pyplot.text(bx, by, strkeys[0], fontsize='12', ha='center', va='center')
        else:
            raise Exception()

    def __init__(self):
        self.figid = hash(self)
        self.fig = pyplot.figure(self.figid)

    def __del__(self):
        pyplot.close(self.figid)

    def paintTreeFrom(self, ttnode):
        self.Xdrawing = 1.0
        self.topReached = 1.0
        self.botReached = 1.0
        self.lftReached = 1.0
        self.rgtReached = 1.0
        pyplot.cla()
        if ttnode!=None:
            self.drawTreeStep(ttnode)
        else:
            pyplot.text(1,1,'EMPTY')
        pyplot.plot(0,0,'w')
        pyplot.plot(self.rgtReached+1,0,'w')
        pyplot.plot(0,self.topReached+1,'w')
        pyplot.plot(self.rgtReached+1,self.topReached+1,'w')
        pyplot.axis('tight')

    def drawTreeStep(self, ttnode):
        if ttnode.isLeaf():
            crty = 1.0
            crtx = self.Xdrawing
            self.Xdrawing += 2.0
        else:
            chld_xs = []
            for child in ttnode.childs:
                chldx, chldy = self.drawTreeStep(child)
                crty = chldy+1
                chld_xs.append(chldx)
            crtx = sum(chld_xs) / len(chld_xs)
            keycnt = len(ttnode.keys)
            for chld_i,chldx in enumerate(chld_xs):
                self.drawArrow(crtx, crty, chldx, chldy, keycnt, chld_i)

        self.topReached = max(self.topReached, crty)
        self.botReached = min(self.botReached, crty)
        self.lftReached = min(self.lftReached, crtx)
        self.rgtReached = max(self.rgtReached, crtx)
        self.drawKeys(ttnode.keys, crtx, crty)
        return crtx,crty

    def drawArrow(self, x0, y0, x1, y1, n0keycount, n1chldidx):
        x0 += self.ArrowStartOffsets[n0keycount][n1chldidx]
        y0 -= 0.1
        y1 += 0.1
        pyplot.arrow(x0, y0, x1-x0, y1-y0)


class Visual23Tree(_23Set):
    def __init__(self):
        super().__init__()
        self.painter = _23Painter()

    def show(self):
        self.painter.paintTreeFrom(self.root)

    def insert(self, x):
        super().insert(x)
        self.show()

    def delete(self, x):
        super().delete(x)
        self.show()
        