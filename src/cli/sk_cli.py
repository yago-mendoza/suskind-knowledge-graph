import cmd
import datetime

from rich import print
print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())

class Placeholder:
    def __init__(self, primary_interface):
        self.primary_interface = primary_interface
    def update(self):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        field = self.primary_interface.current_field
        name = self.primary_interface.current_node
        # 10:46:32 ~ (F/es/-w)[concept]@[(lemma)]/:
        return f"{time_str} ~ (F/w)[{field}]@[{name or ''}(lemma)]/: "

class PrimaryInterface (cmd.Cmd):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.current_node = None
        self.current_field = 'concept'
        self.placeholder = Placeholder(self)
        self.update_prompt()
    
    def update_prompt(self):
        # Default method & attribute for cmd.Cmd
        self.prompt = self.placeholder.update()

    def do_cd(self, concept_name):
        concept = self.database.get_concept(concept_name)
        if concept:
            self.current_node = concept_name
            self.current_field = 'concept'
            self.update_prompt()
        else:
            print(f"No se encontró el concepto: {concept_name}")

    def do_ls(self, arg):
        if self.current_node:
            concept = self.database[self.current_node]
            if self.current_field in ['synset', 'semset']:
                items = getattr(concept, self.current_field)
                print(', '.join(items) if items else "Lista vacía")
            else:
                print("Seleccione 'synset' o 'semset' primero con 'y' o 'e'")
        else:
            print("Seleccione un concepto primero con 'cd'")

    def do_e(self, arg):
        if self.current_node:
            self.current_field = 'semset'
            self.update_prompt()
        else:
            print("Seleccione un concepto primero con 'cd'")

    def do_y(self, arg):
        if self.current_node:
            self.current_field = 'synset'
            self.update_prompt()
        else:
            print("Seleccione un concepto primero con 'cd'")

    def do_exit(self, arg):
        print("Saliendo...")
        return True

if __name__ == "__main__":
    db = Graph('data.txt')
    db.load_from_file('kerouac.txt')
    cli = PrimaryInterface(db)
    cli.cmdloop()