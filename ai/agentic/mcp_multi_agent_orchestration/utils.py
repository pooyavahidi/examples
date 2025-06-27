import logging
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    """Custom formatter with timestamp and colors for different log levels."""

    def format(self, record):
        # Format timestamp as [MM/DD/YY HH:MM:SS]
        timestamp = datetime.fromtimestamp(record.created).strftime(
            "[%m/%d/%y %H:%M:%S]"
        )

        # Color codes for different levels using Colors class
        colors = {
            "DEBUG": Colors.BLUE,
            "INFO": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.MAGENTA,
        }

        color = colors.get(record.levelname, "")

        # Format: [timestamp] LEVEL     message     filename:line
        formatted_message = (
            f"{timestamp} {color}{record.levelname:<8}{Colors.RESET} "
            f"{record.getMessage():<40} {record.filename}:{record.lineno}"
        )

        return formatted_message


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with custom formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger


# Color printing functions
def cprint(
    text: str,
    color: str = "white",
    bold: bool = False,
    underline: bool = False,
) -> None:
    """Print text with specified color and formatting.
    Args:
        text: The text to print
        color: Color name (red, green, yellow, blue, magenta, cyan, white)
        bold: Whether to print in bold
        underline: Whether to underline the text
    """
    color_codes = {
        "red": Colors.RED,
        "green": Colors.GREEN,
        "yellow": Colors.YELLOW,
        "blue": Colors.BLUE,
        "magenta": Colors.MAGENTA,
        "cyan": Colors.CYAN,
        "white": Colors.WHITE,
    }

    color_code = color_codes.get(color.lower(), Colors.WHITE)

    # Build format string
    format_codes = color_code
    if bold:
        format_codes += Colors.BOLD
    if underline:
        format_codes += Colors.UNDERLINE

    print(f"{format_codes}{text}{Colors.RESET}")
