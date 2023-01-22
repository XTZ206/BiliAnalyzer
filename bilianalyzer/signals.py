from collections import OrderedDict

from PySide6.QtCore import Signal, QObject


class UiSignals(QObject):
    updateProgressBar = Signal(int, str)
    setProgressBar = Signal(int, str)
    callErrorBox = Signal(Exception)
    showStatisticsResult = Signal(OrderedDict, list)


ui_signals = UiSignals()
