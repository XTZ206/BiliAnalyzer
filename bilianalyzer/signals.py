from collections import OrderedDict

from PySide6.QtCore import Signal, QObject


class UiSignals(QObject):
    updateDownloadProgress = Signal(int)
    updateAnalyzeProgress = Signal(int)
    callDownloadError = Signal(Exception)
    showAnalyzeResult = Signal(OrderedDict, list[str])


ui_signals = UiSignals()
