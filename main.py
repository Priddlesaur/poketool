from command_line_tools import print_success
from history import load_history_file
from menu import show_main_menu

def main():
    print_success("Welcome to the Pokémon Tool!")

    # Load the history file
    print("Loading history...")
    load_history_file()

    # ASCII art of a Pikachu :)
    print_success("""
    `;-.          ___,
      `.`\\_...._/`.-"`
        \\        /      ,
        /()   () \\    .' `-._
       |)  .    ()\\  /   _.'
       \\  -'-     ,; '. <
        ;.__     ,;|   > \\
       / ,    / ,  |.-'.-'
      (_/    (_/ ,;|.<`
        \\    ,     ;-`
         >   \\    /
        (_,-'`> .'
             (_,'
    """)

    # Main application loop. The show_main_menu function returns False when the user wants to exit.
    while show_main_menu():
        pass

    # Show a goodbye message when the user exits
    print_success("""\n
         _______  _______  _______  ______   _______  __   __  _______  __  
        |       ||       ||       ||      | |  _    ||  | |  ||       ||  | 
        |    ___||   _   ||   _   ||  _    || |_|   ||  |_|  ||    ___||  | 
        |   | __ |  | |  ||  | |  || | |   ||       ||       ||   |___ |  | 
        |   ||  ||  |_|  ||  |_|  || |_|   ||  _   | |_     _||    ___||__| 
        |   |_| ||       ||       ||       || |_|   |  |   |  |   |___  __  
        |_______||_______||_______||______| |_______|  |___|  |_______||__| 
    """)

# Run the main function when the script is executed
if __name__ == '__main__':
    main()