from numpy import array

from plot import return_mayavi_figure, plot_sln_mayavi

class Solution(object):

    def __init__(self, mesh):
        self._mesh = mesh
        self._values = None

    def _need_values(self):
        if self._values is None:
            raise Exception("You need to call set_values() first")

    @property
    def mesh(self):
        return self._mesh

    def get_xy_points(self):
        x = [n[0] for n in self.mesh.nodes]
        y = [n[1] for n in self.mesh.nodes]
        return array(x), array(y)

    def set_values(self, values):
        self._values = values

    def plot(self):
        self._need_values()
        x, y = self.get_xy_points()
        elems = self._mesh.elems
        f = plot_sln_mayavi(x, y, elems, self._values)
        return_mayavi_figure(f)
