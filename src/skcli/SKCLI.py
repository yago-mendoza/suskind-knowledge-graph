import cmd # Importing Python's built-in library for creating command-line interfaces (used for PrimaryInterface and upcoming sub-CLIs)
import datetime # Importing the datetime module to work with dates and times (used at 'get_string()' for PlaceHolder)
import argparse

import difflib

from src.skcli.err_mssg import *
from src.skcli.visuals import *
from src.skcli.command_docstrings import *

"""
# Write a command DOCSTRING for each new command
# Document all the code with in-line comments
# Make sure there's no hard coding at all

r --summary (que active el summary cada vez que se ejecute)
r --ls (que active el ls cada vez que se ejecute)

must be able to set unknown langs (not types) for new entries
prompt_toolkit for autocomplete

cd ..

ls)

14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -s --sort       #   set sort <on>/<off>
14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -c 3 --ncol 3   #   set ncol <int>
14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -t 9 --stop 9   #   set stop <int>/<off>
14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -a 5 --abbr 5   #   set abbr <int>/<off>
14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -f1   #   remember filters can be applied
| Showing 8/1240 results:
| 1. Arma biológica                       | 5. Hermandad
| 2. Tortuga marina                       | 6. Cabellera
| 3. Cárcel de muerte lenta e inevitable  | 7. Simplón
| 4. Tiburones                            | 8. Carretera asfaltada

"""

# The Placeholder class is designed to represent and manage the current state (or "Node") of the command prompt.
class Placeholder():
    def __init__(self, cmd):
        self.cmd = cmd  # Holds a reference to the command module, allowing updates to the cmd.prompt with the generated string from this class.
        # Initialize default properties for the node, representing its language, type, name, and lemma.
        self.lang, self.type, self.name, self.lemma = 'lang', 'type', 'name', 'lemma'
        self.fields = ['y1', 'e1']  # A list of additional fields that influence the outcome of commands like "ls".

    # Public Methods -----

    def update_node(self, node):
        # Updates the current node and its properties. This method is typically called when the node context changes.
        self.node = node  # Stores the entire node object for potential future use.
        # Extracts and updates the node's fundamental attributes to reflect the new context.
        self.lang, self.type, self.name, self.lemma = node.identify()
        # Refreshes the command prompt to include the updated node information.
        self._update_string()
    
    def update_field(self, mode, field):
        # Dynamically calls the add or remove field method based on the mode ('add' or 'remove').
        getattr(self, f"_{mode}_field")(field)  # Performs a single field operation update.
        # Refreshes the command prompt to include the updated fields.
        self._update_string()

    # Private Methods -----

    # Atomically adds a field to the list of fields if it's not already present.
    def _add_field(self, field):
        if field not in self.fields: self.fields.append(field)

    # Atomically removes a field from the list of fields if it's present.
    def _remove_field(self, field):
        if field in self.fields: self.fields.remove(field)

    # Updates the prompt of the cmd object to the newly generated string representing the current state.
    def _update_string(self):
        self.cmd.prompt = self._get_string()

    # Constructs and returns the string that represents the current state and will be used as the cmd prompt.
    def _get_string(self):
        # Formats the current time as a string.
        str_time = datetime.datetime.now().strftime('%H:%M:%S')
        # Sorts and reverses the fields for consistent ordering.
        self.fields = sorted(self.fields)
        self.fields.reverse()
        # Concatenates the fields into a single string.
        fields_list = '[' + '/'.join(self.fields) + ']'
        # Constructs and returns the final prompt string, incorporating time, node properties, and additional fields.
        return f"{str_time} ~ [{self.lang}][{self.type}]@[{self.name}({self.lemma or ''})]/{fields_list or ''}: "



class PrimaryInterface (cmd.Cmd):
    
    def __init__(self, graph):
        super().__init__()  # Initialize the base class (cmd.Cmd).
        self.G = graph  # Store the graph object.
        self.placeholder = Placeholder(self)  # Create a Placeholder instance.
        self._set_random_node()  # Initialize a node at random.    

    # Public Methods -----
        
    def do_help(self, arg):
        """Provide help for a specified command or list all commands if none is specified."""
        if arg:
            # User asked for help on a specific command
            help_text = COMMAND_DOCSTRINGS.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for {arg}")
        else:
            # User typed "help" without specifying a command
            padded_print("Available commands:")
            mini_prompt = ''
            right_padding = max([len(command) for command in COMMAND_DOCSTRINGS]) + len(mini_prompt)
            for command in COMMAND_DOCSTRINGS:
                # Only print the first line of each help text for an overview
                first_line = COMMAND_DOCSTRINGS[command].strip().split('\n')[0]
                padded_print(f"{command+mini_prompt:<{right_padding}} : {first_line[8:]}")
        
    def do_set(self, arg):
        # Set is a multi-purpose function.
        args = arg.split()
        if not args:
            # If no specific arguments are provided, default to setting all 'y' and 'e' prefixed fields (y0, y1, y2, e0, e1, e2).
            for field in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                self.placeholder.update_field('add', field)
        for setting in args:
            # Check if the argument is a shorthand ('y' or 'e') representing a set of fields.
            if setting in ['y', 'e']:
                # If shorthand is used, add all related fields (e.g., y0, y1, y2 for 'y') to the placeholder.
                for field in [f'{setting}{i}' for i in range(3)]:
                    self.placeholder.update_field('add', field)
            # Check if the argument is a specific field (e.g., 'y0', 'e2'), allowing for granular control.
            elif setting in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                field = setting
                self.placeholder.update_field('add', field)
            # Check if the argument matches any known language in the graph.
            elif setting in self.G.list_langs():
                # If a language is specified, update the language in the placeholder and set a random node of that language.
                lang = setting
                self.placeholder.lang = lang
                self._set_random_node(lang=setting, type_='')
            # Check if the argument matches any known type in the graph.
            elif setting in self.G.list_types():
                # If a type is specified, update the type in the placeholder and set a random node of that type.
                type_ = setting
                self.placeholder.type = type_
                self._set_random_node(lang='', type_=setting)
            else:
                # If the argument doesn't match any known settings, inform the user that the setting is invalid.
                print("Invalid setting.")
    
    def do_unset(self, arg):
        # Splits the input string into individual arguments for processing.
        args = arg.split()
        # If no arguments are provided, default to removing all 'y' and 'e' prefixed fields (y0, y1, y2, e0, e1, e2).
        if not args:
            for field in [f'{setting}{i}' for i in range(3) for setting in ['e', 'y']]:
                # Calls the update_field method with the 'remove' mode for each field, effectively clearing all.
                self.placeholder.update_field('remove', field)
        
        # Iterates over each provided argument to determine the appropriate action.
        for setting in args:
            # Checks if the argument is a shorthand ('y' or 'e') for a set of fields.
            if setting in ['y', 'e']:
                # If shorthand is used, remove all related fields (e.g., y0, y1, y2 for 'y') from the placeholder.
                for field in [f'{setting}{i}' for i in range(3)]:
                    self.placeholder.update_field('remove', field)
            # Checks if the argument is a specific field (e.g., 'y0', 'e2'), allowing for granular control.
            elif setting in [f'{setting}{i}' for i in range(3) for setting in ['e', 'y']]:
                field = setting
                # Calls the update_field with 'remove' mode for the specific field.
                self.placeholder.update_field('remove', field)
            else:
                # If the argument doesn't match any known settings, inform the user that the setting is invalid.
                print("Invalid setting.")

    def do_cd(self, arg):
        # Initializes an argument parser specifically for the 'cd' (change directory) command.
        parser = argparse.ArgumentParser()
        # Defines 'name' as a positional argument that can accept multiple values, representing the target node's name.
        parser.add_argument('name', nargs='*', help='The name to search for')

        try:
            # Parses the arguments from the input string. The 'split' method breaks it into a list of arguments.
            parsed_args = parser.parse_args(arg.split())
            # Combines the list of 'name' arguments back into a single string, representing the full name of the target node.
            parsed_name = ' '.join(parsed_args.name)

        except SystemExit:
            # Handles the situation where argparse encounters a parsing error and attempts to exit the script.
            # Intercepting SystemExit here prevents the entire CLI from shutting down due to a malformed command.
            padded_print("Invalid command or arguments. Type 'help cd' for more information.")
            return

        # Initiates the search for nodes with the most specific criteria first, based on the current language and type context.
        nodes = self.G.find(self.placeholder.lang, self.placeholder.type, parsed_name)

        # Implements fallback logic: If the initial search yields no results, progressively broadens the search criteria.
        if not nodes:
            nodes = self.G.find(self.placeholder.lang, '', parsed_name)
        if not nodes:
            nodes = self.G.find('', self.placeholder.type, parsed_name)
        if not nodes:
            nodes = self.G.find('', '', parsed_name)

        # Processes the search results based on the number of nodes found.
        if len(nodes) == 1:
            # If exactly one matching node is found, it's automatically set as the current context.
            self._set_node(nodes[0])
        elif nodes:
            # If multiple matching nodes are found, indicates a future feature for user selection.
            SelectNodeInterface(nodes, self).cmdloop()
        else:
            # If no matching nodes are found, informs the user accordingly.
            number_of_guesses = 3
            scores = []
            for node in self.G:
                ratio = difflib.SequenceMatcher(None, parsed_name, node.name).ratio()
                scores.append((ratio, node))
            top_guessed_nodes = [node for ratio, node in sorted(scores, key=lambda x: x[0], reverse=True)[:number_of_guesses]]
            SelectNodeInterface(top_guessed_nodes, self).cmdloop()
            
            

    def do_r(self, args):
        # Creates a new argument parser to interpret the command line inputs.
        parser = argparse.ArgumentParser(description="Perform a random node search")
        # Adds optional arguments to specify the language and type, enhancing the command's flexibility.
        parser.add_argument('-l', '--lang', type=str, help='Specify the language')
        parser.add_argument('-t', '--type', type=str, help='Specify the type')
        # Parses the arguments from the command line input.
        args = parser.parse_args(args.split())

        # Retrieves the language and type constraints from the parsed arguments, if provided.
        type_constraint = args.type if args.type else None
        lang_constraint = args.lang if args.lang else None

        # Calls the _set_random_node method with the provided language and type constraints.
        # This allows users to narrow down the search to a specific subset of nodes.
        self._set_random_node(lang=lang_constraint, type_=type_constraint)

    def do_ls(self, arg):

        # Initialize the argument parser
        parser = argparse.ArgumentParser(description='List information about the current node.')
        parser.add_argument('-d', '--details', action='store_true', help='Show detailed information about each item.')

        args = parser.parse_args(arg.split())

        if self.placeholder.fields:

            self._update_graph_permissions() # we set graph permissions to fields (for neighbors)
            nodes_to_display = self.placeholder.node.get_neighbors().set()  # Assuming a method to get data from the current node

            if nodes_to_display:
                strings_to_display = [f'| {i}. {node.name}' for i, node in enumerate(nodes_to_display)]
                columnize(strings_to_display, ncol=3, col_width=18)
            else:
                if not self.placeholder.node.get_neighbors('111111'):
                    print('The target node is completely empty.')
                else:
                    print('The set field for the target node is empty.')
        else:
            padded_print("Error. Search field is needed")

    def do_summary(self, arg):
        node = self.placeholder.node
        neighbors_dict = node.get_neighbors()
        padded_print(f'Showing quick summary for targeted node.')
        elements = [f"| {key} : {len(neighbors_dict.get(key))}" for key in neighbors_dict.keys()]
        columnize(elements, ncol=2)

    def do_new(self, arg):
        # uses argparse
        # selects fields as attributes
        # asks for lemma
        pass

    def do_save(self, arg):
        # saves everything to a custom TXT data file
        pass

    # Internal Methods  --------------------
            
    def _set_node(self, new_node):
        if new_node:
            self.placeholder.update_node(new_node)

    def _set_random_node(self, lang='', type_=''):
        new_node = self.G.random(lang=lang, type_=type_)
        if new_node:
            self._set_node(new_node)
        else:
            padded_print('No nodes met the criteria.')

    def _update_graph_permissions(self):
        long_parser = {'y0':'synset0', 'e0':'semset0',
                       'y1':'synset1', 'e1':'semset1',
                       'y2':'synset2','e2':'semset2'}
        self.G.disable()
        for field in self.placeholder.fields:
            self.G.enable(long_parser[field])

    def _print_markdown_title(self):
        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        console.print(Markdown("# Suskind Knowledge Graph"))

    # CMD private re-writen methods --------------------
            
    def preloop(self):
        self._print_markdown_title()
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER)
        print('-'*47)

    def default(self, line):
        padded_print(f"Unknown '{line[:2].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)
        

class SelectNodeInterface(cmd.Cmd):
    prompt = '>> '

    def __init__(self, nodes, parent_cli):
        super().__init__()
        self.nodes = nodes
        self.parent_cli = parent_cli
        self.display()

    def display(self):
        padded_print("Do you mean ...")
        for index, node in enumerate(self.nodes, start=1):
            lang, type, name, lemma = node.identify()
            string_index = str(index).zfill(2 if len(self.nodes)>10 else 1)
            print(f"| {string_index}) [{lang}][{type}][{name}]@[({lemma or ''})]")
        padded_print("(Press Enter without any input to exit)")

    def default(self, line):
        if line == '':
            return True  # Exit if the input is empty.
        try:
            index = int(line) - 1  # Convert to zero-based index.
            if 0 <= index < len(self.nodes):
                selected_node = self.nodes[index]
                self.parent_cli._set_node(selected_node)  # Updated line
                return True  # Return to the main CLI.
            else:
                print("Please enter a valid number from the list.")
        except ValueError:
            print("Please enter a number to select a node or just press Enter to exit.")

    def do_exit(self, arg):
        """Exit back to the main interface."""
        return True  # Returning True exits the cmd loop.



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
    


