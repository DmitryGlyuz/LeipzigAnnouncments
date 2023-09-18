def run_after_confirm(message: str, func, *args, show_starting=True):
    user_input = input(f"Press Y if you want to {message}: ")
    if user_input.lower() == 'y':
        if show_starting:
            print("Starting...")
        func(*args)
        print("Done!\n")
    else:
        print("Ok, the action is cancelled.")
