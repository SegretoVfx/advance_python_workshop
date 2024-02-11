# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# **********************************************************************************
from maya import cmds


def set_color(ctrl_list, color):
    """Set color of selected controllers

    Args:
        ctrl_list (list[str]): List of selected controllers
        color (int): index of the desired color
    """
    color_dic = {
        1: 4,
        2: 13,
        3: 25,
        4: 17,
        5: 17,
        6: 15,
        7: 6,
        8: 16,
    }

    for ctrl_name in ctrl_list:
        cmds.setAttr(f"{ctrl_name}Shape.overrideEnabled", 1)
        cmds.setAttr(f"{ctrl_name}Shape.overrideColor", color_dic[color])
