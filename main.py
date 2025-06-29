import sys
from datetime import datetime

from loguru import logger
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from src.config import cfg
from src.ui import MainWindow


def setup_logger() -> None:
    logger.remove()
    format = "<g>{time:HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c>:<c>{function}:{line}</c> | {message}"

    # pyinstaller 打包并禁用控制台后, sys.stdout 为 None
    if sys.stdout:
        logger.add(
            sys.stdout,
            format=format,
            level="DEBUG",
            colorize=True,
        )

    now = datetime.now()
    logger.add(
        f"logs/{now:%Y-%m-%d}/{now:%Y-%m-%d_%H-%M-%S}.log",
        format=format,
        level="DEBUG",
        diagnose=True,
    )


if __name__ == "__main__":
    # --- 启用高 DPI 支持 ---
    if attr := getattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling", None):
        QApplication.setAttribute(attr)
    if attr := getattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps", None):
        QApplication.setAttribute(attr)
    if attr := getattr(getattr(Qt, "HighDpiScaleFactorRoundingPolicy", None), "PassThrough", None):
        QApplication.setHighDpiScaleFactorRoundingPolicy(attr)

    setup_logger()

    app = QApplication(sys.argv)
    window = cfg.main_window = MainWindow()
    window.show()
    sys.exit(app.exec())
