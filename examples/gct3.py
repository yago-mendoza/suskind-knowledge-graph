from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Lista de ejemplo con palabras en español.
palabras = ['cabra', 'cabrales', 'cabify', 'cable', 'cacerola']

# Crear un completador con la lista de palabras.
completador_palabras = WordCompleter(palabras)

# Crear una sesión de prompt.
session = PromptSession(completer=completador_palabras)

def main():
    while True:
        try:
            # Usar la sesión para obtener la entrada del usuario con autocompletado.
            entrada = session.prompt('>> enter ')
            print(f"Has seleccionado: {entrada}")
        except KeyboardInterrupt:
            # Salir del bucle si se detecta una interrupción por teclado (Ctrl+C).
            break
        except EOFError:
            # Salir del bucle si se detecta un fin de archivo (Ctrl+D).
            break

    print("Autocompletado terminado.")

if __name__ == '__main__':
    main()