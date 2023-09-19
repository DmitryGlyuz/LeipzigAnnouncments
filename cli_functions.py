def run_after_confirm_screen(message: str, func, *args, show_starting=True):
    if message[0].isupper():
        original_letter = message[0]
        lowercase_letter = original_letter.lower()
        message = message.replace(original_letter, lowercase_letter, 1)
    user_input = input(f"Press Y if you want to {message}: ")
    if user_input.lower() == 'y':
        if show_starting:
            print("Starting...")
        func(*args)
        print("Done!\n")
    else:
        print("Ok, the action is cancelled.")
