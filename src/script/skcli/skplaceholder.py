import datetime # Importing the datetime module to work with dates and times (used at 'get_string()' for PlaceHolder)

# The Placeholder class is designed to represent and manage the current state (or "Node") of the command prompt.
class Placeholder():
    def __init__(self, cmd):
        self.cmd = cmd  # Holds a reference to the command module, allowing updates to the cmd.prompt with the generated string from this class.
        # Initialize default properties for the node, representing its language, type, name, and lemma.
        self.lang, self.type, self.name, self.lemma = 'lang', 'type', 'name', 'lemma'
        self.fields = ['y1']  # A list of additional fields that influence the outcome of commands like "ls".

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
        return f"{str_time} ~ {self.node._convert_header_to_compact_format()}/{fields_list or ''}\n: "
