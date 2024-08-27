import cmd 
import datetime
import random

from itertools import combinations

from src.lexical.skcli.aux_funcs.visuals import *
from src.lexical.skcli.aux_funcs.command_docstrings import *
from src.lexical.skcli.aux_funcs.err_mssg import *

from src.lexical.skcomponents.search_algorithms import *

class LS_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, listed_nodes, parent_cli, ls_args):
        super().__init__()
        self.ls_node = parent_cli.placeholder.node
        self.listed_nodes = listed_nodes
        self.parent_cli = parent_cli
        self.ls_args = ls_args
        self.response = None
        self.cmdloop()
    
    def do_cd(self, index): # finisehd
        if index.isdigit():
            new_current_node = self.listed_nodes[int(index)-1]
            self.parent_cli._set_node(new_current_node)
            return True
        else:
            print('Index must be digit.')
    
    def do_ls(self, arg=None):

        if arg:
            print("(SYS: arguments for 'ls' are disabled within the edit session)")
        self._update_listed_nodes()
        if not self.listed_nodes:
            print("The set field for the target node is empty.")
        strings_to_display = [f'| {i + 1}. {name}' for i, name in enumerate([node.name for node in self.listed_nodes])]

        if len(self.listed_nodes):
            print(f"Showing {len(self.listed_nodes)}/{len(self.listed_nodes)} results.")

        formatted_lines = get_n_columns_from_elements(strings_to_display, ncol=self.ls_args.ncol, col_width=self.ls_args.width)
        for line in formatted_lines:
            print(line)

    def do_clear(self, arg):

        field_symb = self.parent_cli.placeholder.fields[0]
        field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]

        ch = input(f'SYS: Are you sure you want to clear this field? [Y/N]\n>> ')
        if ch in {'Y','y'}:
            for node in self.listed_nodes:
                self.parent_cli.G.unbind(self.ls_node, node, field)
            print('Field succesfully cleared.')
            return True
        else:
            print('Cleansing process aborted.')


    def do_del(self, args):
        def is_numeric_or_range(s):
            return all(part.isdigit() or part == '-' for part in s.split('-'))

        def find_indices(arg):
            if is_numeric_or_range(arg):
                return sk.parse_idxs_to_single_idxs(arg)
            return [i + 1 for i, node in enumerate(self.listed_nodes) if node.name == arg]

        if not args:
            print("Error: No arguments provided.")
            return

        # Check if all arguments are numeric or ranges
        if all(is_numeric_or_range(arg) for arg in args.split()):
            idxs = set()
            for arg in args.split():
                idxs.update(find_indices(arg))
        else:
            # If not all numeric, treat the entire argument as a single node name
            idxs = set(find_indices(args))

        if not idxs:
            print(f"Error: No nodes found to delete with the argument '{args}'")
            return

        field_symb = self.parent_cli.placeholder.fields[0]
        field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]

        unbind_cases = []
        for idx in sorted(idxs):
            if 1 <= idx <= len(self.listed_nodes):
                unbind_cases.append((self.listed_nodes[idx-1], field))
            else:
                print(f"Warning: Index {idx} out of range")

        for target_node, field in unbind_cases:
            self.parent_cli.G.unbind(self.ls_node, target_node, field)

        padded_print(f"Deleted {len(unbind_cases)} nodes.")

        self.do_ls()
    
    def do_tag(self, idxs):
        idxs = sk.parse_idxs_to_single_idxs(idxs) # accepts ranges as 5-8 (5,6,7,8)
        if not idxs:
            idxs = list(range(len(self.listed_nodes)))
        for idx in idxs:
            target_node = self.listed_nodes[idx-1]
            if target_node not in self.parent_cli.tagged_nodes:
                self.parent_cli.tagged_nodes.append(target_node)

        padded_print(f'Tagged {len(idxs)} nodes.')
    
    def do_cross(self, args):
        # Divide los argumentos en índices y tipo de relación
        parts = args.split()
        idxs = ' '.join(parts[:-1])  # Todos menos el último
        relation_type = parts[-1]  # Último argumento

        # Verifica si el tipo de relación es válido
        if relation_type not in ['y', 'e']:
            print("Invalid relation type. Use 'y' or 'e'.")
            return

        # Utiliza la función existente para convertir rangos en índices individuales
        idxs = sk.parse_idxs_to_single_idxs(idxs)

        selected_nodes = [self.listed_nodes[idx - 1] for idx in idxs] if idxs else self.listed_nodes

        # Bindea los nodos seleccionados
        for node1, node2 in combinations(selected_nodes, 2):
            # Bindea cada par de nodos
            self.parent_cli.G.bind(node1, node2, relation_type + '1')

        n_conn = len(selected_nodes)

        print(f"Nodes successfully binded ({int((n_conn*(n_conn-1))/2)} conn.) through '{relation_type + '1'}' field.")

    def default(self, line):

        line = line.strip()
        if line[0] in {'y', 'e'} and line[1] in {'0', '1', '2'} and len(line)==2:
            self.parent_cli.placeholder.fields = []
            self.parent_cli.placeholder.update_field('add', line)
            self.do_ls()
        
        elif len(line)>2:

            name = line       

            def capitalize_name(name):
                return name[0].upper() + name[1:] if name else None

            def select_node(matched_nodes):
                
                header_statement = "Did you mean..."
                tail_statement = "(Press Enter to select none)"
                formatted_nodes = [node._convert_header_to_compact_format() for node in matched_nodes]
                SelectInterface(formatted_nodes, self, header_statement, tail_statement).cmdloop()
                response = self._get_response()
                return matched_nodes[int(response)-1] if response else None

            def create_node():
                user_input = input("| Do you want to create this node? [Y/N] : ").strip().lower()

                if user_input in ['Y','y']:

                    lang =  'es'
                    type =  input('> type  : ').strip()
                    lemma = 'NA'

                    return lang, type, lemma

                return None, None, None

            def bind_node(current_node, selected_node, edge_type):
                if selected_node and not selected_node in current_node.get_neighbors(edge_type):
                    self.parent_cli.G.bind(current_node, selected_node, edge_type)
                    print(f"| Successfully binded '{selected_node.name}'.")
                elif selected_node:
                    print('| The node was already present.')

            name = capitalize_name(name)

            matched_nodes = self.parent_cli.G.select(name=name)

            if matched_nodes:

                if len(matched_nodes) > 1:
                    selected_node = select_node(matched_nodes)
                else:
                    selected_node = matched_nodes[0]
            
            if not matched_nodes:

                selected_node = None

            if not selected_node:
                lang, type, lemma = create_node()
                if lang and type and len(lang) == 2 and len(type) == 1:
                    if not self.parent_cli.G.select(lang=lang, type=type, name=name, lemma=lemma):
                        self.parent_cli.G.create_node(lang, type, name, lemma)
                        selected_node = self.parent_cli.G.select(lang=lang, type=type, name=name, lemma=lemma)[0]
                        print("| Node created.")
                    else:
                        print('| The specified set of characteristics already exists.')
                elif lang or type or lemma:
                    print('Failed to validate hash attributes.')

            if selected_node:
                bind_node(self.ls_node, selected_node, self.parent_cli.placeholder.fields[0])
        
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)

    def do_mv(self, arg):

        args = arg.split()
        fields = [arg for arg in args if arg in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']]
        idxs = [arg for arg in args if set(arg).issubset(set('0123456789-')) and arg not in fields]
        name = ' '.join([arg for arg in args if arg not in idxs and arg not in fields])
        
        numbers_set = set()
        for part in idxs:
            numbers_set.update(range(int(part.split('-')[0]), int(part.split('-')[-1]) + 1)) if '-' in part else numbers_set.add(int(part))
        idxs = sorted(numbers_set)

        target_nodes = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes

        if name:
            homologous = self.parent_cli.G.select(name=name)
            if len(homologous) == 1:
                node = homologous[0]
            else:
                SelectInterface([node._convert_header_to_compact_format() for node in homologous], 
                            self, f"Found {len(homologous)} homologous.",
                            "(Select the node to operate)", '>> ').cmdloop()
                response = self._get_response()
                node = homologous[int(response)-1] if response.isdigit() else None
            if node:
                if not fields:
                    fields = self.parent_cli.placeholder.fields

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(node, target_node, field)
                        self.parent_cli.G.unbind(self.ls_node, target_node, self.parent_cli.placeholder.fields[0])
                print(f'Succesfully re-binded {len(target_nodes)} edges.')
            else:
                print('Aborted process.')
        else:
            node = self.ls_node
            if fields:
                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(node, target_node, field)
                        self.parent_cli.G.unbind(node, target_node, self.parent_cli.placeholder.fields[0])
                print(f'Succesfully re-binded {len(target_nodes)} edges.')
            else:
                print('Not enough arguments provided.')

        self.do_ls()
    
    def do_cp(self, arg):

        args = arg.split()
        fields = [arg for arg in args if arg in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']]
        idxs = [arg for arg in args if set(arg).issubset(set('0123456789-')) and arg not in fields]
        name = ' '.join([arg for arg in args if arg not in idxs and arg not in fields])
        
        numbers_set = set()
        for part in idxs:
            numbers_set.update(range(int(part.split('-')[0]), int(part.split('-')[-1]) + 1)) if '-' in part else numbers_set.add(int(part))
        idxs = sorted(numbers_set)

        target_nodes = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes

        if name:
            homologous = self.parent_cli.G.select(name=name)
            if len(homologous) == 1:
                node = homologous[0]
            else:
                SelectInterface([node._convert_header_to_compact_format() for node in homologous], 
                            self, f"Found {len(homologous)} homologous.",
                            "(Select the node to operate)", '>> ').cmdloop()
                response = self._get_response()
                node = homologous[int(response)-1] if response.isdigit() else None
            if node:
                if not fields:
                    fields = self.parent_cli.placeholder.fields

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(node, target_node, field)
                print(f'Succesfully binded {len(target_nodes)} edges.')

            else:
                print('Aborted process.')
        else:
            if fields:

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(self.ls_node, target_node, field)
                print(f'Succesfully binded {len(target_nodes)} edges.')
            else:
                print('Not enough arguments provided.')

        self.do_ls()
    
    def do_align(self, arg):
        args = arg.split()

        fields = [arg for arg in args if arg in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2','e','y']]
        if fields:
            fields = sk.parse_field(fields)
        else:
            fields = sk.parse_field()

        idxs = [arg for arg in args if set(arg).issubset(set('0123456789-')) and arg not in fields]
        
        numbers_set = set()
        for part in idxs:
            numbers_set.update(range(int(part.split('-')[0]), int(part.split('-')[-1]) + 1)) if '-' in part else numbers_set.add(int(part))
        idxs = sorted(numbers_set)

        # Determine whether to include the current placeholder node
        include_placeholder = '.' in args or len(idxs) == 1

        # Determine the target nodes based on the specified indices
        target_nodes = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes

        if include_placeholder:
            target_nodes.append(self.parent_cli.placeholder.node)

        # Initialize a dictionary to hold neighbors for each field
        d = {field: [] for field in fields}

        # Collect neighbors for each field from each target node
        for node in target_nodes:
            for field in fields:
                d[field].extend(node.get_neighbors(field))

        # Ensure all nodes in each field share the same bindings
        labels, contents = [], []
        for node in target_nodes:
            n_conn_o = len(node._get_raw_content())
            for field, neighbors in d.items():
                for neighbor in neighbors:
                    # Bind the target node to each neighbor in the current field
                    self.parent_cli.G.bind(node, neighbor, field)
            n_conn_f = len(node._get_raw_content())
            diff = n_conn_f-n_conn_o

            labels.append(node._convert_header_to_compact_format())
            contents.append(f"{n_conn_o} + {diff} conn. (+{round(100*diff/n_conn_o,2)}%)")

        formatted_lines = get_label_aligned_lines(labels, ' : ', contents)
        for line in formatted_lines:
            padded_print(line)

    def do_help(self, arg=None):
        """Provide help for a specified command or list all commands if none is specified."""
        if arg:
            # User asked for help on a specific command
            help_text = COMMAND_DOCSTRINGS_LS.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'")
        else:
            # User typed "help" without specifying a command
            padded_print("Available commands:")
            mini_prompt = ''
            right_padding = max([len(command) for command in COMMAND_DOCSTRINGS_LS]) + len(mini_prompt)
            for command in COMMAND_DOCSTRINGS_LS:
                # Only print the first line of each help text for an overview
                first_line = COMMAND_DOCSTRINGS_LS[command].strip().split('\n')[0]
                padded_print(f"{command+mini_prompt:<{right_padding}} : {first_line[8:]}")
        pass
    
    def emptyline(self): #finished
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def _get_response(self, reset_response=True):
        # Gets and decides wether it resets the response or not (by default, it does)
        res, self.response = self.response, None if reset_response else self.response
        return res

    def _update_listed_nodes(self):
        self.listed_nodes = list(self.ls_node.get_neighbors(self.parent_cli.placeholder.fields))
        # We update internal object self.listed_nodes to reflect changes that might have been made during the session
        self.listed_nodes = sorted(self.listed_nodes, key=lambda node: node.name)
        # We sort these nodes for readibility (by name)    

class GB_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, parent_cli):
        super().__init__()
        self.parent_cli = parent_cli
        print(f"(SYS: Started edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        self.display()
        self.cmdloop()

    def display(self, represent_bars=True):

        if len(self.parent_cli.tagged_nodes) == 0:
            print("No nodes tagged yet.")
        else:
            padded_print(f'Tagged {len(self.parent_cli.tagged_nodes)} nodes:')
            algorithm_output = centrality(self.parent_cli.tagged_nodes)[0]
            sorted_output = dict(sorted(algorithm_output.items(), key=lambda item: item[1], reverse=True))

            self.parent_cli.tagged_nodes = list(sorted_output.keys()) # to match indexes when accesed via 'rm'
            
            contents = ["{:.4f}".format(round(n,3)) for n in sorted_output.values()]
            formatted_nodes = [f"{i}) {node._convert_header_to_str_format()}"for i, node in enumerate(sorted_output.keys(), start=1)]          
            sep = ':'

            if represent_bars:
                contents = [f'{content} | {"█" * round(float(content) * 35)}' for content in contents]
            padded_print(get_label_aligned_lines(formatted_nodes, sep, contents), tab=1)

    def do_help(self, arg):
        if arg:
            help_text = COMMAND_DOCSTRINGS_GB.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'.")
        else:
            def get_description_from_docstring(docstring): return docstring.strip().split('\n')[0][8:]
            commands = COMMAND_DOCSTRINGS_GB.keys()
            contents = [get_description_from_docstring(COMMAND_DOCSTRINGS_GB[command]) for command in commands]
            formatted_lines = get_label_aligned_lines(commands, ':', contents)
            padded_print("Available commands:", formatted_lines, tab=0)

    def do_del(self, idxs):
        target_nodes = []
        idxs = sk.parse_idxs_to_single_idxs(idxs)
        for idx in idxs:
            if idx > 0:
                target_nodes.append(self.parent_cli.tagged_nodes[idx-1])
        for target_node in target_nodes:
            self.parent_cli.tagged_nodes.remove(target_node)
        print(f"Deleted {len(idxs)} nodes.")
    
    def do_clear(self, arg):
        self.parent_cli.tagged_nodes = []
        print(f"Cleared tagged nodes.")
    
    def do_tag(self, arg):
        self.parent_cli.do_tag(arg)

    def do_ls(self, arg):
        self.display()
    
    def emptyline(self):
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

    # def do_search_dense(self, arg):
    #     """
    #     Search for nodes densely connected to the tagged nodes.
    #     Usage: search_dense <n_coincidences> [field1,field2,...]
        
    #     Arguments:
    #     - n_coincidences: Minimum number of connections a node must have with the tagged nodes
    #     - fields: Optional. Comma-separated list of fields to consider for connections
        
    #     Example: search_dense 3 field1,field2
    #     """
    #     args = arg.split()
    #     if not args or len(args) > 2:
    #         print("Invalid arguments. Usage: search_dense <n_coincidences> [field1,field2,...]")
    #         return

    #     try:
    #         n_coincidences = int(args[0])
    #     except ValueError:
    #         print("n_coincidences must be an integer.")
    #         return

    #     fielding = args[1].split(',') if len(args) > 1 else []

    #     if not self.parent_cli.tagged_nodes:
    #         print("No nodes are currently tagged. Use 'tag' command first.")
    #         return

    #     # Perform density search
    #     dense_nodes = density_search(self.parent_cli.tagged_nodes, n_coincidences, *fielding)

    #     # Display results
    #     if dense_nodes:
    #         print(f"Found {len(dense_nodes)} densely connected nodes:")
    #         self._display_search_results(dense_nodes)
    #     else:
    #         print("No densely connected nodes found.")

    def do_expand(self, arg):
        """
        Perform a deterministic adaptive search to find relevant nodes based on tagged nodes.
        
        Usage: expand <target_results> <sample_size> <max_depth> [fields] [--complete_depth] [--only_new_centrality]
        """
        args = arg.split()

        default_target_results = int(len(self.parent_cli.tagged_nodes)*5)
        default_sample_size = len(self.parent_cli.tagged_nodes)
        default_max_depth = 4

        try:
            target_results = int(args[0]) if len(args) > 0 else default_target_results
            sample_size = int(args[1]) if len(args) > 1 else default_sample_size
            max_depth = int(args[2]) if len(args) > 2 else default_max_depth

            fields = []
            node_type = None
            complete_depth = False
            only_new_centrality = False

            i = 3
            while i < len(args):
                if args[i] in ['-t', '--type']:
                    if i + 1 < len(args):
                        node_type = args[i + 1]
                        i += 2
                    else:
                        print("Error: -t/--type flag requires a type value.")
                        return
                elif args[i] == '--complete_depth':
                    complete_depth = True
                    i += 1
                elif args[i] == '--only_new_centrality':
                    only_new_centrality = True
                    i += 1
                elif '--' not in args[i]:
                    fields = args[i].split(',')
                    i += 1
                else:
                    print(f"Unknown argument: {args[i]}")
                    return
        except ValueError:
            print("Invalid argument types. Please check your input.")
            return

        if not self.parent_cli.tagged_nodes:
            print("No nodes are currently tagged. Use 'tag' command first.")
            return

        # Asegurarse de que tagged_set solo contiene nodos válidos
        tagged_set = [node for node in self.parent_cli.tagged_nodes if node is not None and hasattr(node, 'get_neighbors')]
        if not tagged_set:
            print("No valid nodes in the tagged set.")
            return

        result_set = tagged_set.copy()
        new_additions = []
        search_report = []

        for depth in range(max_depth):
            print(f"Starting iteration at depth {depth + 1}")
            iteration_report = {
                'depth': depth + 1,
                'initial_size': len(result_set),
                'new_connections': 0,
                'added_nodes': 0
            }

            # Calculate centrality for the current result set
            try:
                centralities = centrality(result_set, *fields)[0]
                if not centralities:
                    print(f"No valid centrality scores at depth {depth + 1}. Stopping search.")
                    search_report.append(iteration_report)
                    break
            except Exception as e:
                print(f"Error calculating centrality: {str(e)}. Stopping search.")
                search_report.append(iteration_report)
                break

            # Select top sample_size central nodes
            top_nodes = sorted(centralities.items(), key=lambda x: x[1], reverse=True)[:sample_size]
            top_node_set = [node for node, _ in top_nodes if node is not None and hasattr(node, 'get_neighbors')]

            # Get all connections from top nodes
            extended_set = []
            for node in top_node_set:
                try:
                    neighbors = [n for n in node.get_neighbors(*fields) if n is not None and hasattr(n, 'get_neighbors')]
                    if node_type:
                        neighbors = [n for n in neighbors if hasattr(n, 'type') and n.type == node_type]
                    new_neighbors = [n for n in neighbors if n not in result_set and n not in extended_set]
                    extended_set.extend(new_neighbors)
                    iteration_report['new_connections'] += len(new_neighbors)
                except AttributeError:
                    print(f"Warning: Node {node} does not have get_neighbors method. Skipping.")

            if not extended_set:
                print(f"No new nodes found at depth {depth + 1}. Stopping search.")
                search_report.append(iteration_report)
                break

            # Calculate centrality for the extended set
            if only_new_centrality:
                centrality_set = extended_set
            else:
                centrality_set = result_set + extended_set
            
            try:
                new_centralities = centrality(centrality_set, *fields)[0]
                if not new_centralities:
                    print(f"No valid centrality scores for new nodes at depth {depth + 1}. Stopping search.")
                    search_report.append(iteration_report)
                    break
            except Exception as e:
                print(f"Error calculating centrality for new nodes: {str(e)}. Stopping search.")
                search_report.append(iteration_report)
                break

            # Sort new nodes by centrality score and add top nodes to results
            sorted_new_nodes = sorted(
                [(node, score) for node, score in new_centralities.items() if node in extended_set],
                key=lambda x: x[1],
                reverse=True
            )

            # Strictly adhere to sample_size for adding new nodes
            nodes_to_add = min(sample_size, len(sorted_new_nodes))
            added_nodes = 0
            for node, _ in sorted_new_nodes[:nodes_to_add]:
                if node not in result_set:  # Ensure we're not adding duplicates
                    result_set.append(node)
                    new_additions.append(node)
                    added_nodes += 1

            iteration_report['added_nodes'] = added_nodes
            search_report.append(iteration_report)

            if added_nodes == 0:
                print(f"No new nodes added at depth {depth + 1}. Stopping search.")
                break

            if len(result_set) >= target_results and not complete_depth:
                print(f"Reached target number of results. Stopping search.")
                break
        
        print("Search completed. Calculating final centralities...")

        try:
            final_centralities = centrality(result_set, *fields)[0]
            sorted_output = dict(sorted(final_centralities.items(), key=lambda item: item[1], reverse=True))
        except Exception as e:
            print(f"Error calculating final centralities: {str(e)}")
            sorted_output = {node: 0 for node in result_set}  # Fallback to 0 centrality if calculation fails

        print("\nDisplaying search report...")

        # Display search report
        print("\nSearch Report:")
        for report in search_report:
            print(f"Depth {report['depth']}:")
            print(f"  Initial set size: {report['initial_size']}")
            print(f"  New connections found: {report['new_connections']}")
            print(f"  Nodes added: {report['added_nodes']}")
        
        print(f"\n> Targets achievement: {len(sorted_output)}/{target_results} ({int(100*(len(sorted_output)/target_results))}%)\n")
        if len(sorted_output) < target_results:
            print(f"Note: Search stopped at depth {len(search_report)} without reaching the target number of results.")

        # Display results
        self._display_expand_results(sorted_output, new_additions)
    
    def _display_expand_results(self, sorted_results, new_additions):
        """
        Helper method to display adaptive search results in a formatted manner.
        
        Arguments:
        - sorted_results: Dictionary of {node: centrality_score}
        - new_additions: List of newly added nodes
        """
        max_id_length = max(len(str(i)) for i in range(1, len(sorted_results) + 1))
        max_node_length = max(len(self._safe_node_str(node)) for node in sorted_results)

        for i, (node, score) in enumerate(sorted_results.items(), 1):
            node_str = self._safe_node_str(node)
            id_str = str(i).rjust(max_id_length)
            
            bar_length = int(score * 35)  # Normalize bar length to 35 characters max
            bar = '█' * bar_length + '░' * (35 - bar_length)
            
            new_indicator = "[NEW]" if node in new_additions else "     "
            
            print(f"{id_str}) {new_indicator} {node_str:<{max_node_length}} | {score:.4f} {bar}")


    def _safe_node_str(self, node):
        """Safely convert a node to a string representation."""
        if node is None:
            return "None"
        if hasattr(node, '_convert_header_to_str_format'):
            try:
                return node._convert_header_to_str_format()
            except Exception:
                pass
        return str(node)
    
# POPUP CLIs ----------------------
    
    # These CLIs don't require HELP of any kind.
    
class SelectInterface(cmd.Cmd):

    def __init__(self, options, parent_cli, header_statement="", tail_statement="", prompt='>> '):
        super().__init__()
        self.options = options
        self.header_statement = header_statement
        self.tail_statement = tail_statement
        self.parent_cli = parent_cli
        self.prompt = prompt
        self.display()
    
    def display(self):
        padded_print(self.header_statement)
        for index, option in enumerate(self.options, start=1):
            string_index = str(index).zfill(2 if len(self.options)>10 else 1)
            padded_print(f"{string_index}) {option}", tab=1)
        padded_print(self.tail_statement)

    def deliver_result(self, response):
        self.parent_cli.response = None
        self.parent_cli.response = response

    def default(self, line):
        """
        The default method in a cmd.Cmd subclass is called when a command is entered
        that doesn't match any existing do_*
        """
        try:
            if isinstance(line, str) and not line.isdigit():
                self.deliver_result(line.strip())
            else:
                index = int(line) - 1  # Convert to zero-based index.
                if 0 <= index < len(self.options):
                    self.deliver_result(line)
                else:
                    print("Please enter a valid index.")
        except ValueError:
            print("Please enter a number to select an option or just press Enter to exit.")
        return True # exits loops
    
    def emptyline(self):
        # To exit with an empty Enter key press
        return True
    
    def do_exit(self, arg):
        return True 

    