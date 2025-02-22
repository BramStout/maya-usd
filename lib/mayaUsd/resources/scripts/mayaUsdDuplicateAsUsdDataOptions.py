#
# Copyright 2022 Autodesk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import maya.cmds as cmds
import maya.mel as mel

from mayaUsdLibRegisterStrings import getMayaUsdLibString
from mayaUsdMergeToUSDOptions import getDefaultMergeToUSDOptionsDict
import mayaUsdOptions

from functools import partial


_kDuplicateAsUsdDataOptionsHelpContentId = 'UsdEditDuplicateAsMaya'

def showDuplicateAsUsdDataOptions():
    """
    Shows the duplicate-as-Usd-data options dialog.
    """

    windowName = "DuplicateAsUsdDataOptionsDialog"
    if cmds.window(windowName, query=True, exists=True):
        if cmds.window(windowName, query=True, visible=True):
            return
        # If it exists but is not visible, assume something wrong happened.
        # Delete the window and recreate it.
        cmds.deleteUI(windowName)

    window = cmds.window(windowName, title=getMayaUsdLibString("kDuplicateAsUsdDataOptionsTitle"), widthHeight=mayaUsdOptions.defaultOptionBoxSize())
    _createDuplicateAsUsdDataOptionsDialog(window)


def _createDuplicateAsUsdDataOptionsDialog(window):
    """
    Creates the duplicate-as-Usd-data dialog.
    """

    windowLayout = cmds.setParent(query=True)

    menuBarLayout = cmds.menuBarLayout(parent=windowLayout)

    windowFormLayout = cmds.formLayout(parent=windowLayout)

    subFormLayout = cmds.formLayout(parent=windowFormLayout)
    subScrollLayout = cmds.scrollLayout('DuplicateAsUsdDataOptionsDialogSubScrollLayout', cr=True, bv=True)
    cmds.formLayout(subFormLayout, edit=True,
        attachForm=[
            (subScrollLayout,       "top",      0),
            (subScrollLayout,       "bottom",   0),
            (subScrollLayout,       "left",     0),
            (subScrollLayout,       "right",    0)]);
    subLayout = cmds.columnLayout("DuplicateAsUsdDataOptionsDialogSubLayout", adjustableColumn=True)

    optionsText = getDuplicateAsUsdDataOptionsText()
    _fillDuplicateAsUsdDataOptionsDialog(subLayout, optionsText, "post")

    menu = cmds.menu(label=getMayaUsdLibString("kEditMenu"), parent=menuBarLayout)
    cmds.menuItem(label=getMayaUsdLibString("kSaveSettingsMenuItem"), command=_saveDuplicateAsUsdDataOptions)
    cmds.menuItem(label=getMayaUsdLibString("kResetSettingsMenuItem"), command=partial(_resetDuplicateAsUsdDataOptions, subLayout))

    cmds.setParent(menuBarLayout)
    if _hasDuplicateAsUsdDataOptionsHelp():
        menu = cmds.menu(label=getMayaUsdLibString("kHelpMenu"), parent=menuBarLayout)
        cmds.menuItem(label=getMayaUsdLibString("kHelpDuplicateAsUsdDataOptionsMenuItem"), command=_helpDuplicateAsUsdDataOptions)

    buttonsLayout = cmds.formLayout(parent=windowFormLayout)

    applyText  = getMayaUsdLibString("kApplyButton")
    closeText = getMayaUsdLibString("kCloseButton")
    # Use same height for buttons as in Maya option boxes.
    bApply     = cmds.button(label=applyText, width=100, height=26, command=_saveDuplicateAsUsdDataOptions)
    bClose     = cmds.button(label=closeText, width=100, height=26, command=partial(_closeDuplicateAsUsdDataOptionsDialog, window))

    spacer = 8      # Same spacing as Maya option boxes.
    edge   = 6

    cmds.formLayout(buttonsLayout, edit=True,
        attachForm=[
            (bClose,    "bottom", edge),
            (bClose,    "right",  edge),

            (bApply,    "bottom", edge),
            (bApply,    "left",   edge),
        ],
        attachPosition=[
            (bClose,    "left",   spacer/2, 50),
            (bApply,    "right",  spacer/2, 50),
        ])

    cmds.formLayout(windowFormLayout, edit=True,
        attachForm=[
            (subFormLayout,         'top',      0),
            (subFormLayout,         'left',     0),
            (subFormLayout,         'right',    0),
            
            (buttonsLayout,         'left',     0),
            (buttonsLayout,         'right',    0),
            (buttonsLayout,         'bottom',   0),
        ],
        attachControl=[
            (subFormLayout,         'bottom',   edge, buttonsLayout)
        ])

    cmds.showWindow()


def _closeDuplicateAsUsdDataOptionsDialog(window, data=None):
    """
    Reacts to the duplicate-as-Usd-data options dialog being closed by the user.
    """
    cmds.deleteUI(window)


def _saveDuplicateAsUsdDataOptions(data=None):
    """
    Saves the duplicate-as-Usd-data options as currently set in the dialog.
    The MEL receiveDuplicateAsUsdDataOptionsTextFromDialog will call setDuplicateAsUsdDataOptionsText.
    """
    mel.eval('''mayaUsdTranslatorExport("", "query=all;!output", "", "receiveDuplicateAsUsdDataOptionsTextFromDialog");''')


def _resetDuplicateAsUsdDataOptions(subLayout, data=None):
    """
    Resets the duplicate-as-Usd-data options in the dialog.
    """
    optionsText = mayaUsdOptions.convertOptionsDictToText(getDefaultDuplicateAsUsdDataOptionsDict())
    _fillDuplicateAsUsdDataOptionsDialog(subLayout, optionsText, "fill")


def _fillDuplicateAsUsdDataOptionsDialog(subLayout, optionsText, action):
    """
    Fills the duplicate-as-Usd-data options dialog UI elements with the given options.
    """
    cmds.setParent(subLayout)
    mel.eval(
        '''
        mayaUsdTranslatorExport("{subLayout}", "{action}=all;!output", "{optionsText}", "")
        '''.format(optionsText=optionsText, subLayout=subLayout, action=action))


def _hasDuplicateAsUsdDataOptionsHelp():
    """
    Returns True if the help topic for the options is available in Maya.
    """
    # Note: catchQuiet returns 0 or 1, not the value, so we use a dummy assignment
    #       to produce the value to be returned by eval().
    url = mel.eval('''catchQuiet($url = `showHelp -q "''' + _kDuplicateAsUsdDataOptionsHelpContentId + '''"`); $a = $url;''')
    return bool(url)

def _helpDuplicateAsUsdDataOptions(data=None):
    """
    Shows help on the duplicate-as-Usd-data options dialog.
    """
    cmds.showHelp(_kDuplicateAsUsdDataOptionsHelpContentId)


def _getDuplicateAsUsdDataOptionsVarName():
    """
    Retrieves the option var name under which the duplicate-as-Usd-data options are kept.
    """
    return "mayaUsd_DuplicateAsUsdDataOptions"


def getDuplicateAsUsdDataOptionsText():
    """
    Retrieves the current duplicate-as-Usd-data options as text with column-spearated key/value pairs.
    """
    return mayaUsdOptions.getOptionsText(
        _getDuplicateAsUsdDataOptionsVarName(),
        getDefaultDuplicateAsUsdDataOptionsDict())
    

def setDuplicateAsUsdDataOptionsText(optionsText):
    """
    Sets the current duplicate-as-Usd-data options as text with column-spearated key/value pairs.
    Called via receiveDuplicateAsUsdDataOptionsTextFromDialog in MEL, which gets called via
    mayaUsdTranslatorExport in query mode.
    """
    mayaUsdOptions.setOptionsText(_getDuplicateAsUsdDataOptionsVarName(), optionsText)


def getDefaultDuplicateAsUsdDataOptionsDict():
    """
    Retrieves the default duplicate-as-Usd-data options.
    """
    # For now, the duplicate and merge options defaults are the same.
    return getDefaultMergeToUSDOptionsDict()
