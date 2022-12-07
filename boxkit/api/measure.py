""" Module with implemenation of region methods"""

import numpy

from ..resources import stencils

from ..library import Process

from . import create


@Process(stencils=[stencils.skimeasure])
def bubbles(self, dataframes, lsetkey, **attributes):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    dataframes : list of Dataset objects
    lsetkey    : key containing level-set/binary data

    Returns
    -------
    listbubbles : list of bubble properties
    """

    regionlist = []
    bubblekey = "bubble"

    for dataset in dataframes:
        dataset.addvar(bubblekey, dtype=numpy.int)
        regionlist.append(create.region(dataset, **attributes))

    listbubbles = self.tasks["skimeasure"]["region"](regionlist, lsetkey, bubblekey)

    for dataset in dataframes:
        dataset.delvar(bubblekey)

    return listbubbles
