import os
import cmd # Importing Python's built-in library for creating command-line interfaces (used for PrimaryInterface and upcoming sub-CLIs)
import argparse

from src.skcli.skplaceholder import *
from src.skcli.aux_clis import *

from src.skcli.aux_funcs.err_mssg import *
from src.skcli.aux_funcs.visuals import *
from src.skcli.aux_funcs.command_docstrings import *

"""
###############################
###########################
#######################
###################
###############
###########
DISCLAIMER
1. No metas más funcionalidades hasta que la actual versión no esté 
PERFECTAMENTE documentada.
2. Si metes funcionalidades próximamente, que sean VITALES para el
funcionamiento del programa. No metas funcionalidades superfluas de momento.
El objetivo es tenerlo ready para Bélgica.
3. Próximamente, si creas un <COMANDO> nuevo, completa su DOCSTRING de forma
ordenada. Y documenta todo su código con in-line comments apropiados.
###########
###############
###################
#######################
###########################
###############################

# 1. Add additional flags at 'r' --------------------------------------------

r -t (sin complementos terminados) causes a fatal error (should not) ni tampoco nadie a quien le falten argumentos debería
r --summary (que active el summary cada vez que se ejecute)
r --ls (que active el ls cada vez que se ejecute)
r -f (not working as expected)

do_new (creates a new node being able to set new language (-l) or lemma (-l), because if already existing, cannot create unless a lemma is set)
do_save (save the graph to a file)

# 2. Add local flags for 'ls' and global flags for 'ls' ---------------------------

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

and 'status' shows this variables
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls --status
| Showing 'ls' set parameters:
| .rand -off  (randomization)
| .sort -off  (sorting)
| .slit -off  (sliting output)
| .ncol 2     (nº of columns)
| .abbr -off  (abbreviating results)

# 3. Add a subCLI for 'ls' -------------------------------------

>> del 8 7 6  # borrar entradas
>> del 8 7 6 -r  # refreshes (shows)
>> refresh  # refreshes (shows)
>> add Alto, Normal (te refieres a...?) # tiene que existir
| Error. Node 'asdf' was not found, hence, not included.
a random suggestor
ls with multiple fields : makes mandatory write '> y0' for interactive subCLI
ls -> warning if 'no connections yet'
Showing X/X for 'ls'
'r' habilitated within the 'ls' subCLI
4 6 1 7 > y0

# 4. Editing node properties ------------------------------------

name -e
>> Banco # y aquí editamos
    >> Banco
    | Warning. There's already 2 entries called 'Banco'. Select one to merge.
    |  1. [es][n][Banco]@[('institución')]
    |  2. [es][n][Banco]@[('mobiliario')]
    |  3. <new_lemma>

lemma -e
| Other lemmas for this entry are ...
|  1. Institución
|  2. Mobiliario
|  <new_lemma>
>> Grupo
-e or lang -e or type -e

# 5. Deleting a node ---------------------------------------------

14:32:18 ~ [en][j][Banco]@[('Grupo')]/[y0/y1/y2]: rm
| Warning. Are you sure you want to remove this node (1159 edges)? [Y/N]
>> Y

# 6. Filters -----------------------

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter -e
| Entered editor mode on filters:
| f1/type('w').lang('es')
| f2/starts('clar')
>> rm f1
>> add contains('esonate').lang('en')
>> ''
14:32:04 ~ [es][n][concept]@[(lemma)]/:

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
| Showing filters:
| f1/lang('es').contains('trent')
| f2/starts('clar')
14:32:04 ~ [es][n][concept]@[(lemma)]/:

14:32:04 ~ [es][n][concept]@[(lemma)]/: set f1
14:32:04 ~ [es][n][concept]@[(lemma)]/: unset ls f1
14:32:04 ~ [es][n][concept]@[(lemma)]/: set ls f2
14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
| Showing filters:
| [ls, cd, r] f1/lang('es')
| [ls] f2/lang('en')
14:32:04 ~ [es][n][concept]@[(lemma)]/: filter ls
| Showing filters:
| f1/lang('es')
| [>] f2/lang('en')
14:32:04 ~ [es][n][concept]@[(lemma)]/: unset f1
14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
| Showing filters:
| f1/lang('es')
| [ls] f2/lang('en')

# 7. TERMINAL ---------------------------------------

14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]: term
Python. Granted a pathway to SKComponents objects and methods.
Type "Node" or "Graph" to inspect objects and "exit" to leave.
>>> Node.compress.expand('synset').compress('synset2')
>>> G.view_names()
>>> n = G.random()
>>> G.disable('semset')    # implementar que podamos ahorrarnos comillas
>>> ndst = G.filter_
Exiting terminal...
14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]:

# 8. NESTED_HISTORY ------------------------------------

| Showing nested history:
| root: [0] Andar(/7)
|       └── [1] Cercenar (<6th> of 7)
|            ├── [2] Elegía (<7th> of 7)
|            └── [3] Esperanza (<42th> of 102)
cd ..
| Warning: this action will delete the nested search history. Are you sure? [Y/N]

#################################################################################

# 98. Undo and Go back to previous node
via 'undo' and 'cd ..'

# 99. Autocomplete via 'tab' key
prompt_toolkit for autocomplete

¿Useful symbols?
    <, >
    clear, copy, paste
    extract / export, min
    commit, push, autosave 
¿Very future steps?
    min_path
    reduce a set
    search method
    decide where to use 'rich' colors
    I dont need a hist of every single action done. So hist will be just for visited nodes.
    status (already set, to do)
    suggestions
    and changing words from category within a same node
    traduccion con filter, no con funcion explicita
    (same for merging synset1's, just a way to merge nodes and them also)


"""

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
            elif setting in self.G.set_types():
                # If a type is specified, update the type in the placeholder and set a random node of that type.
                type_ = setting
                self.placeholder.type = type_
                self._set_random_node(type=type_)
            elif setting in self.G.set_langs():
                # new language being inputed
                # If a language is specified, update the language in the placeholder and set a random node of that language.
                lang = setting
                self.placeholder.lang = lang
                self._set_random_node(lang=lang)
            # Check if the argument matches any known type in the graph.
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
        nodes = self.G.find(lang=self.placeholder.lang,
                            type=self.placeholder.type,
                            name=parsed_name)

        # Implements fallback logic: If the initial search yields no results, progressively broadens the search criteria.
        if not nodes:
            nodes = self.G.find(lang=self.placeholder.lang,
                                name=parsed_name)
        if not nodes:
            nodes = self.G.find(type=self.placeholder.type,
                                name=parsed_name)
        if not nodes:
            nodes = self.G.find(name=parsed_name)

        # Processes the search results based on the number of nodes found.
        if len(nodes) == 1:
            # If exactly one matching node is found, it's automatically set as the current context.
            self._set_node(nodes[0])
        elif nodes:
            # If multiple matching nodes are found, indicates a future feature for user selection.
            SelectNodeInterface(nodes, self).cmdloop()
        else:
            # If no matching nodes are found, informs the user accordingly.
            candidates = self.G
            number_of_guesses = 3
            top_guessed_nodeset = candidates.scan_for_similar_nodes(name=parsed_name, k=number_of_guesses)
            SelectNodeInterface(top_guessed_nodeset, self).cmdloop()

    def do_r(self, args):
        # Creates a new argument parser to interpret the command line inputs.
        parser = argparse.ArgumentParser(description="Perform a random node search")
        # Adds optional arguments to specify the language and type, enhancing the command's flexibility.
        parser.add_argument('-l', '--lang', type=str, help='Specify the language')
        parser.add_argument('-t', '--type', type=str, help='Specify the type')
        parser.add_argument('-f', '--fav', action='store_true', help='Toggle favorite switch')  # Notice the action change.
        
        # Parses the arguments from the command line input.
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

        # Initialize the argument parser
        parser = argparse.ArgumentParser(description='List information about the current node.')
        parser.add_argument('-d', '--details', action='store_true', help='Show detailed information about each item.')

        args = parser.parse_args(arg.split())

        if self.placeholder.fields:

            self._update_graph_permissions_to_fields() # we set graph permissions to fields (for neighbors)
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

        parser = argparse.ArgumentParser(description='Creates a new node.')
        parser.add_argument('-l', '--diff', type=str, help='Specify the language or lemma of the node, if needed.')
        
        args = parser.parse_args(arg.split())

        # lang, lemma = None, None

        # if args.diff:
        #     if len(args.diff)==2 and args.diff.islower():
        #         lang = args.diff
        #     else:
        #         lemma = args.diff

        # lang  = lang if lang else self.placeholder.lang
        # type_ = self.placeholder.type
        # name  = args.name
        # lemma = lemma if lemma else ''

        # akin_nodes = self.G.find(lang=lang, type=type_, name=name, lemma=lemma)

        # if not akin_nodes:
        #     self.G.create_node(lang, type_, name, lemma)
        # else:
        #     print('This node already exists at this scope.')
        #     for node in akin_nodes:
        #         print(f'| {node}')
        #     print('Tip: try using a different lemma.')

    # Internal Methods  --------------------
            
    def _set_node(self, new_node):
        if new_node:
            self.placeholder.update_node(new_node)

    def _set_random_node(self, **kwargs):
        new_node = self.G.random(**kwargs)
        if new_node:
            self._set_node(new_node)
        else:
            padded_print('No nodes met the criteria.')

    def _update_graph_permissions_to_fields(self):
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
        
    def do_clear(self, arg):
        self.preloop()
        
    def preloop(self):
        os.system('cls')
        self._print_markdown_title()
        padded_print(HELP_DISCLAIMER, CONTEXTUAL_DISCLAIMER)
        print('-'*47)

    def default(self, line):
        padded_print(f"Unknown '{line[:2].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)

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
    


