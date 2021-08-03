"""Module with implementation of measure methods"""

import itertools

import skimage.measure as skimage_measure

from ...utilities import Task

from ..create import Region,Block

def skimeasure():
    """
    Public method to create a dictionary of actions
    """
    tasklist = ['region','block']

    actions = {task: eval(task).copy() for task in tasklist}

    for task in actions.values(): task.actions = actions

    return actions

@Task(unit=Region)
def region(self,unit,lsetkey,labelkey):
    """
    Measure properties for a region

    Parameters
    ----------
    unit     : Region object

    lsetkey  : key to the level-set/binary data

    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties

    """
    listprops = self.actions['block'](unit.blocklist,lsetkey,labelkey)

    listprops = list(itertools.chain.from_iterable(listprops))

    return listprops

@Task(unit=Block)
def block(self,unit,lsetkey,labelkey):
    """
    Measure properties for a unit

    Parameters
    ----------
    unit     : Block object

    lsetkey  : key to the level-set/binary data

    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties

    """
    unit[labelkey] = skimage_measure.label(unit[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(unit[labelkey].astype(int))

    listprops = [{'area' : props['area']*unit.dx*unit.dy*unit.dz} for props in listprops]

    return listprops