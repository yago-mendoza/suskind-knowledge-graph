import cmd # Importing Python's built-in library for creating command-line interfaces (used for PrimaryInterface and upcoming sub-CLIs)
import datetime # Importing the datetime module to work with dates and times (used at 'get_string()' for PlaceHolder)
import argparse

from src.skcli.err_mssg import *
from src.skcli.visuals import *

# It's designed to represent and manage the current <Node> of the command prompt.
class Placeholder():
    def __init__(self, cmd):
        self.cmd = cmd  # reference used to update the cmd.prompt to the placeholder string that this class generates
        self.lang, self.type, self.name, self.lemma = 'lang', 'type', 'name', 'lemma'  # node properties
        self.fields = []  # fields that will dictate the results of "ls"

    # Public Methods

    def update_node(self, node):
        self.node = node  # indeed, it also keeps the node
        self.lang, self.type, self.name, self.lemma = node.identify()  # extracts the attributes
        self._update_string()  # updates the string (every update methods will do so)
    
    def update_field(self, mode, field):
        # modes are 'add' or 'remove' (_add_field(field) and _remove_field(field))
        getattr(self, f"_{mode}_field")(field)  # updates the fields with a single field operation
        self._update_string()  # updates the string (every update methods will do so)

    # Private Methods

    # Atomic editing of the fields
    def _add_field(self, field):
        if field not in self.fields: self.fields.append(field)
    def _remove_field(self, field):
        if field in self.fields: self.fields.remove(field)
    # Sets the prompt at the upstream object cmd to the generated string
    def _update_string(self):
        self.cmd.prompt = self._get_string()
    # Generate the string that will be used as the cmd prompt
    def _get_string(self):
        str_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.fields = sorted(self.fields)
        self.fields.reverse()
        fields_list = '[' + '/'.join(self.fields) + ']'
        return f"{str_time} ~ [{self.lang}][{self.type}]@[{self.name}({self.lemma or ''})]/{fields_list or ''}: " 
    

class PrimaryInterface (cmd.Cmd):

    def preloop(self):

        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        console.print(Markdown("# Suskind Knowledge Graph"))
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER)
        print('-'*47)

    def default(self, line):
        padded_print(f"Unknown '{line[:5]}...' command.", CONTEXTUAL_DISCLAIMER)
    
    def __init__(self, graph):
        super().__init__()  # Initialize the base class (cmd.Cmd).
        self.G = graph  # Store the graph object.
        self.placeholder = Placeholder(self)  # Create a Placeholder instance.
        self._set_random_node()  # Initialize a node at random.    



    

    # Public Methods
        
    def do_set(self, arg):
        args = arg.split()
        if not args:
            for field in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                self.placeholder.update_field('add', field)

        for setting in args:
            if setting in ['y', 'e']:
                for field in [f'{setting}{i}' for i in range(3)]:
                    self.placeholder.update_field('add', field)
            elif setting in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                field = setting
                self.placeholder.update_field('add', field)
            elif setting in self.G.list_langs():
                lang = setting
                self.placeholder.lang = lang
                self._set_random_node(lang=setting, type_='')
            elif setting in self.G.list_types():
                type_ = setting
                self.placeholder.type = type_
                self._set_random_node(lang='', type_=setting)
            else:
                print("Invalid setting.")
    
    def do_unset(self, arg):
        args = arg.split()
        if not args:
            for field in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                self.placeholder.update_field('remove', field)

        for setting in args:
            if setting in ['y', 'e']:
                for field in [f'{setting}{i}' for i in range(3)]:
                    self.placeholder.update_field('remove', field)
            elif setting in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                field = setting
                self.placeholder.update_field('remove', field)
            else:
                print("Invalid setting.")

    def do_r(self, args):

        parser = argparse.ArgumentParser(description="Perform a random node search")
        parser.add_argument('-l', '--lang', type=str, help='Specify the language')
        parser.add_argument('-t', '--type', type=str, help='Specify the type')
        args = parser.parse_args(args.split())

        type_constraint = args.type if args.type else None
        lang_constraint = args.lang if args.lang else None

        self._set_random_node(lang=lang_constraint, type_=type_constraint)

    def do_cd(self, arg):
        # Create an argument parser for the 'cd' command
        parser = argparse.ArgumentParser()
        parser.add_argument('name', nargs='*', help='The name to search for')  # Name is a positional argument

        try:
            # Parse the arguments
            parsed_args = parser.parse_args(arg.split())
            parsed_name = ' '.join(parsed_args.name)  # Join the list back into a string

        except SystemExit:
            # argparse automatically exits on error, which would end your CLI
            # Intercepting SystemExit prevents the entire script from exiting if the command is malformed.
            padded_print("Invalid command or arguments. Type 'help cd' for more information.")
            return

        # Start with the most specific search based on user input.
        nodes = self.G.find(self.placeholder.lang, self.placeholder.type, parsed_name)

        # Apply fallback logic only to the categories that weren't specified by the user.
        if not nodes:
            nodes = self.G.find(self.placeholder.lang, '', parsed_name)
        if not nodes:
            nodes = self.G.find('', self.placeholder.type, parsed_name)
        if not nodes:
            nodes = self.G.find('', '', parsed_name)

        # Handle the result based on the number of nodes found.
        if len(nodes) == 1:
            self._set_node(nodes[0])  # Automatically update if only one node found.
        elif nodes:
            print('Still need to develop prompt_user subCLI')
        else:
            padded_print("No nodes found.")

    # Internal Functions
            
    def _set_node(self, new_node):
        if new_node:
            self.placeholder.update_node(new_node)

    def _set_random_node(self, lang='', type_=''):
        new_node = self.G.random(lang=lang, type_=type_)
        if new_node:
            self._set_node(new_node)
        else:
            padded_print('No nodes met the criteria.')
        


# class SelectNodeInterface(cmd.Cmd):
#     prompt = '>> '

#     def __init__(self, nodes, parent_cli):
#         super().__init__()
#         self.nodes = nodes  # The list of nodes to choose from.
#         self.parent_cli = parent_cli  # Reference to the parent CLI for returning data or state.
#         self.display()

#     def display(self):
#         print("| Did you mean ...")
#         for index, node in enumerate(self.nodes, start=1):
#             lang, type, name, lemma = node.identify()
#             print(f"| {index}) [{lang}][{type}][{name}]@[({lemma or ''})]")
#         print("| (Press Enter without any input to exit)")

#     def default(self, line):
#         if line == '':
#             return True  # Exit if the input is empty.
#         try:
#             index = int(line) - 1  # Convert to zero-based index.
#             if 0 <= index < len(self.nodes):
#                 selected_node = self.nodes[index]
#                 self.parent_cli.set_node_directly(selected_node)
#                 return True  # Return to the main CLI.
#             else:
#                 print("Please enter a valid number from the list.")
#         except ValueError:
#             print("Please enter a number to select a node or just press Enter to exit.")

#     def do_exit(self, arg):
#         """Exit back to the main interface."""
#         return True  # Returning True exits the cmd loop.

#     def postloop(self):
#         print("Returning to main interface...")





# los argumentos -> library argparse, action, help 
        
# class CLIFilter(cmd.Cmd):
#     prompt = '>'
#     def __init__(self, filter_manager):
#         super().__init__()
#         self.filter_manager = filter_manager

#     def do_filter(self, line):
#         args = line.split()
#         if "-e" in args:
#             editor = CLIFilter(self.filter_manager)
#             editor.cmdloop("Entered editor mode on filters:")
#         else:
#             self.show_filters()
    


