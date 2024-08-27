import os
import re
import cmd
import random
import argparse

from collections import Counter

import src.script.sktools as sk

from src.script.skcli.skplaceholder import *
from src.script.skcli.aux_clis import *

from src.script.skcli.aux_funcs.err_mssg import *
from src.script.skcli.aux_funcs.visuals import *
from src.script.skcli.aux_funcs.command_docstrings import *

from src.script.skcomponents.sknode import Node

from pathlib import Path
import shutil
import datetime


class ScriptInterface (cmd.Cmd):
    
    def __init__(self, graph):
        super().__init__()
        self.G = graph 
        self.placeholder = Placeholder(self)
        self.response = None

        self.nodes_hist = []

        self._set_random_node()

        self.ls_default_lang = None
        self.ls_default_type = None

        self.r_default_lang = None
        self.r_default_type = None

        self.filter_tags = []

    # Public Methods -----
        
    def do_term(self, arg):

        import re

        print("Python SKTerminal. Access to SKComponents objects and methods.")
        print('Type "Node" or "G" to inspect objects and "exit" to leave.')

        # Include self.G as G in the local context
        local_context = {"self": self, "Node": Node, "G": self.G}

        # In your loop, modify the command based on this function's return value
        while True:
            command = input(">>> ")

            if command in ["exit", "quit", "q"]:
                print("Exiting SKTerminal...")
                break

            if command.strip() == "":
                continue

            # Wrap the command in a try-except to capture execution errors
            try:
                # Use compile to prepare a code object from the command
                code_obj = compile(command, '<string>', 'eval')
            except SyntaxError:
                # Fallback to exec for statements that do not return a value
                try:
                    exec(command, globals(), local_context)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                # Execute compiled command that is expected to return a value
                try:
                    result = eval(code_obj, globals(), local_context)
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"Error: {e}")     
        
    def do_save(self, arg):
        filename = arg.strip() or 'script.txt'  # Use 'script.txt' as default filename if none is provided
        file_path = Path(filename)
        backup_dir = Path('sec_copy') / 'script'
        
        try:
            # Ensure the backup directory exists
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Save the main file
            self.G.save(file_path)
            print(f"Data saved successfully to {file_path}")
            
            # Create a backup copy with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_filename
            
            shutil.copy2(file_path, backup_path)
            print(f"Backup saved to {backup_path}")
            
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

        args = arg.split()

        if not args:
            args = ['y', 'e']

        # Set is a multi-purpose function.
        y_fields, e_fields = {'y0', 'y1', 'y2'}, {'e0', 'e1', 'e2'}
        all_fields = y_fields | e_fields
        current_set = set(self.placeholder.fields)

        # Determine if the args are exclusively related to 'y', 'e', or their specific fields.
        args_related_to_ye = any(arg in {'y', 'e'} or arg in all_fields for arg in args)

        # Clear fields only if args are related to 'y', 'e', or their specific fields,
        # and not in the case of adding 'e' to all 'y' or 'y' to all 'e'.
        if args and args_related_to_ye:
            if not (set(args) == {'e'} and y_fields.issubset(current_set) or 
                    set(args) == {'y'} and e_fields.issubset(current_set)):
                self.placeholder.fields = []

        # Process each arg for adding fields.
        for setting in args:
            if setting == 'e':
                if len(self.placeholder.fields) == 6:
                    self.placeholder.fields = []
                    self.placeholder.fields.extend(['e2', 'e1', 'e0'])
                else:
                    self.placeholder.fields.extend(e_fields - current_set)
            elif setting == 'y':
                if len(self.placeholder.fields) == 6:
                    self.placeholder.fields = []
                    self.placeholder.fields.extend(['y2', 'y1', 'y0'])
                else:
                    self.placeholder.fields.extend(y_fields - current_set)
            elif setting in all_fields:
                self.placeholder.fields.append(setting)

        # Deduplicate placeholder.fields while preserving order.
        self.placeholder.fields = list(dict.fromkeys(self.placeholder.fields))        

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

    def do_pick(self, arg):
        """
        Suggest a list of elements to pick from and add the selected element to the current field of the placeholder.
        Usage: pick [-c CHOICES]
        """
        parser = argparse.ArgumentParser(description="Pick an element to add to the current field.")
        parser.add_argument("-c", "--choices", type=int, default=5, help="Number of choices to display (default: 5)")
        
        try:
            args = parser.parse_args(arg.split())
        except SystemExit:
            return
        
        if not self.placeholder.fields:
            print("Error: No field selected. Use 'set' to select a field first.")
            return
        
        current_field = self.placeholder.fields[0]
        is_syntactic = current_field.startswith('y')
        
        if is_syntactic:
            # For syntactic fields (y0, y1, y2), suggest random node names
            all_nodes = [node for node in self.G if node != self.placeholder.node and node not in self.placeholder.node.get_neighbors(current_field)]
            suggestions = random.sample(all_nodes, min(args.choices, len(all_nodes)))
            choices = [node.name for node in suggestions]
        else:
            # For semantic fields (e0, e1, e2), suggest random semantic attributes
            all_semantic_attrs = set()
            for node in self.G:
                all_semantic_attrs.update(node.get_neighbors('e'))
            current_attrs = set(self.placeholder.node.get_neighbors(current_field))
            available_attrs = list(all_semantic_attrs - current_attrs)
            choices = random.sample(available_attrs, min(args.choices, len(available_attrs)))
        
        print(f"Suggestions for {current_field}:")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        
        while True:
            user_input = input(">> ")
            if user_input == "":
                print("No selection made. Exiting pick mode.")
                return
            try:
                index = int(user_input) - 1
                if 0 <= index < len(choices):
                    selected = choices[index]
                    if is_syntactic:
                        selected_node = next(node for node in suggestions if node.name == selected)
                        self.G.bind(self.placeholder.node, selected_node, current_field)
                        print(f"Successfully added node '{selected}' to {current_field}")
                    else:
                        self.G.bind(self.placeholder.node, selected, current_field)
                        print(f"Successfully added '{selected}' to {current_field}")
                    return
                else:
                    print("Invalid index. Please try again or press Enter to exit.")
            except ValueError:
                print("Invalid input. Please enter a number or press Enter to exit.")

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
        
        if parsed_name == '..':
            if len(self.nodes_hist)>1:
                last_node = self.nodes_hist.pop(-1)
                if self.placeholder.node == last_node:
                    last_node = self.nodes_hist.pop(-1)
                self._set_node(last_node)
            else:
                print('Reached base state.')
        
        else:
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
                    number_of_guesses = 10
                    nodes = sk.find_similars(graph=self.G, target_name=parsed_name, k=number_of_guesses)
                    options = [node._convert_header_to_compact_format() for node in nodes]

                header_statement = "Do you mean ..."
                tail_statement = "(Press Enter without any input to exit)"

                SelectInterface(options, self, header_statement, tail_statement).cmdloop()
                response = self._get_response()
                if response:
                    if response.isdigit():
                        self._set_node(nodes[int(response)-1])
                    else:
                        padded_print('Could not identify index.')

    def do_pin(self, arg):
        self.placeholder.node.edit(favorite=True)
        self._set_node(self.placeholder.node)

    def do_unpin(self, arg):
        self.placeholder.node.edit(favorite=False)
        self._set_node(self.placeholder.node)

    def do_del(self, arg):

        current_node = self.placeholder.node
        ch = input(f'SYS: Are you sure you want to remove this node ({len(current_node.get_neighbors())} edges)? [Y/N]\n>> ')
        if ch in {'Y','y'}:
            self.G.delete_node(current_node)
            self._set_random_node()
            print('Node succesfully removed.')
        else:
            print('Deletion process aborted.')
    
    def do_details(self, arg):

        node = self.placeholder.node
        sizes = node.get_sizes()
        synset_sizes = ', '.join([f'y{i} = {size}' for i, size in enumerate(node.get_sizes()[:3])])
        semset_sizes = ', '.join([f'e{i} = {size}' for i, size in enumerate(node.get_sizes()[3:])])
        padded_print(f'Synset sizes ({synset_sizes})')
        padded_print(f'Semset sizes ({semset_sizes})')
    
    def do_r(self, args):

        self.do_clear('')

        parser = argparse.ArgumentParser(description="Perform a random node search")
        parser.add_argument('-l', '--lang', type=str, nargs='?', const='', default=None, help='Specify the language or reset')
        parser.add_argument('-t', '--type', type=str, nargs='?', const='', default=None, help='Specify the type or reset')
        parser.add_argument('-s', '--sos', type=str, default=None, help='Sets a bias for low-connected nodes.')
        parser.add_argument('-f', '--fav', action='store_true', help='Toggle favorite switch')
        try:
            args = parser.parse_args(args.split())
        except SystemExit:
            return 

        # Actualiza o elimina las restricciones globales basándose en los argumentos
        if args.lang is not None:
            if args.lang == '' and self.r_default_lang:
                print(f"([!] Successfully unset `r` global filter '{self.r_default_lang}')")
                self.r_default_lang = None
            elif args.lang != '':
                self.r_default_lang = args.lang
                print(f"([!] Global filter set for `r` at '{self.r_default_lang}'; 'r -l' to unset)")

        if args.type is not None:
            if args.type == '' and self.r_default_type:
                print(f"([!] Successfully unset `r` global filter '{self.r_default_type}')")
                self.r_default_type = None
            elif args.type != '':
                self.r_default_type = args.type
                print(f"([!] Global filter set for `r` at '{self.r_default_type}'; 'r -t' to unset)")

        # Aplica las restricciones globales para el filtrado solo si están definidas
        lang_constraint = self.r_default_lang if self.r_default_lang else None
        type_constraint = self.r_default_type if self.r_default_type else None

        if args.sos is not None:
            try:
                sos_value = int(args.sos)
                candidates = self.G.edge_count('<=', sos_value)
            except ValueError:
                print("Error: 'sos' argument must be an integer.")
                return
        else:
            candidates = self.G

        new_node = candidates.random(lang=lang_constraint, type=type_constraint, favorite=args.fav)

        if new_node:
            self._set_node(new_node)
        else:
            print('No nodes met the criteria. Try relaxing the constraints.')

    def do_ls(self, arg):
        args = arg.split()

        if args and args[0] in ('y0', 'y1', 'y2', 'e0', 'e1', 'e2'):
            self.placeholder.fields = []
            self.placeholder.update_field('add', args.pop(0))

        parser = argparse.ArgumentParser(description='List information about the current node.')
        parser.add_argument('-d', '--details', action='store_true', default=None, help='Provides a more detailed display.')
        parser.add_argument('-w', '--width', type=int, default=35, help='Width for the column.')
        parser.add_argument('-a', '--abbr', type=int, default=None, help='Abbreviate all results to a maximum length.')
        parser.add_argument('-p', '--stop', type=int, default=None, help='Set a max of nodes to be displayed.')
        parser.add_argument('-c', '--ncol', type=int, default=2, help='Number of columns.')
        parser.add_argument('-r', '--shuffle', action='store_true', help='Shuffles the results.')
        parser.add_argument('-l', '--lang', nargs='?', const='', default=None, help='Filter by language (only for y fields).')
        parser.add_argument('-t', '--type', nargs='?', const='', default=None, help='Filter by type (only for y fields).')
        
        ls_args, unknown = parser.parse_known_args(args)
        
        if unknown:
            padded_print(f'Unrecognized argument(s): {" ".join(unknown)}', tab=0)

        if not self.placeholder.fields:
            padded_print("Error. Search field is needed", tab=0)
            return

        cn = self.placeholder.node
        is_semantic = all(field.startswith('e') for field in self.placeholder.fields)
        is_syntactic = all(field.startswith('y') for field in self.placeholder.fields)

        if not (is_semantic or is_syntactic):
            padded_print("Error. Mixed field types are not allowed. Use only 'y' fields or only 'e' fields.", tab=0)
            return

        if is_semantic:
            entries = []
            for field in self.placeholder.fields:
                # Cambiamos esto para acceder directamente al atributo del nodo
                #field_name = f"semset{field[1]}"  # Convierte 'e0' a 'semset0', 'e1' a 'semset1', etc.
                #entries.extend(getattr(cn, field_name, []))
                entries = cn.get_neighbors(field)
            
            if ls_args.shuffle:
                random.shuffle(entries)
            if ls_args.stop:
                entries = entries[:ls_args.stop]
            
            if len(entries) == 0:
                print("| The set field for the target node is empty.")
            else:
                print(f"Showing {len(entries)} semantic entries:")
                for i, entry in enumerate(entries, 1):
                    print(f"| {i}. {entry}")

        else:  # is_syntactic
            nodes = []
            for field in self.placeholder.fields:
                nodes.extend(cn.get_neighbors(field))
            
            if ls_args.lang:
                if ls_args.lang == '':
                    self.ls_default_lang = None
                    print(f"([!] Successfully unset `ls` global language filter)")
                else:
                    self.ls_default_lang = ls_args.lang
                    print(f"([!] Global language filter set for `ls` at '{self.ls_default_lang}'; 'ls -l' to unset)")
                nodes = [node for node in nodes if node.lang == self.ls_default_lang]

            if ls_args.type:
                if ls_args.type == '':
                    self.ls_default_type = None
                    print(f"([!] Successfully unset `ls` global type filter)")
                else:
                    self.ls_default_type = ls_args.type
                    print(f"([!] Global type filter set for `ls` at '{self.ls_default_type}'; 'ls -t' to unset)")
                nodes = [node for node in nodes if node.type == self.ls_default_type]

            nodes = sorted(nodes, key=lambda node: node.name)

            if ls_args.shuffle:
                random.shuffle(nodes)
            if ls_args.stop:
                nodes = nodes[:ls_args.stop]

            if nodes:
                print(f"(SYS: Started edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
                print(f"Showing {len(nodes)} syntactic entries:")
                
                if ls_args.details:
                    max_index_length = len(str(len(nodes)))
                    for i, node in enumerate(nodes, 1):
                        sizes = [str(i) for i in node.get_sizes()]
                        str_sizes = '/'.join(sizes[:3]) + ' - ' + '/'.join(sizes[3:])
                        print(f"{str(i).zfill(max_index_length)}) [{node.lang}][{node.type}][{node.name}][{node.lemma}]....({str_sizes})")
                else:
                    names = [node.name for node in nodes]
                    if ls_args.abbr:
                        names = [name[:ls_args.abbr] + '...' if len(name) > ls_args.abbr else name for name in names]
                    strings_to_display = [f'| {i+1}. {name}' for i, name in enumerate(names)]
                    formatted_lines = get_n_columns_from_elements(strings_to_display, ncol=ls_args.ncol, col_width=ls_args.width)
                    for line in formatted_lines:
                        print(line)

                if len(self.placeholder.fields) == 1:
                    LS_Interface(nodes, self, ls_args)
            else:
                padded_print('The set field for the target node is empty.', tab=0)

    def do_new(self, name):

        if name:

            lang =  'es'
            type =  't'
            lemma = 'NA' 
            
            matches = self.G.find(lang=lang, type=type, name=name, lemma=lemma)
            if not matches:
                if lang and type and len(lang) == 2 and len(type) == 1:
                    self.G.create_node(lang, type, name, lemma)
                    print("| Node created.")
                    self._set_node(self.G.find(lang=lang, type=type, name=name, lemma=lemma))
                else:
                    print('Failed to validate hash attributes.')
            else:
                print('| The specified set of characteristics already exists.')
                self._set_node(self.G.find(lang=lang, type=type, name=name, lemma=lemma))
        else:
            padded_print('You need to insert the name as argument.')

    # Internal Methods  --------------------
        
    def _set_node(self, new_node):
        if new_node:
            self.placeholder.update_node(new_node)
            if not self.nodes_hist or new_node != self.nodes_hist[-1]:
                self.nodes_hist.append(new_node)

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
        console.print(Markdown("# Suskind Knowledge Graph (script)"))

    # CMD private re-writen methods --------------------
        
    def do_clear(self, arg):
        self.preloop()
        
    def preloop(self):
        os.system('cls')
        self._print_markdown_title()
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER, tab=0)
        print('-'*47)

    def default(self, line):

        # Function to select a node from a list of matched nodes.
        def select_node(matched_nodes):
                
            header_statement = "Did you mean..."
            tail_statement = "(Press Enter to select none)"

            # Convert each node to a compact format suitable for display.
            formatted_nodes = [node._convert_header_to_compact_format() for node in matched_nodes]
            
            # Display the selection interface with formatted nodes and get user response.
            SelectInterface(formatted_nodes, self, header_statement, tail_statement).cmdloop()
            response = self._get_response()
            
            # Return the selected node based on user input or None if no selection was made.
            return matched_nodes[int(response)-1] if response else None

        # Handling command line input for node manipulation.
        if (line.startswith('y') or line.startswith('e')) and len(line)==2:
            # Clear existing fields for placeholder if the line matches specific fields.
            self.placeholder.fields = []
            self.placeholder.update_field('add', line)
        elif (line.startswith('y') or line.startswith('e')) and len(line)==1:
            # Reset fields and expand command shorthand for further processing.
            self.placeholder.fields = []
            if line == 'e':
                line = ['e0', 'e1', 'e2']
            elif line == 'y':
                line = ['y0', 'y1', 'y2']
            for _ in line:
                self.placeholder.update_field('add', _)

        elif len(line) > 2:
            if len(self.placeholder.fields) == 1:
                cn = self.placeholder.node
                cf = self.placeholder.fields[0]

                if cf.startswith('y'):
                    # Proceso para campos sintácticos (y0, y1, y2)
                    matches = self.G.select(name=line)
                    selected_node = None
                    if matches:
                        if len(matches) > 1:
                            selected_node = select_node(matches)
                        else:
                            selected_node = matches[0]
                    else:
                        print('(SYS: Name does not match any node. Fill to create it.)')
                        lang = 'es'
                        type = input('> type  : ').strip()
                        lemma = 'NA'
                        if lang and type and len(lang) == 2 and len(type) == 1:
                            if not self.G.select(lang=lang, type=type, name=line, lemma=lemma):
                                self.G.create_node(lang, type, line, lemma)
                                print("| Node created.")
                                selected_node = self.G.select(lang=lang, type=type, name=line, lemma=lemma)[0]
                            else:
                                print('| The specified set of characteristics already exists.')
                        elif lang or type or lemma:
                            print('Failed to validate hash attributes.')

                    if selected_node:
                        if selected_node != cn:
                            self.G.bind(cn, selected_node, cf)
                            print(f"| Successfully binded '{selected_node.name}'.")
                        else:
                            print("Can't bind node to itself.")
                else:
                    # Proceso para campos semánticos (e0, e1, e2)
                    self.G.bind(cn, line, cf)
                    print(f"| Successfully added '{line}' to {cf}.")
            else:
                padded_print("Select a single valid fielding.")
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)
    
    def do_edit(self, arg):

        # Parse the input arguments
        args = arg.split()
        if len(args) < 2:
            print("Error: Invalid syntax. Use 'edit [attribute] [new_value]'.")
            return

        attribute, new_value = args[0], ' '.join(args[1:])
        cn = self.placeholder.node

        # Check if the attribute is valid
        valid_attributes = ['lang', 'type', 'name', 'lemma']
        if attribute not in valid_attributes:
            print(f"Error: Unknown attribute '{attribute}'. Valid attributes are {', '.join(valid_attributes)}.")
            return

        # Check if the new value is the same as the current value
        current_value = getattr(cn, attribute)
        if new_value == current_value:
            print("The new value must be different from the current.")
            return
        
        # Algorithm ---

        # Prepare the query dynamically based on the attribute being edited
        query = {attr: getattr(cn, attr) if attr != attribute else new_value for attr in valid_attributes}
        # {lang: cn.lang, type: cn.type, name: cn.name, lemma: new_value}

        if self.G.find(**query):
            perfect_match_node = self.G.find(**query)
            self.G.merge_nodes(cn, perfect_match_node)                        
            print('The conformed node matched an existing one, and has been merged.')
        else:
            # Apply the change
            print('Change applied successfully.')
        
        getattr(cn, 'edit')(**{attribute: new_value})

        self.placeholder.update_node(self.placeholder.node)
    
    def do_tag(self, arg):
        try:
            if arg:
                self.add_filter_tag(arg)
            else:
                print("Usage: tag <new_tag>")
        except Exception as e:
            print(f"An error occurred while adding tag: {e}")

    def do_tags(self, arg):
        try:
            if not self.filter_tags:
                print("No tags set.")
            else:
                print("Current tags:")
                for i, tag in enumerate(self.filter_tags, 1):
                    print(f"| {i}. {tag}")
                
                while True:
                    user_input = input(">> ")
                    if not user_input:
                        break
                    elif user_input.startswith("del "):
                        self.delete_filter_tag(user_input[4:])
                    else:
                        print("Invalid command. Use 'del <tag_name_or_index>' or press Enter to exit.")
                
            self.show_expected_results()
        except Exception as e:
            print(f"An error occurred in tags command: {e}")

    def add_filter_tag(self, tag):
        if tag not in self.filter_tags:
            self.filter_tags.append(tag)
            padded_print(f"Tag '{tag}' added successfully.")
        else:
            padded_print(f"Tag '{tag}' already exists.")
        self.show_expected_results()

    def delete_filter_tag(self, identifier):
        if identifier.isdigit():
            index = int(identifier) - 1
            if 0 <= index < len(self.filter_tags):
                deleted_tag = self.filter_tags.pop(index)
                padded_print(f"Tag '{deleted_tag}' deleted successfully.")
            else:
                padded_print("Invalid index.")
        else:
            if identifier in self.filter_tags:
                self.filter_tags.remove(identifier)
                padded_print(f"Tag '{identifier}' deleted successfully.")
            else:
                padded_print(f"Tag '{identifier}' not found.")

    def show_expected_results(self):
        stats = self.get_filter_stats()
        results = []
        
        for i in range(1, 6):  # Máximo de 5 'qt' contadores
            if f'qt{i}' in stats:
                results.append(f"qt({i})={stats[f'qt{i}']}")
        
        print("Expected results | " + " ".join(results))

    def do_filter(self, arg):
        try:
            threshold = 1.0
            if arg:
                try:
                    threshold = float(arg)
                    if not 0 <= threshold <= 1:
                        raise ValueError
                except ValueError:
                    padded_print("Invalid threshold. Please enter a number between 0 and 1.")
                    return

            matching_nodes = self.apply_filter(threshold)

            if matching_nodes:
                padded_print(f"Found {len(matching_nodes)} matching nodes:")
                for i, node in enumerate(matching_nodes, 1):
                    padded_print(f"{i}. {node.name}")
            else:
                padded_print("No matching nodes found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def apply_filter(self, threshold):
        matching_nodes = []
        total_tags = len(self.filter_tags)
        if total_tags == 0:
            padded_print("No filter tags set. Use 'tag' command to add tags.")
            return matching_nodes
        
        for node in self.G:
            try:
                semantic_content = ' '.join(item for i in range(3) for item in getattr(node, f'semset{i}', []) if item != '')
                matched_tags = sum(tag.lower() in semantic_content.lower() for tag in self.filter_tags)
                if matched_tags / total_tags >= threshold:
                    matching_nodes.append(node)
            except Exception as e:
                padded_print(f"Error processing node {node.name}: {e}")
        
        return matching_nodes

    def get_filter_stats(self):
        stats = Counter()
        total_tags = len(self.filter_tags)
        
        if total_tags == 0:
            print("No filter tags set. Use 'tag' command to add tags.")
            return stats
        
        max_qt = min(total_tags, 5)  # Limit to a maximum of 5 'qt' counters
    
        for node in self.G:
            try:
                semantic_content = ' '.join(item for i in range(3) for item in getattr(node, f'semset{i}', []) if item != '')
                matched_tags = sum(tag.lower() in semantic_content.lower() for tag in self.filter_tags)

                for i in range(1, max_qt + 1):
                    if matched_tags >= i:
                        stats[f'qt{i}'] += 1
            except Exception as e:
                print(f"Error processing node {node.name}: {e}")
        
        return stats

    def do_sug(self, arg):
        """Suggest nodes or semantic elements for binding based on semantic similarity or randomly."""
        if len(self.placeholder.fields) != 1:
            print("Error: This function requires exactly one active field.")
            return

        current_field = self.placeholder.fields[0]
        current_node = self.placeholder.node

        is_syntactic = current_field.startswith('y')
        
        def get_semantic_content(node):
            return set(item for i in range(3) for item in getattr(node, f'semset{i}', []) if item)

        current_semantic_content = get_semantic_content(current_node)

        if is_syntactic:
            # Exclude the current node and nodes already connected in this field
            all_nodes = [node for node in self.G if node != current_node and node not in getattr(current_node, f'synset{current_field[1]}', [])]
            
            if current_semantic_content:
                similar_nodes = sorted(
                    all_nodes,
                    key=lambda node: len(get_semantic_content(node) & current_semantic_content),
                    reverse=True
                )
                similar_nodes = [node for node in similar_nodes if get_semantic_content(node) & current_semantic_content]
            else:
                similar_nodes = []

            total_similar = len(similar_nodes)
            print(f"| Found {total_similar} nodes with semantic similarity.")
            
            suggested = set()

            # First, suggest similar nodes
            for i, node in enumerate(similar_nodes):
                user_input = input(f"| [{i+1}/{total_similar}] {node.name} [Y/N] (q to quit) > ").lower()

                if user_input in ['q', 'exit']:
                    print("| Exiting suggestion mode.")
                    return
                elif user_input == 'y':
                    self.G.bind(current_node, node, current_field)
                    print(f"| Nodes successfully binded through {current_field}")
                    suggested.add(node)
                elif user_input in ['', 'n']:
                    suggested.add(node)
                    continue
                else:
                    print("| Invalid input. Skipping this suggestion.")
                    suggested.add(node)

            # Then, suggest random nodes
            random_nodes = [node for node in all_nodes if node not in similar_nodes and node not in suggested]
            random.shuffle(random_nodes)

            if random_nodes:
                print("| The following suggestions are purely random.")

            for i, node in enumerate(random_nodes):
                user_input = input(f"| [{i+1}/{len(random_nodes)}] {node.name} [Y/N] (q to quit) > ").lower()

                if user_input in ['q', 'exit']:
                    print("| Exiting suggestion mode.")
                    return
                elif user_input == 'y':
                    self.G.bind(current_node, node, current_field)
                    print(f"| Nodes successfully binded through {current_field}")
                elif user_input in ['', 'n']:
                    continue
                else:
                    print("| Invalid input. Skipping this suggestion.")

        else:
            # For semantic fields, suggest semantic elements
            all_nodes = [node for node in self.G if node != current_node]
            
            if current_semantic_content:
                similar_nodes = sorted(
                    all_nodes,
                    key=lambda node: len(get_semantic_content(node) & current_semantic_content),
                    reverse=True
                )
                similar_nodes = [node for node in similar_nodes if get_semantic_content(node) & current_semantic_content]
            else:
                similar_nodes = []

            semantic_suggestions = set()
            for node in similar_nodes:
                semantic_suggestions.update(get_semantic_content(node) - current_semantic_content)
            
            semantic_suggestions = list(semantic_suggestions)
            random.shuffle(semantic_suggestions)

            total_similar = len(semantic_suggestions)
            print(f"| Found {total_similar} semantic elements from similar nodes.")

            suggested = set()

            # First, suggest similar semantic elements
            for i, item in enumerate(semantic_suggestions):
                user_input = input(f"| [{i+1}/{total_similar}] {item} [Y/N] (q to quit) > ").lower()

                if user_input in ['q', 'exit']:
                    print("| Exiting suggestion mode.")
                    return
                elif user_input == 'y':
                    self.G.bind(current_node, item, current_field)
                    print(f"| Successfully added '{item}' to {current_field}")
                elif user_input in ['', 'n']:
                    suggested.add(item)
                    continue
                else:
                    print("| Invalid input. Skipping this suggestion.")
                    suggested.add(item)

            # Then, suggest random semantic elements
            if total_similar == 0 or len(suggested) == total_similar:
                print("| No more similar semantic elements. Suggesting random semantic elements.")
                random_semantic_elements = set()
                for node in all_nodes:
                    random_semantic_elements.update(get_semantic_content(node) - current_semantic_content - suggested)
                random_semantic_elements = list(random_semantic_elements)
                random.shuffle(random_semantic_elements)

                for i, item in enumerate(random_semantic_elements):
                    user_input = input(f"| [{i+1}/{len(random_semantic_elements)}] {item} [Y/N] (q to quit) > ").lower()

                    if user_input in ['q', 'exit']:
                        print("| Exiting suggestion mode.")
                        return
                    elif user_input == 'y':
                        self.G.bind(current_node, item, current_field)
                        print(f"| Successfully added '{item}' to {current_field}")
                    elif user_input in ['', 'n']:
                        continue
                    else:
                        print("| Invalid input. Skipping this suggestion.")

        print("| Suggestions exhausted.")
        
    def do_back(self, arg):
        """Return to the main menu to select a different mode."""
        print("~\n\033[90mReturning to main menu...\033[0m")
        self.should_restart = True
        do_save = input('\033[93mWARNING:\033[0m do you want to save the current version? [Y/N]\n> ')
        if do_save not in {'no', 'NO', 'N', 'n'}:
            self.do_save("")
        return True

    def do_exit(self, arg):
        """Exit the program completely."""
        print("\n\033[92mExiting the program...\033[0m")
        self.should_restart = False
        return True

    def do_q(self, arg):
        """Quick exit, same as 'exit'."""
        return self.do_exit(arg)
