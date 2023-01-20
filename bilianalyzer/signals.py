from collections import OrderedDict

from PySide6.QtCore import Signal, QObject


class UiSignals(QObject):
    updateDownloadProgress = Signal(int)
    updateAnalyzeProgress = Signal(int)
    callErrorBox = Signal(Exception)
    showAnalyzeResult = Signal(OrderedDict, list[str])


ui_signals = UiSignals()
