from _23TreeModel import _23TreeModel
from _23TreeView import _23Painter

class _23TreeVisualizer():
    """
    2-3 Tree visualizer, what users finally interact with.
    """
    def __init__(self):
        self.animMode = ''

        # Stat code:
        # 0: idle
        # 1: in an insertion
        # 2: in an deletion
        self.stat = 0

        self.model = _23TreeModel()
        self.painter = _23Painter(self.model)

        pass

    def show(self):
        """Show the tree in a figure."""
        self.painter.update(False)

    def animOn(self, cmd='a'):
        """
        Turn animation on and set animation mode.

        Params:
            cmd(str)    animation mode (see NOTE)

        NOTE:
            2 modes are available:
            - 'a'   complete animation (default)
            - 'aa'  step-by-step animation
        """
        if cmd=='a':
            raise Exception('Not implemented')

        if cmd not in ['a','aa']:
            print('Invalid animation mode: {0}'.format(cmd))
            return
        self.animMode = cmd

    def animOff(self):
        """Turn animation off."""
        self.animMode = ''

    def step(self):
        """Go 1 step further."""
        if self.stat == 0:
            print('No operation in progress.')
            return
        
        finished = self.model.step()
        if finished:
            self.stat = 0
        self.painter.update(True)

    def add(self, newkey, animCtrl=None):
        """
        Start an insertion.

        Params:
            newkey(object)  the key you wanna insert
            animCtrl(str)   extra command to change animation mode(see NOTE)

        NOTE:
            The param *animCtrl* controls animation mode like this:
            - None  Keep the current mode (default)
            - ''    Disable animation. This is similar to:
                        ...
                        animOff()
                        add(newkey)
                        ...
            - 'a'   Use complete animation. This is similar to:
                        ...
                        animOn('a')
                        add(newkey)
                        ...
            - 'aa'  Use step-by-step animation. This is similar to:
                        ...
                        animOn('aa')
                        add(newkey)
                        ...
        """
        if self.stat != 0:
            print('Cannont do that. One operation is in progress.')
            return

        if animCtrl not in [None, '', 'a', 'aa']:
            print('Invalid animCtrl arg: {0}'.format(animCtrl))
            return

        if animCtrl == '':
            self.animOff()
            self.add(newkey)
            return

        if animCtrl != None:
            self.animOn(animCtrl)
            self.add(newkey)
            return

        self.model.startInsert(newkey)
        
        if self.animMode == 'aa':
            self.stat = 1
            self.painter.update(True)
            return

        if self.animMode == 'a':
            finished = False
            while True:
                self.painter.update(True)
                if finished: break
                finished = self.model.step()
            return

        if self.animMode == '':
            while True:
                finished = self.model.step()
                if finished: break
            self.painter.update(False)
            return

        assert False
        
    def delete(self, oldkey, animCtrl=None):
        """
        Start an deletion.

        Params:
            oldkey(object)  the key you wanna delete
            animCtrl(str)   extra command to change animation mode(see NOTE)

        NOTE:
            The param *animCtrl* controls animation mode like this:
            - None  Keep the current mode (default)
            - ''    Disable animation. This is similar to:
                        ...
                        animOff()
                        add(oldkey)
                        ...
            - 'a'   Use complete animation. This is similar to:
                        ...
                        animOn('a')
                        delete(oldkey)
                        ...
            - 'aa'  Use step-by-step animation. This is similar to:
                        ...
                        animOn('aa')
                        delete(oldkey)
                        ...
        """
        print('Not implemented')
        return
        ###TODO

        if self.stat != 0:
            print('Cannont do that. One operation is in progress.')
            return

        if animCtrl not in [None, '', 'a', 'aa']:
            print('Invalid animCtrl arg: {0}'.format(animCtrl))
            return

        if animCtrl == '':
            self.animOff()
            self.delete(oldkey)
            return

        if animCtrl != None:
            self.animOn(animCtrl)
            self.delete(oldkey)
            return

        self.model.startDelete(oldkey)
        
        if self.animMode == 'aa':
            self.stat = 2
            self.painter.update(True)
            return

        if self.animMode == 'a':
            finished = False
            while True:
                self.painter.update(True)
                if finished: break
                finished = self.model.step()
            return

        if self.animMode == '':
            while True:
                finished = self.model.step()
                if finished: break
            self.painter.update(False)
            return

        assert False
