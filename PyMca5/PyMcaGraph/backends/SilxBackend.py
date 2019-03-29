#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2019 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__doc__ = """
Silx Plot Backend.
"""

from silx.gui import qt
from silx.gui.plot import PlotWidget

class SilxBackend(PlotWidget):
    def __init__(self, *var, **kw):
        PlotWidget.__init__(self, *var, **kw)
        # No context menu by default, execute zoomBack on right click
        print("CALLED!!!!!!!!!")
        plotArea = self.getWidgetHandle()
        plotArea.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        plotArea.customContextMenuRequested.connect(self._zoomBack)

    def _zoomBack(self, pos):
        self.getLimitsHistory().pop()

    def addCurve(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.addCurve(self, *var, **kw)

    def addImage(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        if "xScale" in kw:
            xScale = kw["xScale"]
            del kw["xScale"]
        if "yScale" in kw:
            yScale = kw["yScale"]
            del kw["yScale"]
        if xScale is not None or yScale is not None:
            origin = kw.get("origin", None)
            scale = kw.get("scale", None)
            if origin is None and scale is None:
                kw["origin"] = xScale[0], yScale[0]
                kw["scale"] = xScale[1], yScale[1]
        return PlotWidget.addImage(self, *var, **kw)

    def setActiveCurve(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.setActiveCurve(self, *var, **kw)

    def setActiveImage(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.setActiveImage(self, *var, **kw)

    def insertXMarker(self, *var, **kw):
        return self.addXMarker(*var, **kw)

    def insertYMarker(self, *var, **kw):
        return self.addYMarker(*var, **kw)

    def insertMarker(self, *var, **kw):
        return self.addMarker(*var, **kw)

    def removeCurve(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.removeCurve(self, *var, **kw)

    def isActiveCurveHandlingEnabled(self):
        return self.isActiveCurveHandling()

    def enableActiveCurveHandling(self, *args, **kwargs):
        return self.setActiveCurveHandling(*args, **kwargs)

    def invertYAxis(self, *args, **kwargs):
        return self.getYAxis().setInverted(*args, **kwargs)

    def showGrid(self, flag=True):
        if flag in (0, False):
            flag = None
        elif flag in (1, True):
            flag = 'major'
        else:
            flag = 'both'
        return self.setGraphGrid(flag)

    def keepDataAspectRatio(self, *args, **kwargs):
        return self.setKeepDataAspectRatio(*args, **kwargs)

    def hideCurve(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.hideCurve(self, *var, **kw)

    def setGraphXLimits(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.setGraphXLimits(self, *var, **kw)

    def setGraphYLimits(self, *var, **kw):
        if "replot" in kw:
            del kw["replot"]
        return PlotWidget.setGraphYLimits(self, *var, **kw)

    def isDrawModeEnabled(self):
        return self.getInteractiveMode()['mode'] == 'draw'


    def setDrawModeEnabled(self, flag=True, shape='polygon', label=None,
                           color=None, **kwargs):
        if color is None:
            color = 'black'

        if flag:
            self.setInteractiveMode('draw', shape=shape,
                                    label=label, color=color)
        elif self.getInteractiveMode()['mode'] == 'draw':
            self.setInteractiveMode('select')

    def getDrawMode(self):
        mode = self.getInteractiveMode()
        return mode if mode['mode'] == 'draw' else None

    def isZoomModeEnabled(self):
        return self.getInteractiveMode()['mode'] == 'zoom'

    def setZoomModeEnabled(self, flag=True, color=None):
        if color is None:
            color = 'black'
        if flag:
            self.setInteractiveMode('zoom', color=color)
        elif self.getInteractiveMode()['mode'] == 'zoom':
            self.setInteractiveMode('select')

    def setActiveCurveColor(self, *var, **kw):
        return PlotWidget.setActiveCurveStyle(self, *var, **kw)

if __name__ == "__main__":
    def callback(ddict):
        print("RECEIVED = ", ddict)
    from silx.gui import qt
    app = qt.QApplication([])
    w = SilxBackend()
    w.setCallback(callback)
    w.addCurve([1, 2, 3], [4, 5, 6], legend="My Curve")
    w.insertXMarker(1.5, draggable=True)
    w.show()
    app.exec_()
