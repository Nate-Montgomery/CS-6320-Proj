def log_message(message):
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def format_message(content, author):
    """Formats a message for display."""
    return f"{author}: {content}"

def handle_error(error):
    """Handles errors and logs them."""
    log_message(f"Error occurred: {error}")