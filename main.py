import os
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime

# Asegúrate de que el directorio raíz del proyecto esté en el path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexical.skcomponents.skgraph import Graph as LexicalGraph
from src.lexical.skcli.SKCLI import LexicalInterface
from src.script.skcomponents.skgraph import Graph as ScriptGraph
from src.script.skcli.SKCLI import ScriptInterface

class ModeInterface(ABC):
    def __init__(self, name):
        self.name = name
        self.database_file = f"{name}.txt"

    @abstractmethod
    def run(self, graph):
        pass

class LexicalMode(ModeInterface):
    def __init__(self):
        super().__init__("lexical")

    def run(self, graph):
        interface = LexicalInterface(graph)
        interface.cmdloop()
        return interface

class ScriptMode(ModeInterface):
    def __init__(self):
        super().__init__("script")

    def run(self, graph):
        print("\033[92mQuotations mode is active.\033[0m")
        interface = ScriptInterface(graph)
        interface.cmdloop()
        return interface

class SimpleModeSelection:
    def __init__(self, modes):
        self.modes = modes

    def display_options(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[93m\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\\033[96m")
        print("\033[93mSUSKIND KNOWLEDGE GRAPH\033[96m")
        print("\033[93m/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\033[96m")
        print(f"\033[90mTip: once inside, write 'back' to return.\033[0m")
        print(f"\033[90mTip: write 'exit' to log out.\033[0m")
        print(f"\033[90m[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\033[0m")
        print("\033[95mAvailable modes:\033[0m")
        for i, mode in enumerate(self.modes.values(), 1):
            print(f"  \033[92m{i}.\033[0m {mode.name.capitalize()}")

    def select_mode(self):
        self.display_options()
        while True:
            try:
                choice = input("\033[93m  Select (1-{}): \033[0m".format(len(self.modes)))
                if choice.lower() in {'exit', 'q'}:
                    break
                else:
                    os.system('cls')
                    index = int(choice) - 1
                    if 0 <= index < len(self.modes):
                        return list(self.modes.values())[index]
                    else:
                        print("\033[91mInvalid selection. Please try again.\033[0m")
            except ValueError:
                print("\033[91mPlease enter a valid number.\033[0m")
            except EOFError:
                print("\n\033[91mExiting mode selection.\033[0m")
                return None

class GraphLoader:
    @staticmethod
    def load_graph(filename, mode):
        data_file_path = os.path.join(os.path.dirname(__file__), filename)
        data_file_path = os.path.normpath(data_file_path)
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"The file {data_file_path} does not exist.")
        
        if mode == "lexical":
            return LexicalGraph(data_file_path)
        else:
            return ScriptGraph(data_file_path)

def run_application():
    while True:
        modes = {
            'lexical': LexicalMode(),
            'script': ScriptMode()
        }

        selector = SimpleModeSelection(modes)
        selected_mode = selector.select_mode()

        if selected_mode:
            print(f"\033[92mSelected mode: {selected_mode.name.capitalize()}\033[0m")
            time.sleep(0.15)
            try:
                print("\033[93mInitializing system...\033[0m")
                time.sleep(0.15)
                
                print("\033[96mLoading graph...\033[0m")
                graph = GraphLoader.load_graph(selected_mode.database_file, selected_mode.name)
                time.sleep(0.15)
                
                interface = selected_mode.run(graph)
                if interface.should_restart:
                    continue
                else:
                    break
                
            except FileNotFoundError as e:
                print(f"\n\033[91mError: {e}")
                print(f"Make sure the file '{selected_mode.database_file}' exists in the project root directory.\033[0m")
            except Exception as e:
                print(f"\n\033[91mAn unexpected error occurred: {e}\033[0m")
        else:
            print("\033[90m\n    Terminating...\033[0m")
            break

    print()

if __name__ == '__main__':
    run_application()