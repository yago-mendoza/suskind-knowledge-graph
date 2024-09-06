import os
import random
import cmd
import colorama
from colorama import Fore, Back, Style
import datetime
import time
import re

class LiteratureExplorer(cmd.Cmd):
    prompt = Fore.CYAN + 'LitExplorer> ' + Style.RESET_ALL

    def __init__(self):
        super().__init__()
        self.root_dir = '.'
        self.folders = []
        self.selected_folders = []
        self.phrases = []
        self.current_phrase = None
        self.search_results = []
        self.current_search_index = 0
        self.last_search_query = ""
        self.lmin = None
        self.lmax = None
        self.in_search_mode = False
        self.folder_sizes = {}  # New attribute to store folder sizes in bytes
        self.total_size = 0
        self.show_bars = True

    def preloop(self):
        self.load_folders()
        self.calculate_folder_sizes()
        self.select_folders()
        self.load_phrases()
        self.clear_screen()

    def postcmd(self, stop, line):
        if not line.strip():
            return stop
        self.print_tips()
        return stop

    def print_tips(self):
        print(Style.DIM + "\nTips:")
        print(Style.DIM + "- Press Enter to repeat the last command or see next search result")
        print(Style.DIM + "- Type 'help' or '?' for a list of commands")
        print(Style.DIM + "- Use 'search' with AND, OR, NOT for advanced queries")
        if self.lmin:
            print(Style.DIM + f"- Current min length filter: {self.lmin} (type 'lmin' to unset)")
        if self.lmax:
            print(Style.DIM + f"- Current max length filter: {self.lmax} (type 'lmax' to unset)")

    def emptyline(self):
        if self.in_search_mode:
            self.display_next_search_result()
        elif self.lastcmd:
            return self.onecmd(self.lastcmd)

    def do_r(self, arg):
        """Display a random phrase"""
        self.in_search_mode = False
        self.get_random_phrase()

    def do_search(self, arg):
        """
        Search for phrases using advanced query.
        Usage: search <query>
        Operators: AND, OR, NOT (case sensitive)
        Examples:
            search tree AND red
            search cat OR dog
            search bird NOT flying
        """
        if not arg:
            print("Please provide a search query.")
            return
        self.last_search_query = arg
        self.search_phrases(arg)
        self.in_search_mode = True

    def do_d(self, arg):
        """Display partial context of the current phrase"""
        self.display_context(full=False)
        input(Style.DIM + "Press Enter to return to search results...")
        if self.in_search_mode:
            self.display_current_search_result()

    def do_dd(self, arg):
        """Display full file content of the current phrase"""
        self.display_context(full=True)
        input(Style.DIM + "Press Enter to return to search results...")
        if self.in_search_mode:
            self.display_current_search_result()

    def do_folder(self, arg):
        """Select folders to search in"""
        self.select_folders()
        self.load_phrases()

    def do_lmin(self, arg):
        """Set minimum length filter for phrases"""
        if arg:
            try:
                self.lmin = int(arg)
                print(f"Minimum length set to {self.lmin}")
            except ValueError:
                print("Please provide a valid integer for lmin")
        else:
            self.lmin = None
            print("Minimum length filter unset")

    def do_lmax(self, arg):
        """Set maximum length filter for phrases"""
        if arg:
            try:
                self.lmax = int(arg)
                print(f"Maximum length set to {self.lmax}")
            except ValueError:
                print("Please provide a valid integer for lmax")
        else:
            self.lmax = None
            print("Maximum length filter unset")

    def do_q(self, arg):
        """Quit the program"""
        print("Thank you for using Literature Explorer!")
        return True

    def do_help(self, arg):
        """List available commands with "help" or detailed help with "help cmd"."""
        cmd.Cmd.do_help(self, arg)

    def default(self, line):
        if line == '?':
            self.do_help('')
        else:
            print(f"Invalid command: {line}. Type '?' for help.")

    def load_folders(self):
        ignore_folders = ["__PDFs", "__pycache__", ".git", ".vscode"]
        self.folders = self.get_nested_folders(self.root_dir, ignore_folders)
        self.selected_folders = [folder for folder, _ in self.folders]

    def get_nested_folders(self, path, ignore_folders, level=0):
        folders = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and item not in ignore_folders:
                relative_path = os.path.relpath(item_path, self.root_dir).replace(os.sep, '/')
                folders.append((relative_path, level))
                folders.extend(self.get_nested_folders(item_path, ignore_folders, level + 1))
        return folders

    def calculate_folder_sizes(self):
        self.folder_sizes = {}
        self.folder_file_counts = {}
        self.total_size = 0
        
        for folder, _ in self.folders:
            folder_path = os.path.join(self.root_dir, folder)
            folder_size = 0
            for root, _, files in os.walk(folder_path):
                txt_files = [f for f in files if f.endswith('.txt')] #
                self.folder_file_counts[folder] = len(txt_files) #
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        try:
                            folder_size += os.path.getsize(file_path)
                        except Exception as e:
                            print(f"Error reading file {file_path}: {str(e)}")
            
            self.folder_sizes[folder] = folder_size
            self.total_size += folder_size
    
    def folder_contains_only_txt_files(self, folder):
        folder_path = os.path.join(self.root_dir, folder)
        return all(f.endswith('.txt') for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))

    def folder_contains_only_subfolders(self, folder):
        folder_path = os.path.join(self.root_dir, folder)
        return all(os.path.isdir(os.path.join(folder_path, f)) for f in os.listdir(folder_path))
    
    def calculate_selected_percentage(self):
        selected_size = sum(self.folder_sizes[folder] for folder in self.selected_folders)
        total_size = sum(self.folder_sizes.values())
        return (selected_size / total_size) * 100 if total_size > 0 else 0
    
    def select_folders(self):
        while True:
            self.clear_screen()
            self.print_header("Folder Selection")
            max_name_length = max(len(os.path.basename(folder)) for folder, _ in self.folders)
            bar_length = 20
            
            # Find the maximum folder size
            max_folder_size = max(self.folder_sizes.values())
            
            for i, (folder, level) in enumerate(self.folders, 1):
                status = '[X]' if folder in self.selected_folders else '[ ]'
                indent = '    ' * level
                folder_name = os.path.basename(folder)
                
                # Calculate relative percentage
                relative_percentage = (self.folder_sizes[folder] / max_folder_size) if max_folder_size > 0 else 0
                
                if self.show_bars:
                    filled_length = int(relative_percentage * bar_length)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length) + '░'
                    percentage_str = f'{relative_percentage:7.2%}'  # Changed to 7.2% for consistent width

                    if self.folder_contains_only_subfolders(folder):
                        folder_name = f'<{folder_name.upper()}>'
                    elif self.folder_contains_only_txt_files(folder):
                        folder_name = f"{folder_name} (*{self.folder_file_counts[folder]})"

                    print(f"{percentage_str} {bar} {i:2d} - {status} {indent}{folder_name}")
                else:
                    if self.folder_contains_only_subfolders(folder):
                        folder_name = f'<{folder_name.upper()}>'
                    elif self.folder_contains_only_txt_files(folder):
                        folder_name = f"{folder_name} (*{self.folder_file_counts[folder]})"

                    print(f"{i:2d} - {status} {indent}{folder_name}")
            
            print(Style.DIM + "\nEnter folder numbers to toggle selection, 'all' to select all, 'none' to deselect all,")
            print(Style.DIM + "'bar' to toggle bar display, or press Enter to finish.")
            
            selected_percentage = self.calculate_selected_percentage()
            choice = input(f"Choice [{selected_percentage:.2f}% selected]: ").strip().lower()
            
            if choice == '':
                break
            elif choice == 'all':
                self.selected_folders = [folder for folder, _ in self.folders]
            elif choice == 'none':
                self.selected_folders = []
            elif choice == 'bar':
                self.show_bars = not self.show_bars
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.folders):
                    self.toggle_folder_selection(index)
            else:
                self.print_error("Invalid input. Please try again.")

    def toggle_folder_selection(self, index):
        folder, _ = self.folders[index]
        if folder in self.selected_folders:
            self.deselect_folder_and_subfolders(folder, index)
        else:
            self.select_folder_and_subfolders(folder, index)

    def select_folder_and_subfolders(self, folder, index):
        if folder not in self.selected_folders:
            self.selected_folders.append(folder)
        for i in range(index + 1, len(self.folders)):
            subfolder, sublevel = self.folders[i]
            if sublevel <= self.folders[index][1]:
                break
            if subfolder not in self.selected_folders:
                self.selected_folders.append(subfolder)

    def deselect_folder_and_subfolders(self, folder, index):
        if folder in self.selected_folders:
            self.selected_folders.remove(folder)
        for i in range(index + 1, len(self.folders)):
            subfolder, sublevel = self.folders[i]
            if sublevel <= self.folders[index][1]:
                break
            if subfolder in self.selected_folders:
                self.selected_folders.remove(subfolder)

    def load_phrases(self):
        self.phrases = []
        total_files = sum(len([f for f in os.listdir(os.path.join(self.root_dir, folder)) if f.endswith('.txt')]) for folder in self.selected_folders)
        processed_files = 0

        for folder in self.selected_folders:
            folder_path = os.path.join(self.root_dir, folder)
            for file in os.listdir(folder_path):
                if file.endswith('.txt'):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            sentences = [s.strip() for s in content.replace('\n', '.').split('.') if s.strip()]
                            self.phrases.extend([(folder.replace(os.sep, '/'), file, i, s) for i, s in enumerate(sentences)])
                    except Exception as e:
                        self.print_error(f"Error reading file {file_path}: {str(e)}")
                    
                    processed_files += 1
                    self.show_progress(processed_files, total_files)

        print("\nLoading complete!")
        time.sleep(1)
        self.clear_screen()

    def show_progress(self, current, total):
        percent = int(current * 100 / total)
        bar = '=' * percent + '-' * (100 - percent)
        print(f'\rProgress: [{bar}] {percent}%', end='')

    def get_random_phrase(self):
        if self.phrases:
            filtered_phrases = self.filter_phrases(self.phrases)
            if filtered_phrases:
                self.current_phrase = random.choice(filtered_phrases)
                self.display_phrase(self.current_phrase)
            else:
                self.print_error("No phrases available with current length filters.")
        else:
            self.print_error("No phrases available. Please check your folder selection.")

    def search_phrases(self, query):
        tokens = self.tokenize_query(query)
        all_results = self.evaluate_query(tokens)
        self.search_results = self.filter_phrases(all_results)
        random.shuffle(self.search_results)
        self.current_search_index = 0
        if self.search_results:
            self.display_current_search_result()
        else:
            self.print_error(f"No results found for '{query}' with current length filters.")

    def tokenize_query(self, query):
        return re.findall(r'\S+|\s+', query)

    def evaluate_query(self, tokens):
        stack = []
        current_set = set()
        operation = 'OR'

        for token in tokens:
            if token.upper() in ('AND', 'OR', 'NOT'):
                operation = token.upper()
            elif token.strip():
                phrase_set = set(phrase for phrase in self.phrases if token.lower() in phrase[3].lower())
                if operation == 'AND':
                    current_set = current_set & phrase_set if current_set else phrase_set
                elif operation == 'OR':
                    current_set |= phrase_set
                elif operation == 'NOT':
                    current_set -= phrase_set

        return list(current_set)

    def filter_phrases(self, phrases):
        return [phrase for phrase in phrases if self.phrase_matches_length_filters(phrase[3])]

    def phrase_matches_length_filters(self, phrase):
        if self.lmin and len(phrase) < self.lmin:
            return False
        if self.lmax and len(phrase) > self.lmax:
            return False
        return True

    def display_next_search_result(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.display_current_search_result()

    def display_current_search_result(self):
        if self.search_results:
            self.current_phrase = self.search_results[self.current_search_index]
            total_results = len(self.search_results)
            self.display_phrase(self.current_phrase, f"Result {self.current_search_index + 1}/{total_results}", highlight=self.last_search_query)

    def display_phrase(self, phrase, header_extra="", highlight=""):
        folder, file, index, text = phrase
        text += '.'
        self.clear_screen()
        self.print_header(f"Phrase Display {header_extra}")
        print(Fore.BLUE + f"Location: {folder}/{file}")
        print(Fore.BLUE + f"Index: {index}")
        print(Fore.BLUE + f"Length: {len(text)}")
        if highlight:
            highlighted_text = self.highlight_text(text, highlight)
            print(Style.RESET_ALL + highlighted_text)
        else:
            print(Style.RESET_ALL + text)

    def highlight_text(self, text, query):
        tokens = self.tokenize_query(query)
        words_to_highlight = [token for token in tokens if token.upper() not in ('AND', 'OR', 'NOT')]
        for word in words_to_highlight:
            text = re.sub(f'({re.escape(word)})', Fore.RED + r'\1' + Style.RESET_ALL, text, flags=re.IGNORECASE)
        return text

    def display_context(self, full=False):
        if self.current_phrase:
            folder, file, index, _ = self.current_phrase
            file_path = os.path.join(self.root_dir, folder, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    sentences = [s.strip() + '.' for s in content.replace('\n', '.').split('.') if s.strip()]
                    
                    if full:
                        context = sentences
                        context_type = "Full File Content"
                    else:
                        start = max(0, index - 2)
                        end = min(len(sentences), index + 3)
                        context = sentences[start:end]
                        context_type = "Partial Context"

                    self.clear_screen()
                    self.print_header(f"{context_type} Display")
                    print(Fore.BLUE + f"Location: {folder}/{file}")
                    print(Fore.BLUE + f"Index: {index}")
                    print(Style.RESET_ALL)

                    for i, sentence in enumerate(context):
                        if (not full and i + start == index) or (full and i == index):
                            highlighted_sentence = Fore.YELLOW + sentence + Style.RESET_ALL
                            if self.last_search_query:
                                highlighted_sentence = self.highlight_text(highlighted_sentence, self.last_search_query)
                            print(highlighted_sentence)
                        else:
                            print(sentence)
            except Exception as e:
                self.print_error(f"Error reading file {file_path}: {str(e)}")
        else:
            self.print_error("No current phrase selected.")

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title):
        print(Fore.GREEN + Style.BRIGHT + "=" * 50)
        print(Fore.GREEN + Style.BRIGHT + f"  {title}")
        print(Fore.GREEN + Style.BRIGHT + f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.GREEN + Style.BRIGHT + "=" * 50)
        print(Style.RESET_ALL)

    @staticmethod
    def print_error(message):
        print(Fore.RED + Style.BRIGHT + "Error: " + message + Style.RESET_ALL)