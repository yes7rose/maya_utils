# encoding: utf-8

class MayaStandAlone(object):
    """ stand alone maya"""

    def __init__(self):
        import maya.standalone as mayaAlone
        self.mayaAlone = mayaAlone

        print("init maya")
        self.mayaAlone.initialize()
        import maya.cmds as mcmds

        self.cmds = mcmds

    def __del__(self):
        print("uninit maya")
        self.cmds.file(new=True, force=True)
        self.cmds.quit(force=True)
        self.mayaAlone.uninitialize()

if __name__ == '__main__':

    m = MayaStandAlone()
    m.cmds.file(new=True, force=True)
    g = m.cmds.group(name = "test", empty=True)
    print(g)
    m.cmds.quit(force=True)
