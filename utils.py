def get_choice(title, options):
    """
    Handle a list of text options to generate a 
    menu, validate the input and return the result index.

    Args:
    title = Title printed before the strings.
    options = List of strings to display.
    """

    while (True):
        print(f"\n{title}")
        for i, option in enumerate(options, 1):
            print(f"{i}) {option}")

        try:
            choice = int(input(f"Choose (1-{len(options)}): ")) - 1
            if 0 <= choice < len(options):
                return choice
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")