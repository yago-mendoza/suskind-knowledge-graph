import cmd
import datetime
from ..skcomponents.main import *
from rich import print

class Placeholder:
    def __init__(self, primary_interface):
        self.primary_interface = primary_interface
    def update(self):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        field = self.primary_interface.current_field
        name = self.primary_interface.current_node
        return f"{time_str} ~ (F/w)[{field}]@[{name or ''}(lemma)]/: " # 10:46:32 ~ (F/es/-w)[concept]@[(lemma)]/:

class PrimaryInterface (cmd.Cmd):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.current_node = None
        self.current_field = 'concept'
        self.placeholder = Placeholder(self)
        self.update_prompt()
        self.lang = ['es']
        self.type = ['n']
    
    def update_prompt(self):
        # Default method & attribute for cmd.Cmd
        self.prompt = self.placeholder.update()

    def do_set(self, property):
        if property in self.database.list_langs():
            self.lang.append(property)
        elif property in self.database.list_types():
            self.lang.append(property)

    def do_cd(self, concept_name):
        concept = self.database.find(self.lang, self.type, concept_name, '')
        if concept:
            self.current_node = concept_name
            self.current_field = 'concept'
            self.update_prompt()
        else:
            print(f"No se encontró el concepto: {concept_name}")

    def do_exit(self, arg):
        print("Saliendo...")
        return True

if __name__ == "__main__":
    G = Graph('data.txt')
    cli = PrimaryInterface(G)
    cli.cmdloop()