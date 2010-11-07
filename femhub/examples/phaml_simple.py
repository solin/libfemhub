"""
Python version of the example "simple".
"""
import os
import base64
import hashlib
import inspect
import tempfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


from numpy import array

from phaml import Phaml
from femhub.plot import plot_mesh_mpl, plot_sln_mayavi
from femhub import Mesh

# This function is not used anywhere yet
def get_solution_points(polygons, orders):
    """
    Returns a list of x and y points for the values of the solution.
    """
    x = []
    y = []
    for e_id in polygons:
        e_x = list(polygons[e_id][:, 0])
        e_y = list(polygons[e_id][:, 1])
        x.extend(e_x)
        y.extend(e_y)
    return array(x), array(y)

def run(problem_number=1, params={}):
    """
    Allows to run phaml examples with various parameters.

    problem_number ... which example to run
    params         ... solver parameters (refinement strategy,
                       error tolerance, ...)

    Examples:

    >>> from femhub.examples.phaml_simple import run
    >>> import phaml
    >>> run(1, params = {
            "term_energy_err": 1e-6,
            "hp_strategy": phaml.HP_SMOOTH_PRED,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_SMOOTH_PRED,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_PRIOR2P_H1,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_REFSOLN_ELEM,
            })

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_file = os.path.join(current_dir, "data", "domain")
    p = Phaml(domain_file, problem_number)
    p.solve(params)
    x, y, elems, orders = p.get_mesh()
    nodes = zip(x, y)
    # Count nodes from 0:
    elems = elems - 1
    mesh = Mesh(nodes, elems, [], [], orders=orders)
    return mesh
    #polygons, orders = convert_mesh(*mesh_data)

    #f = plot_mesh_mpl(polygons, orders)
    #buffer = StringIO()
    #f.savefig(buffer, format='png', dpi=80)
    #return_png_image(buffer)


    #x, y, mesh, _ = mesh_data
    #values = p.get_solution_values(x, y)

    #mesh = [elem-1 for elem in mesh]
    #f = plot_sln_mayavi(x, y, mesh, values)
    # We need to save the image through a file, until we figure out how to
    # force mayavi to save it to the buffer directly
    #_, filename = tempfile.mkstemp("a.png")
    #f.savefig(filename)
    #buffer = StringIO()
    #buffer.write(open(filename).read())
    #return_png_image(buffer)
