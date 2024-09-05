import sys
import os
from colorama import init, Fore, Style

# Asegúrate de que el directorio raíz del proyecto esté en el path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.skcomponents.skgraph import Graph as LexicalGraph
from src.skcli.SKCLI import LexicalInterface

# Inicializar colorama
init(autoreset=True)

def print_color(text, color):
    """
    Imprime texto en color usando colorama.
    :param text: El texto a imprimir
    :param color: El color deseado (debe ser un atributo de Fore)
    """
    print(f"{color}{text}{Style.RESET_ALL}")

class GraphLoader:
    @staticmethod
    def load_graph(filename):
        """
        Carga el grafo desde un archivo.
        :param filename: Nombre del archivo de la base de datos
        :return: Instancia de LexicalGraph
        """
        data_file_path = os.path.join(os.path.dirname(__file__), filename)
        data_file_path = os.path.normpath(data_file_path)
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"The file {data_file_path} does not exist.")
        
        return LexicalGraph(data_file_path)

def run_application():
    """
    Función principal que ejecuta la aplicación.
    """
    database_file = "lexical.txt"

    print_color("Initializing system...", Fore.BLUE)
    print_color("Loading graph...", Fore.GREEN)

    try:
        # Cargar el grafo
        graph = GraphLoader.load_graph(database_file)
        
        # Iniciar la interfaz léxica
        interface = LexicalInterface(graph)
        interface.cmdloop()
    except FileNotFoundError as e:
        print_color(f"Error: {e}", Fore.RED)
        print_color(f"Make sure the file '{database_file}' exists in the project root directory.", Fore.RED)
    except Exception as e:
        print_color(f"An unexpected error occurred: {e}", Fore.RED)

if __name__ == '__main__':
    run_application()