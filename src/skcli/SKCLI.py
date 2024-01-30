import os
import cmd
import random
import argparse

import src.sktools as sk

from src.skcli.skplaceholder import *
from src.skcli.aux_clis import *

from src.skcomponents.search_algorithms import *

from src.skcli.aux_funcs.err_mssg import *
from src.skcli.aux_funcs.visuals import *
from src.skcli.aux_funcs.command_docstrings import *

# be able to use grab on LS command

# how to clear whole fields even nodes

# for the 'r' random method -------------------------------------------------
    
# a parameter -s like size that lets know how many nodes arep ossible of geting (in function of filter)

# 1. Add additional flags at 'r' 
# r --summary (que active el summary cada vez que se ejecute)
# r -f (not working as expected)

# do_new (creates a new node being able to set new language (-l) or lemma (-l), because if already existing, cannot create unless a lemma is set)
# do_save (save the graph to a file)

# 4. Editing node properties ------------------------------------

# name -e
# >> Banco # y aquí editamos
#     >> Banco
#     | Warning. There's already 2 entries called 'Banco'. Select one to merge.
#     |  1. [es][n][Banco]@[('institución')]
#     |  2. [es][n][Banco]@[('mobiliario')]
#     |  3. <new_lemma>

# lemma -e
# | Other lemmas for this entry are ...
# |  1. Institución
# |  2. Mobiliario
# |  <new_lemma>
# >> Grupo
# -e or lang -e or type -e

# 5. Deleting a node ---------------------------------------------

# 14:32:18 ~ [en][j][Banco]@[('Grupo')]/[y0/y1/y2]: rm
# | Warning. Are you sure you want to remove this node (1159 edges)? [Y/N]
# >> Y



# 7. TERMINAL ---------------------------------------

# 14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]: term
# Python. Granted a pathway to SKComponents objects and methods.
# Type "Node" or "Graph" to inspect objects and "exit" to leave.
# >>> Node.compress.expand('synset').compress('synset2')
# >>> G.view_names()
# >>> n = G.random()
# >>> G.disable('semset')    # implementar que podamos ahorrarnos comillas
# >>> ndst = G.filter_
# Exiting terminal...
# 14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]:

# 8. NESTED_HISTORY ------------------------------------

# | Showing nested history:
# | root: [0] Andar(/7)
# |       └── [1] Cercenar (<6th> of 7)
# |            ├── [2] Elegía (<7th> of 7)
# |            └── [3] Esperanza (<42th> of 102)
# cd ..
# | Warning: this action will delete the nested search history. Are you sure? [Y/N]

#################################################################################

# # 98. Undo and Go back to previous node
# via 'undo' and 'cd ..'

# # 99. Autocomplete via 'tab' key
# prompt_toolkit for autocomplete

# ¿Useful symbols?
#     <, >
#     clear, copy, paste
#     extract / export, min
#     commit, push, autosave 
# ¿Very future steps?
#     min_path
#     reduce a set
#     search method
#     decide where to use 'rich' colors
#     I dont need a hist of every single action done. So hist will be just for visited nodes.
#     status (already set, to do)
#     suggestions
#     and changing words from category within a same node
#     traduccion con filter, no con funcion explicita
#     (same for merging synset1's, just a way to merge nodes and them also)


class SK_Interface (cmd.Cmd):
    
    def __init__(self, graph):
        super().__init__()
        self.G = graph 
        self.placeholder = Placeholder(self)
        self.response = None
        self.grabbed_nodes = []

        self._set_random_node()

    # Public Methods -----
    
    def do_save(self, arg): 
        filename = arg.strip() or 'data.txt'  # Use 'data' as default filename if none is provided
        try:
            self.G.save(filename)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def do_help(self, arg):
        """Provide help for a specified command or list all commands if none is specified."""
        if arg:
            # User asked for help on a specific command
            help_text = COMMAND_DOCSTRINGS_SK.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'.")
        else:
            # User typed "help" without specifying a command
            def get_description_from_docstring(docstring): return docstring.strip().split('\n')[0][8:]
            commands = COMMAND_DOCSTRINGS_SK.keys()
            contents = [get_description_from_docstring(COMMAND_DOCSTRINGS_SK[command]) for command in commands]
            formatted_lines = get_label_aligned_lines(commands, ':', contents)
            padded_print("Available commands:", formatted_lines, tab=0)
        
    def do_set(self, arg):
        # Set is a multi-purpose function.
        args = arg.split()
        if not args:
            # If no specific arguments are provided, default to setting all 'y' and 'e' prefixed fields (y0, y1, y2, e0, e1, e2).
            for field in [f'{setting}{i}' for i in range(3) for setting in ['e','y']]:
                self.placeholder.update_field('add', field)
        for setting in args:
            if {'e0', 'e1', 'e2', 'y0', 'y1', 'y2'}.issubset(self.placeholder.fields):
                self.placeholder.fields = []
                # DE ENTRADA, Si esta lleno y estamos intentando hacer un 'set', será que queremos borrar y dejar solo ese. Lo entendemos.
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
            else:
                if len(setting) == 1: 
                    if setting in self.G.get_set('type'):
                        # If a type is specified, update the type in the placeholder and set a random node of that type.
                        type = setting
                        self.placeholder.type = type
                        self._set_random_node(type=type)
                    else:
                        print("Invalid 'type'.")
                elif len(setting) == 2:
                    if setting in self.G.get_set('lang'):
                        # new language being inputed
                        # If a language is specified, update the language in the placeholder and set a random node of that language.
                        lang = setting
                        self.placeholder.lang = lang
                        self._set_random_node(lang=lang)
                    else:
                        print("Invalid 'lang'.")
                else:
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
            padded_print("Invalid command or arguments. Type 'help cd' for more information.", tab=0)
            return

        nodes = self.G.select(name=parsed_name)

        # Processes the search results based on the number of nodes found.
        if len(nodes) == 1:
            # If exactly one matching node is found, it's automatically set as the current context.
            self._set_node(nodes[0])

        else:
            
            # If multiple matching nodes are found, indicates a future feature for user selection.
            if nodes:
                options = [node._convert_header_to_compact_format() for node in nodes]
            else:
                number_of_guesses = 4
                nodes = sk.find_similars(graph=self.G, target_name=parsed_name, k=number_of_guesses)
                options = [node._convert_header_to_compact_format() for node in nodes]

            header_statement = "Do you mean ..."
            tail_statement = "(Press Enter without any input to exit)"
            SelectInterface(options, self, header_statement, tail_statement).cmdloop()
            response = self._get_response()
            if response:
                self._set_node(nodes[int(response)-1])

    def do_grab(self, arg):

        if arg:
            # grab ____
            parser = argparse.ArgumentParser()
            parser.add_argument('name', nargs='*', help='The name to search for')
            parsed_args = parser.parse_args(arg.split())
            parsed_name = ' '.join(parsed_args.name)

            nodes = self.G.select(name=parsed_name)

            if len(nodes) == 1:
                self.grabbed_nodes.append(nodes[0])

            else:
                if nodes:
                    options = [node._convert_header_to_compact_format() for node in nodes]
                else:
                    number_of_guesses = 4
                    nodes = sk.find_similars(graph=self.G, target_name=parsed_name, k=number_of_guesses)
                    options = [node._convert_header_to_compact_format() for node in nodes]

                header_statement = "Do you mean ..."
                tail_statement = "(Press Enter without any input to exit)"
                SelectInterface(options, self, header_statement, tail_statement).cmdloop()
                response = self._get_response()
                if response:
                    target_node = nodes[int(response)-1]
                    if target_node not in self.grabbed_nodes:
                        self.grabbed_nodes.append(target_node)

        else:
            # grab (will grab the current)
            if self.placeholder.node not in self.grabbed_nodes:
                self.grabbed_nodes.append(self.placeholder.node)
    
    def do_grabbed(self, arg):
        GB_Interface(self)
    
    def do_run(self, arg):

        print(f"(SYS: Started search-session at {datetime.datetime.now().strftime('%H:%M:%S')})")

        parser = argparse.ArgumentParser(description='Run density search with specified parameters.')
        parser.add_argument('k', nargs='?', type=int, help='MSL (Minimum Shared Linkage) as an integer.', default=None)
        parser.add_argument('-f', '--fielding', action='store_true', help='Restricts the search to results within the placeholder fielding.')
        parser.add_argument('-d', '--details', action='store_true', help='Provides a more detailed display.')
        parser.add_argument('-w', '--width', type=int, default=20, help='Width for the column.')
        parser.add_argument('-a', '--abbr', type=int, default=None, help='Abbreviate all results to a maximum length.')
        parser.add_argument('-t', '--stop', type=int, default=None, help='Set a max of nodes to be displayed.')
        parser.add_argument('-c', '--ncol', type=int, default=3, help='Number of columns.')
        parser.add_argument('-r', '--shuffle', action='store_true', help='Shuffles the results.')
        ls_args, unknown = parser.parse_known_args(arg.split())
        if unknown:
            print(f'Unrecognized argument(s): {" ".join(unknown)}')
            return
        
        # Handle the k value for density search
        k = (str(ls_args.k) if ls_args.k else None) or input(">> MSL (Minimum Shared Linkage) [int] : ")
        while not k.isdigit() or int(k) > len(self.grabbed_nodes):
            if not k.isdigit():
                print("Please, enter a valid integer.")
            elif int(k) > len(self.grabbed_nodes):
                print(f"Please, enter an integer <{len(self.grabbed_nodes)} (selectable nodes).")
            k = input(">> Minimum Shared Linkage (MSL) : ")
        k = int(k)

        fielding = self.placeholder.fields if ls_args.fielding else []

        # Perform the density search (excludes original ones)
        output_nodes = [node for node in density_search(self.grabbed_nodes, k, *fielding) if node not in self.grabbed_nodes]

        # Apply the arguments to the nodes
                
        if ls_args.shuffle:
            random.shuffle(output_nodes)
        if ls_args.stop and ls_args.stop <= len(output_nodes):
            output_nodes = output_nodes[:ls_args.stop]
        if ls_args.details:
            max_index_length = len(str(len(output_nodes) - 1))
            for i, node in enumerate(output_nodes):
                sizes = [str(i) for i in node.get_sizes()]
                str_sizes = '/'.join(sizes[:3]) + ' - ' + '/'.join(sizes[3:])
                print(f"{str(i+1).zfill(max_index_length)}) [{node.lang}][{node.type}][{node.name}][{node.lemma}]....({str_sizes})")
        else:
            names = [node.name for node in output_nodes]
            if ls_args.abbr:
                names = [name[:ls_args.abbr] + '...' if len(name) > ls_args.abbr else name for name in names]

            print(f"Showing {len(names)}/{len(output_nodes)} results.")
            strings_to_display = [f'| {i+1}. {name}' for i, name in enumerate(names)]
            formatted_lines = get_n_columns_from_elements(strings_to_display, ncol=ls_args.ncol, col_width=ls_args.width)
            for line in formatted_lines:
                print(line)
        
        print(f"(SYS: Ended search-session at {datetime.datetime.now().strftime('%H:%M:%S')})")

    def do_r(self, args):

        parser = argparse.ArgumentParser(description="Perform a random node search")
        parser.add_argument('-l', '--lang', type=str, help='Specify the language')
        parser.add_argument('-t', '--type', type=str, help='Specify the type')
        parser.add_argument('-f', '--fav', action='store_true', help='Toggle favorite switch')  # Notice the action change.
        args = parser.parse_args(args.split())

        # Retrieves the language and type constraints from the parsed arguments, if provided.
        type_constraint = args.type if args.type else None
        lang_constraint = args.lang if args.lang else None

        # Calls the _set_random_node method with the provided language and type constraints.
        # This allows users to narrow down the search to a specific subset of nodes.
        self._set_random_node(lang=lang_constraint,
                              type=type_constraint,
                              favorite=args.fav)

    def do_ls(self, arg):

        # 14:32:18 ~ [en][j][Normal]@[('')]/[y]: ls -f1   #   remember filters can be applied

        parser = argparse.ArgumentParser(description='List information about the current node.')
        parser.add_argument('-d', '--details', action='store_true', default=None, help='Provides a more detailed display.')
        parser.add_argument('-w', '--width', type=int, default=20, help='Width for the column.')
        parser.add_argument('-a', '--abbr', type=int, default=None, help='Abbreviate all results to a maximum length.')
        parser.add_argument('-t', '--stop', type=int, default=None, help='Set a max of nodes to be displayed.')
        parser.add_argument('-c', '--ncol', type=int, default=3, help='Number of columns.')
        parser.add_argument('-r', '--shuffle', action='store_true', help='Shuffles the results.')

        ls_args, unknown = parser.parse_known_args(arg.split())
        
        if unknown:
            padded_print(f'Unrecognized argument(s): {" ".join(unknown)}', tab=0)

        if self.placeholder.fields:

            nodes = list(self.placeholder.node.get_neighbors(self.placeholder.fields))
            nodes = sorted(nodes, key=lambda node: node.name)

            if nodes:

                if ls_args.shuffle:
                    random.shuffle(nodes)

                if ls_args.stop:
                    if ls_args.stop <= len(nodes):
                        nodes = nodes[:ls_args.stop]

                if ls_args.details:

                    # sin ponemos details, aplican todos los criterios menos 'abbr'
                    # solo tienen sentido 'stop' y 'r' de 'random/suffle'
                    to_print = []
                    max_index_length = len(str(len(nodes) - 1))  # Length of the largest index

                    for i, node in enumerate(nodes):
                        sizes = [str(i) for i in node.get_sizes()]
                        str_sizes = '/'.join(sizes[:3]) + ' - ' + '/'.join(sizes[3:])
                        to_print.append(f'[{node.lang}][{node.type}][{node.name}][{node.lemma}]....({str_sizes})')
                    for i, _ in enumerate(to_print):
                        print(f"{str(i+1).zfill(max_index_length)}) {_}")
                
                else:

                    names = [node.name for node in nodes]
                        
                    if ls_args.abbr:
                        names = [name[:ls_args.abbr] + '...' if len(name) > ls_args.abbr else name for name in names]

                    if len(self.placeholder.fields) == 1:
                        print(f"(SYS: Started edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
                    
                    print(f"Showing {len(names)}/{len(self.placeholder.node.get_neighbors(self.placeholder.fields))} results.")
                    strings_to_display = [f'| {i+1}. {name}' for i, name in enumerate(names)]
                    
                    formatted_lines = get_n_columns_from_elements(strings_to_display, ncol=ls_args.ncol, col_width=ls_args.width)
                    for line in formatted_lines:
                        print(line)
            else:
                padded_print('The set field for the target node is empty.', tab=0)

            if len(self.placeholder.fields) == 1:
                LS_Interface(nodes, self, ls_args)

        if not self.placeholder.fields:
            padded_print("Error. Search field is needed", tab=0)

    def do_new(self, arg):
        NW_Interface(self)

    # Internal Methods  --------------------
            
    def _set_node(self, new_node):
        if new_node:
            self.placeholder.update_node(new_node)

    def _set_random_node(self, **kwargs):
        new_node = self.G.random(**kwargs)
        if new_node:
            self._set_node(new_node)
        else:
            padded_print('No nodes met the criteria.', tab=0)
    
    def _get_response(self, reset_response=True):
        # Gets and decides wether it resets the response or not (by default, it does)
        res, self.response = self.response, None if reset_response else self.response
        return res

    def _print_markdown_title(self):
        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        console.print(Markdown("# Suskind Knowledge Graph"))

    # CMD private re-writen methods --------------------
        
    def do_clear(self, arg):
        self.preloop()
        
    def preloop(self):
        os.system('cls')
        self._print_markdown_title()
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER, tab=0)
        print('-'*47)

    def default(self, line):
        padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER, tab=0)

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

    # def do_filter(self, arg):

    #     parser = argparse.ArgumentParser(prog='filter', add_help=False)
    #     parser.add_argument('-e', '--edit', action='store_true', help='Enter filter editing mode')
    #     args = parser.parse_args(arg.split())
    
    #     if args.edit:
    #         self._enter_filter_editor()
    #     else:
    #         if self.filters:
    #             for idx, filter in enumerate(self.filters, 1):
    #                 padded_print(f"f{idx}/{filter}")
    #         else:
    #             print("No filters set.")

    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: filter -e
    # # | Entered editor mode on filters:
    # # | f1/type('w').lang('es')
    # # | f2/starts('clar')
    # # >> rm f1
    # # >> add contains('esonate').lang('en')
    # # >> ''
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/:

    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
    # # | Showing filters:
    # # | f1/lang('es').contains('trent')
    # # | f2/starts('clar')
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/:

    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: set f1
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: unset ls f1
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: set ls f2
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
    # # | Showing filters:
    # # | [ls, cd, r] f1/lang('es')
    # # | [ls] f2/lang('en')
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: filter ls
    # # | Showing filters:
    # # | f1/lang('es')
    # # | [>] f2/lang('en')
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: unset f1
    # # 14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
    # # | Showing filters:
    # # | f1/lang('es')
    # # | [ls] f2/lang('en')