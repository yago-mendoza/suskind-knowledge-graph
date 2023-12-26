
from src.skcomponents.skgraph import Graph

import cmd
import datetime
from rich import print

# los argumentos -> library argparse, action, help 


class Placeholder(str):

    def __init__(self, node=None, fields=None):
        self.lang = 'lang' or node.lang
        self.type = 'type' or node.type
        self.name = 'name' or node.name
        self.lemma = 'lemma' or node.lemma
        self.fields = fields or []
    
    def get_string(self):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        fields = '[' + '/'.join(self.fields) + ']'
        return f"{time_str} ~ [{self.lang}][{self.type}]@[{self.name}({self.lemma or ''})]/{fields or ''}: "
        
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
        self.prompt = self.placeholder.get_string()

    def do_set(self, element):
        if element in self.graph.list_langs():
            self.placeholder.lang = element

        elif element in self.graph.list_types():
            self.placeholder.type = type

        elif element in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']:
            self.placeholder.fields.append(element)

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