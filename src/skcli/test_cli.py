
from src.skcomponents.skgraph import Graph

import cmd
import datetime
import argparse
from rich import print

# los argumentos -> library argparse, action, help 

class Placeholder(str):

    def __init__(self, cmd):
        self.cmd = cmd  # static
        self.lang, self.type, self.name, self.lemma = 'lang', 'type', 'name', 'lemma'  # updated through update(node)
        self.fields = []  # starts out empty

    def update(self, node):
        self.node = node
        self.lang, self.type, self.name, self.lemma = node.identify()

    def get_string(self):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        fields = '[' + '/'.join(self.fields) + ']'
        return f"{time_str} ~ [{self.lang}][{self.type}]@[{self.name}({self.lemma or ''})]/{fields or ''}:"

class PrimaryInterface (cmd.Cmd):

    def __init__(self, graph):
        super().__init__()
        self.G = graph
        self.placeholder = Placeholder(self)
        self.filters = FilterManager(self)
    
        self.set_random_node()  # inicializamos el PlaceHolder en un nodo aleatorio

    def set_random_node(self):
        self.placeholder.update(self.G.random())

    def do_set(self, element):
        if element in self.graph.list_langs():
            self.placeholder.lang = element

        elif element in self.graph.list_types():
            self.placeholder.type = type

        elif element in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']:
            self.placeholder.fields.append(element)

    def do_cd(self, concept_name):
        concept = self.database.find(self.lang, self.type, concept_name, '')
        if concept:
            self.current_node = concept_name
            self.current_field = 'concept'
            self.update_prompt()
        else:
            print(f"No se encontró el concepto: {concept_name}")



class FilterManager:

    def __init__(self, cmd):
        self.cmd = cmd
        self.filters = {
            'f1': "type('w').lang('es')",
            'f2': "starts('clar')"
        }
    
    def add_filter(self, filter_name, filter_def):
        self.filters[filter_name] = filter_def

    def remove_filter(self, filter_name):
        if filter_name in self.filters:
            del self.filters[filter_name]
    
    def show_filter(self):
        return self.filters

    def do_exit(self, arg):
        print("Saliendo...")
        return True
    
class CLIFilter(cmd.Cmd):
    prompt = '>'
    def __init__(self, filter_manager):
        super().__init__()
        self.filter_manager = filter_manager

    def do_filter(self, line):
        args = line.split()
        if "-e" in args:
            editor = CLIFilter(self.filter_manager)
            editor.cmdloop("Entered editor mode on filters:")
        else:
            self.show_filters()
    
    def show_filters(self):
        print("| Filters:")
        for name, definition in self.filter_manager.list_filters().items():
            print(f"| {name}/{definition}")

    def do_exit(self, line):
        """Exit the application."""
        return True

    def emptyline(self):
        # Do nothing on empty input line
        pass
    
    def do_add(self, line):
        args = line.split()
        if len(args) == 2:
            self.filter_manager.add_filter(args[0], args[1])
            print(f"Added filter: {args[0]}")
        else:
            print("Usage: add [filter_name] [filter_definition]")

    def do_rm(self, line):
        self.filter_manager.remove_filter(line)
        print(f"Removed filter: {line}")

    def do_list(self, line):
        filters = self.filter_manager.list_filters()
        for name, definition in filters.items():
            print(f"{name}/{definition}")

    def do_exit(self, line):
        return True

    def emptyline(self):
        # Exit the editor when an empty line is entered
        return True
    

