import colorama
from literature_explorer import LiteratureExplorer

def main():
    colorama.init(autoreset=True)
    try:
        LiteratureExplorer().cmdloop()
    except Exception as e:
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"An unexpected error occurred: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()