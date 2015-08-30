class _23TreeVisualizer():
    """
    2-3 Tree visualizer, what users finally interact with.
    """
    def __init__(self):
        pass

    def show(self):
        """Show the tree in a matplotlib figure."""
        pass

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
        pass

    def animOff(self):
        """Turn animation off."""
        pass

    def step(self):
        """Go 1 step further."""
        pass

    def stepback(self):
        """Go back for 1 step."""
        pass

    def add(self, newkey, animCtrl=''):
        """
        Start an insertion.

        Params:
            newkey(object)  the key you wanna insert
            animCtrl(str)   extra command to change animation mode(see NOTE)

        NOTE:
            The param *animCtrl* controls animation mode like this:
            - ''    Keep the current mode (default), or
            - 'a'   Use complete animation. This is equal to:
                        ...
                        animOn('a')
                        add(newkey)
                        ...
            - 'aa'  Use step-by-step animation. This is equal to:
                        ...
                        animOn('aa')
                        add(newkey)
                        ...
        """
        pass

    def delete(self, oldkey, animCtrl=''):
        """
        Start an deletion.

        Params:
            oldkey(object)  the key you wanna delete
            animCtrl(str)   extra command to change animation mode(see NOTE)

        NOTE:
            The param *animCtrl* controls animation mode like this:
                - ''    Keep the current mode (default), or
                - 'a'   Use complete animation. This is equal to:
                            ...
                            animOn('a')
                            delete(oldkey)
                            ...
                - 'aa'  Use step-by-step animation. This is equal to:
                            ...
                            animOn('aa')
                            delete(oldkey)
                            ...
        """
        pass


