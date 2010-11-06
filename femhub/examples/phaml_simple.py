"""
Python version of the example "simple".
"""
import os
import base64
import hashlib
import inspect

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


from numpy import array

from phaml import Phaml
from femhub.plot import plot_mesh_mpl, plot_sln_mayavi

def convert_mesh(x, y, elems, elems_orders):
    """
    Convert the mesh from Phaml representation to femhub representation.
    """
    polygons = {}
    for n, elem in enumerate(elems):
        polygons[n] = array([ [x[i-1], y[i-1]] for i in elem ])
    orders = {}
    for n, order in enumerate(elems_orders):
        orders[n] = order
    return polygons, orders

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
    mesh_data = p.get_mesh()
    polygons, orders = convert_mesh(*mesh_data)

    import matplotlib
    matplotlib.use("Agg")
    f = plot_mesh_mpl(polygons, orders)
    #f.savefig("mesh.png")
    buffer = StringIO()
    f.savefig(buffer, format='png', dpi=80)
    return_png_image(buffer)


    x, y, mesh, _ = mesh_data
    values = p.get_solution_values(x, y)

    mesh = [elem-1 for elem in mesh]
    f = plot_sln_mayavi(x, y, mesh, values)
    #f.savefig("sln.png")
    buffer = StringIO()
    f.savefig(buffer, format='png', dpi=80)
    return_png_image(buffer)

def return_png_image(png_data):
    """
    Returns the PNG image in png_data into the online lab as a result.

    png_data ... StringIO() instance (or similar)

    You can call this function as many times as you want, and it will keep
    appending new images at the end of the output cell.
    """
    frame = inspect.currentframe().f_back

    # FIXME: This depends on where you call the return_png_image() function
    # from:
    frame = frame.f_back

    try:
        try:
            plots = frame.f_globals['__plots__']
        except KeyError:
            plots = []

        value = png_data.getvalue()

        data = base64.b64encode(value)
        hash = hashlib.sha1(data).hexdigest()

        plots.append({
            'data': data,
            'size': len(value),
            'type': 'image/png',
            'encoding': 'base64',
            'checksum': hash,
        })

        frame.f_globals['__plots__'] = plots
    finally:
        del frame
