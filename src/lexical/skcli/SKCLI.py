import os
import re
import cmd
import random
import argparse

import src.lexical.sktools as sk

from src.lexical.skcli.skplaceholder import *
from src.lexical.skcli.aux_clis import *

from src.lexical.skcomponents.search_algorithms import *

from src.lexical.skcli.aux_funcs.err_mssg import *
from src.lexical.skcli.aux_funcs.visuals import *
from src.lexical.skcli.aux_funcs.command_docstrings import *

from pathlib import Path
import shutil
import datetime

class LexicalInterface (cmd.Cmd):
    
    def __init__(self, graph):
        super().__init__()
        self.G = graph
        self.should_restart = False
        self.placeholder = Placeholder(self)
        self.response = None
        self.tagged_nodes = []

        self.nodes_hist = []

        self._set_random_node()

        self.ls_default_lang = None
        self.ls_default_type = None

        self.r_default_lang = None
        self.r_default_type = None

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
    
    def do_sug(self, arg):

        # Define a helper function to flatten a list of lists into a single list.
        def flatten(lst):
            return [item for subset in lst for item in subset]
        
        # Check if there is exactly one field in the placeholder; proceed only if true.
        if len(self.placeholder.fields) == 1:

            cn = self.placeholder.node  # Current node being considered for suggestions.
            cf = self.placeholder.fields[0]  # Current field being considered for suggestions.
        
            # Suggestion logic for different singular fields.

            if cf == 'y0':
                y1 = cn.get_neighbors('y1')  # Retrieve neighbors connected via 'y1'.
                y1_y0 = flatten([neighbor.get_neighbors('y0') for neighbor in y1])  # Flatten list of neighbors' neighbors connected via 'y0'.
                
                suggestions = y1_y0  # Compile suggestions list.

            if cf == 'y1':
                y1 = cn.get_neighbors('y1')
                y1_y1 = flatten([neighbor.get_neighbors('y1') for neighbor in y1])
                y1_y1_y1 = flatten([neighbor.get_neighbors('y1') for neighbor in y1_y1])

                y2 = cn.get_neighbors('y1')
                y2_y1 = flatten([neighbor.get_neighbors('y1') for neighbor in y2])

                e = cn.get_neighbors('e')
                e_y = flatten([neighbor.get_neighbors('y') for neighbor in e])

                intersection = centrality(list(set(e+e_y)), 'e')[1]
                e_y_ie = [neighbor for neighbor, rating in intersection.items() if rating > 0.35]
                e_y_ie = NodeSet(e_y_ie).select(type=cn.type)

                suggestions = y1_y1 + y1_y1_y1 + y2_y1 + e_y_ie
            
            if cf == 'y2':
                y1 = cn.get_neighbors('y1')
                y1_y2 = flatten([neighbor.get_neighbors('y2') for neighbor in y1])

                suggestions = y1_y2
            
            if cf == 'e0':
                y1 = cn.get_neighbors('y1')
                y1_e0 = flatten([neighbor.get_neighbors('e0') for neighbor in y1])

                e = cn.get_neighbors('e')
                e_e = flatten([neighbor.get_neighbors('e') for neighbor in e])

                suggestions = y1_e0 + e_e

            if cf == 'e1':
                y1 = cn.get_neighbors('y1')
                y1_e1 = flatten([neighbor.get_neighbors('e1') for neighbor in y1])

                e = cn.get_neighbors('e')
                e_e = flatten([neighbor.get_neighbors('e') for neighbor in e])
                
                suggestions = y1_e1 + e_e
            
            if cf == 'e2':
                y1 = cn.get_neighbors('y1')
                y1_e2 = flatten([neighbor.get_neighbors('e2') for neighbor in y1])

                e = cn.get_neighbors('e')
                e_e = flatten([neighbor.get_neighbors('e') for neighbor in e])
                
                suggestions = y1_e2 + e_e
            
            # Finalize the suggestions by removing duplicates and any direct neighbors.
            suggestions = NodeSet(list(set([n for n in suggestions if n not in cn.get_neighbors()])))

            # Ensure the current node is not included in its own suggestions.
            if cn in suggestions:
                suggestions.remove(cn)
            # Also remove any direct neighbors connected via the current field.
            for n in cn.get_neighbors(cf):
                if n in suggestions:
                    suggestions.remove(n)

            # Inform the user that the suggestion session has started.
            print(f"(SYS: Started sug-session at {datetime.datetime.now().strftime('%H:%M:%S')}. Type 'q' to leave.)")
            
            ch = None
            randomize = True # Flag to control random suggestion selection.
            while ch not in ['q','exit']:
                if randomize:
                    rn = suggestions.random() # Select a random suggestion if flag is set.

                if rn:
                    # Prompt user for input regarding the current suggestion.
                    ch = input(f"| {rn._convert_header_to_compact_format()} [Y/N (/e_/y_)] >> ")
                    randomize = True # Reset randomization flag for next loop iteration.

                    if ch in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']:
                        # If the user inputs a specific field, bind the current node to the suggested node with that field.
                        self.G.bind(cn, rn, ch)
                        padded_print(f"Successfully binded node to '{ch}' field.")
                    elif ch in ['Y','y']:
                        # If the user confirms the suggestion without specifying a field, use the current field for binding.
                        self.G.bind(cn, rn, cf)
                        padded_print(f"Successfully binded node to '{cf}' field.")
                    elif ch in ['N','n','']:
                        # If the user rejects the suggestion or inputs an empty response, do nothing and loop for a new suggestion.
                        pass
                    elif ch in ['q','exit']:
                        # If the user wants to exit, set the loop control variable to quit.
                        pass
                    else:
                        # If the input is invalid, prompt the user again without changing the suggestion.
                        randomize = False
                        padded_print('Please, enter a valid input.')
                else:
                    # If no suggestions are available, exit the loop.
                    ch = 'q'
                    padded_print('No suggestions found.')

            print(f"(SYS: Ended sug-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        
        else:
            padded_print('Select one and only field.')

    
    def do_vg(self, arg):
        examples = self.placeholder.node.examples
        if examples not in [[],['']]:
            print(f"(SYS: Started vg-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
            padded_print(f'Showing {len(examples)} example(s):')
            for i, example in enumerate(examples):
                padded_print(f"{i}) {example}", tab=1)
        else:
            padded_print('There are no examples.')
        action = input('>> ').split()
        while action:
            if action[0] == 'del':
                action.pop(0)
                idxs = sk.parse_idxs_to_single_idxs(' '.join(action))
                exs = [ex for i, ex in enumerate(self.placeholder.node.examples) if i in idxs]
                for ex in exs:
                    self.placeholder.node.examples.remove(ex)
                padded_print(f'Removed {len(exs)} example(s).')
            elif action[0] == '?':
                action.pop(0)
                if len(action)!=0:
                    arg = action.pop(0)
                    help_text = COMMAND_DOCSTRINGS_VG.get(arg)
                    print(help_text)
                else:
                    padded_print('Available commands:')
                    padded_print('___ : Adds an example for the node.')
                    padded_print('del : Deletes the given examples')
            else:
                new_example = ' '.join(action)
                if new_example not in self.placeholder.node.examples:
                    if '' in self.placeholder.node.examples:
                        self.placeholder.node.examples.remove('')
                    self.placeholder.node.examples.append(new_example)
                    padded_print('Added the last example.')
            action = input('>> ').split()
        print(f"(SYS: Ended vg-session at {datetime.datetime.now().strftime('%H:%M:%S')})")        

    def do_save(self, arg):
        filename = arg.strip() or 'lexical.txt'  # Use 'lexical.txt' as default filename if none is provided
        file_path = Path(filename)
        backup_dir = Path('sec_copy') / 'lexical'
        
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
                    number_of_guesses = 4
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
                else:
                    return

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

    def do_rtag(self, arg):
        try:
            count = int(arg)
            if count <= 0:
                print("Please provide a positive integer.")
                return
            
            new_nodes = []
            for _ in range(count):
                random_node = self.G.random()
                if random_node not in self.tagged_nodes:
                    self.tagged_nodes.append(random_node)
                    new_nodes.append(random_node)

            if new_nodes:
                print(f"Successfully added {len(new_nodes)} random nodes:")
                for node in new_nodes:
                    print(f"> Tagged {node._convert_header_to_compact_format()}")
            else:
                print("No new nodes were added. All randomly selected nodes were already tagged.")

        except ValueError:
            print("Invalid input. Please provide a valid integer.")

    def do_tag(self, arg):

        if arg:
            # tag ____
            parser = argparse.ArgumentParser()
            parser.add_argument('name', nargs='*', help='The name to search for')
            parsed_args = parser.parse_args(arg.split())
            parsed_name = ' '.join(parsed_args.name)

            nodes = self.G.select(name=parsed_name)

            if len(nodes) == 1:
                self.tagged_nodes.append(nodes[0])

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
                    if target_node not in self.tagged_nodes:
                        self.tagged_nodes.append(target_node)

        else:
            # tag (will tag the current)
            if self.placeholder.node not in self.tagged_nodes:
                self.tagged_nodes.append(self.placeholder.node)
    
    def do_tagged(self, arg):
        GB_Interface(self)
    
    def do_details(self, arg):

        node = self.placeholder.node
        sizes = node.get_sizes()
        synset_sizes = ', '.join([f'y{i} = {size}' for i, size in enumerate(node.get_sizes()[:3])])
        semset_sizes = ', '.join([f'e{i} = {size}' for i, size in enumerate(node.get_sizes()[3:])])
        padded_print(f'Synset sizes ({synset_sizes})')
        padded_print(f'Semset sizes ({semset_sizes})')
    
    def do_run(self, arg):

        print(f"(SYS: Started search-session at {datetime.datetime.now().strftime('%H:%M:%S')})")

        parser = argparse.ArgumentParser(description='Run density search with specified parameters.')
        parser.add_argument('k', nargs='?', type=int, help='MSL (Minimum Shared Linkage) as an integer.', default=None)
        parser.add_argument('-f', '--fielding', action='store_true', help='Restricts the search to results within the placeholder fielding.')
        parser.add_argument('-d', '--details', action='store_true', help='Provides a more detailed display.')
        parser.add_argument('-w', '--width', type=int, default=35, help='Width for the column.')
        parser.add_argument('-a', '--abbr', type=int, default=None, help='Abbreviate all results to a maximum length.')
        parser.add_argument('-p', '--stop', type=int, default=None, help='Set a max of nodes to be displayed.')
        parser.add_argument('-c', '--ncol', type=int, default=4, help='Number of columns.')
        parser.add_argument('-r', '--shuffle', action='store_true', help='Shuffles the results.')

        parser.add_argument('-l', '--lang', default=None, help='Restricts the results to the given lang.')
        parser.add_argument('-t', '--type', default=None, help='Restricts the results to the given type.')

        ls_args, unknown = parser.parse_known_args(arg.split())
        if unknown:
            print(f'Unrecognized argument(s): {" ".join(unknown)}')
            return
        
        # Handle the k value for density search
        k = (str(ls_args.k) if ls_args.k else None) or input(">> MSL (Minimum Shared Linkage) [int] : ")
        while not k.isdigit() or int(k) > len(self.tagged_nodes):
            if not k.isdigit():
                print("Please, enter a valid integer.")
            elif int(k) > len(self.tagged_nodes):
                print(f"Please, enter an integer <{len(self.tagged_nodes)} (selectable nodes).")
            k = input(">> Minimum Shared Linkage (MSL) : ")
        k = int(k)

        fielding = self.placeholder.fields if ls_args.fielding else []

        # Perform the density search (excludes original ones)
        output_nodes = NodeSet([node for node in density_search(self.tagged_nodes, k, *fielding) if node not in self.tagged_nodes])

        if ls_args.lang:
            output_nodes = output_nodes.select(lang=ls_args.lang)
        if ls_args.type:
            output_nodes = output_nodes.select(type=ls_args.type)

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

    def do_rvg(self, args):
        parser = argparse.ArgumentParser(description="Random example viewer and searcher")
        parser.add_argument('search_string', nargs='*', default=None, help='String to search for in examples')
        parser.add_argument('--caps', action='store_true', help='Match case for search string')
        
        try:
            parsed_args = parser.parse_args(args.split())
        except SystemExit:
            return

        examples = []
        for n in self.G:
            examples.extend(n.examples)
        
        examples = list(set(examples))  # Remove duplicates
        if '' in examples:
            examples.remove('')

        if parsed_args.search_string:
            search_string = ' '.join(parsed_args.search_string)
            
            # Create a regex pattern for whole word/phrase matching
            if parsed_args.caps:
                pattern = r'\b' + re.escape(search_string) + r'\b'
                regex = re.compile(pattern)
                matching_examples = [ex for ex in examples if regex.search(ex)]
            else:
                pattern = r'\b' + re.escape(search_string) + r'\b'
                regex = re.compile(pattern, re.IGNORECASE)
                matching_examples = [ex for ex in examples if regex.search(ex)]
            
            if matching_examples:
                print(f"Found {len(matching_examples)} matching examples, v.g.:")
                print('***')
                print(random.choice(matching_examples))
                print('***')
            else:
                print(f"No examples found containing the exact word/phrase '{search_string}'")
        else:
            print('***')
            print(random.choice(examples))
            print('***')
  

    def do_r(self, args):
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
                print(f"([!] Succesfully unset `r` global filter '{self.r_default_lang}')")
                self.r_default_lang = None  # Elimina la restricción si el argumento es una cadena vacía
            elif args.lang != '':
                if args.lang != self.r_default_lang:
                    self.r_default_lang = args.lang  # Actualiza la restricción global
                    print(f"([!] Global filter set for `r` at '{self.r_default_lang}'; 'r -l' to unset)")

        if args.type is not None:
            if args.type == '' and self.r_default_type:
                print(f"([!] Succesfully unset `r` global filter '{self.r_default_type}')")
                self.r_default_type = None  # Elimina la restricción si el argumento es una cadena vacía
            elif args.type != '':
                if args.type != self.r_default_type:
                    self.r_default_type = args.type  # Actualiza la restricción global
                    print(f"([!] Global filter set for `r` at '{self.r_default_type}'; 'r -t' to unset)")

        # Aplica las restricciones globales para el filtrado
        lang_constraint = self.r_default_lang
        type_constraint = self.r_default_type

        if args.sos is not None:
            try:
                sos_value = int(args.sos)  # Try to convert args.sos to an integer
                candidates = self.G.edge_count('<=', sos_value)
            except ValueError:
                print("Error: 'sos' argument must be an integer.")
                return  # Exit the function or handle the error as appropriate
        else:
            candidates = self.G  # No 'sos' filter applied
    
        new_node = candidates.random(lang=lang_constraint, type=type_constraint, favorite=args.fav)

        if new_node:
            self._set_node(new_node)
        else:
            padded_print('No nodes met the criteria.', tab=0)

    def do_ls(self, arg):
        args = arg.split()

        if args and args[0] in ('y0', 'y1', 'y2', 'e0', 'e1', 'e2'):
            self.placeholder.fields = []
            self.placeholder.update_field('add', args.pop(0))  # Switch the placeholder field

        # Now, handle the remaining arguments as the node_name
        node_name = []
        while args and not args[0].startswith('-'):
            node_name.append(args.pop(0))

        if node_name:
            # Unir todas las partes del nombre del nodo
            node_name = ' '.join(node_name)
            if not self.do_cd(node_name):
                return

        parser = argparse.ArgumentParser(description='List information about the current node.')
        parser.add_argument('-d', '--details', action='store_true', default=None, help='Provides a more detailed display.')
        parser.add_argument('-w', '--width', type=int, default=35, help='Width for the column.')
        parser.add_argument('-a', '--abbr', type=int, default=None, help='Abbreviate all results to a maximum length.')
        parser.add_argument('-p', '--stop', type=int, default=None, help='Set a max of nodes to be displayed.')
        parser.add_argument('-c', '--ncol', type=int, default=2, help='Number of columns.')
        parser.add_argument('-r', '--shuffle', nargs='?', const=0, type=int, help='Shuffles the results. Optional: specify number of random entries to display.')
        parser.add_argument('-l', '--lang', nargs='?', const='', default=None, help='Filter by language and sets it as default for following "ls". No argument resets to default.')
        parser.add_argument('-t', '--type', nargs='?', const='', default=None, help='Filter by type and sets it as default for following "ls". No argument resets to default.')
        
        ls_args, unknown = parser.parse_known_args(args)
        
        if unknown:
            padded_print(f'Unrecognized argument(s): {" ".join(unknown)}', tab=0)

        if self.placeholder.fields:
            nodes = self.placeholder.node.get_neighbors(self.placeholder.fields)

            # Reset language filter if '-l' is used without an argument.
            if ls_args.lang == '':
                print(f"([!] Successfully unset `ls` global filter '{self.ls_default_lang}')")
                self.ls_default_lang = None
            elif ls_args.lang is not None:
                self.ls_default_lang = ls_args.lang

            if ls_args.type == '':
                self.ls_default_type = None
                print(f"([!] Successfully unset `ls` global filter '{self.ls_default_type}')")
            elif ls_args.type is not None:
                self.ls_default_type = ls_args.type
                
            if self.ls_default_lang:
                print(f"([!] Global filter set for `ls` at '{self.ls_default_lang}'; 'ls -l' to unset)")
                nodes = nodes.select(lang=self.ls_default_lang)
            if self.ls_default_type:
                print(f"([!] Global filter set for `ls` at '{self.ls_default_type}'; 'ls -t' to unset)")
                nodes = nodes.select(type=self.ls_default_type)

            nodes = sorted(nodes, key=lambda node: node.name)

            if nodes:
                if ls_args.shuffle is not None:
                    random.shuffle(nodes)
                    if ls_args.shuffle > 0:
                        nodes = nodes[:ls_args.shuffle]
                elif ls_args.stop:
                    if ls_args.stop <= len(nodes):
                        nodes = nodes[:ls_args.stop]

                if ls_args.details:
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

    def do_new(self, name):

        if name:

            lang =  'es'
            type =  input('> type  : ').strip()
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
        console.print(Markdown("# Suskind Knowledge Graph (lexical)"))

    # CMD private re-writen methods --------------------
        
    def do_clear(self, arg):
        self.preloop()
        
    def preloop(self):
        os.system('cls')
        self._print_markdown_title()
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER, COMMON_COMMANDS, EXPANSION_COMMANDS, tab=0)
        padded_print()
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
        
        # Function to bind a node to the current node with a specified edge type.
        def bind_node(current_node, selected_node, edge_type):
            # Check if the selected node is not already a neighbor with the specified edge type.
            if selected_node and not selected_node in current_node.get_neighbors(edge_type):
                # If not, bind the nodes together with the specified edge type.
                self.G.bind(current_node, selected_node, edge_type)
                print(f"| Successfully binded '{selected_node.name}'.")
            elif selected_node:
                # Inform if the node was already present and thus not added again.
                print('| The node was already present.')

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
        elif len(line)>2:
            if len(self.placeholder.fields)==1:
                # Attempt to match or create node based on extended input.
                matches = self.G.select(name=line)
                selected_node = None
                if matches:
                    # Handle multiple matches through selection or direct assignment.
                    if len(matches) > 1:
                        selected_node = select_node(matches)
                    else:
                        selected_node = matches[0]
                
                else:
                    # If no matches, prompt for node creation.
                    print('(SYS: Name does not match any node. Fill to create it.)')
                    lang =  'es'
                    type =  input('> type  : ').strip()
                    lemma = 'NA' 
                    # Validate inputs for new node creation.
                    if lang and type and len(lang) == 2 and len(type) == 1:
                        # Check if a node with specified characteristics exists, create if not.
                        if not self.G.select(lang=lang, type=type, name=line, lemma=lemma):
                            self.G.create_node(lang, type, line, lemma)
                            print("| Node created.")
                            selected_node = self.G.select(lang=lang, type=type, name=line, lemma=lemma)[0]
                        else:
                            print('| The specified set of characteristics already exists.')
                    elif lang or type or lemma:
                        # Fail if any validation for the new node attributes fails.
                        print('Failed to validate hash attributes.')
                        
                # Binding or linking logic if a selected or created node is available.
                cn = self.placeholder.node
                cf = self.placeholder.fields[0]

                if selected_node:
                    if selected_node!=self.placeholder.node:
                        bind_node(cn, selected_node, cf)
                    else:
                        padded_print("Can't bind node to itself.")
            else:
                padded_print("Select a single valid fielding.")
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", tab=0)

    def do_edit(self, arg):

        # Checks ---

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
