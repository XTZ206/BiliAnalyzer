from PySide6.QtCore import Signal, QObject


class UiSignals(QObject):
    updateProgressBar = Signal(int)
    callDownloadError = Signal(Exception)


ui_signals = UiSignals()
