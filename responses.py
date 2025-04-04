
def handleResponses(message):
    message = message.lower()
    if message == "breakfast":
        return 1
    elif message == "lunch":
        return 2
    elif message == "dinner":
        return 3
    else:
        return 4