import cmd
import datetime
from skcomponents import *
from rich import print

# self.prompt
# self.intro
# complete_xxx
# do_help para documentar cada comando
# prompt_suffix

'''
ABOUT FILTERS

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter -e
| Entered editor mode on filters:
| f1/type('w').lang('es')
| f2/starts('clar')
>> rm f1
>> contains('esonate').lang('en') > f1   # (> f1 is optional)
>> ''
14:32:09 ~ [es][n][concept]@[(lemma)]/: filter
| Showing defined filters:
| f1/starts('clar')
| f2/contains('esonate').lang('en')
14:32:11 ~ [es][n][concept]@[(lemma)]/: r -favorite
14:32:11 ~ [en][n][Dinero]@[('')]/: r -f2     # random but applying the filter
14:32:15 ~ [en][v][Resonate]@[('')]/: ls -f1    # watches but applying the filter
14:32:18 ~ [en][v][Resonate]@[('')]/:
14:32:18 ~ [en][v][Resonate]@[('')]/: filter -rm
14:32:18 ~ [en][v][Resonate]@[('')]/: filter
14:32:18 ~ [en][v][Resonate]@[('')]/: filter -e
>> ''
14:32:18 ~ [en][v][Resonate]@[('')]/: filter
14:32:18 ~ [en][v][Resonate]@[('')]/: r
14:32:18 ~ [es][n][Alabastro]@[('')]/: cd normal
| Did you mean ...
| a) [en][j][Normal]@[('')]
| b) [es][j][Normal]@[('')]
>> a
14:32:18 ~ [en][j][Normal]@[('')]/: summary
| Showing quick summary for <node> connections:
| synset0 : 14   | semset0 : 61
| synset1 : 515  | semset1 : 551
| synset2 : 14   | semset2 : 65
14:32:18 ~ [en][j][Normal]@[('')]/: .sort -on   ######
14:32:18 ~ [en][j][Normal]@[('')]/: .rand -on   ######
14:32:18 ~ [en][j][Normal]@[('')]/: ls
| Error. Search field is needed.
14:32:18 ~ [en][j][Normal]@[('')]/: set e
14:32:18 ~ [en][j][Normal]@[('')]/[e0/e1/e2]: unset
14:32:18 ~ [en][j][Normal]@[('')]/: set y
14:32:18 ~ [en][j][Normal]@[('')]/[y0/y1/y2]: unset y0 y2
14:32:18 ~ [en][j][Normal]@[('')]/[y1]:
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: .ncol 2   ######
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls -slit 8
| Showing 8/1240 results:
| 1. Arma biológica                       | 5. Hermandad
| 2. Tortuga marina                       | 6. Cabellera
| 3. Cárcel de muerte lenta e inevitable  | 7. Simplón
| 4. Tiburones                            | 8. Carretera asfaltada
>> ''
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: .abbr 20   ######
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls -slit 8 -f2 ######
| Showing 8/1240 results:
| 1. Arma biológica          | 5. Hermandad
| 2. Tortuga marina          | 6. Cabellera
| 3. Cárcel de muerte le...  | 7. Simplón
| 4. Tiburones               | 8. Carretera asfaltada
>> ''
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: .cut -off .rand -off
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls status
| Showing 'ls' set parameters:
| .rand -off  (randomization)
| .sort -off  (sorting)
| .slit -off  (sliting output)
| .ncol 2     (nº of columns)
| .abbr -off  (abbreviating results)
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls
| Showing 8/1240 results:
| 1. Arma biológica          | 5. Hermandad
| 2. Tortuga marina          | 6. Cabellera
| 3. Cárcel de muerte le...  | 7. Simplón
| 4. Tiburones               | 8. Carretera asfaltada
>> del 8 7 6
>> refresh
| 1. Arma biológica          | 4. Tiburones
| 2. Tortuga marina          | 5. Hermandad
| 3. Cárcel de muerte le...
>> add Perro de caza
>> add asdf
| Error. Node 'asdf' was not found, hence, not included.
>> add Bat
| Did you mean ...
| a) [en][n][Bat]@[('mammal')]
| b) [en][n][Bat]@[('tool')]
>> a
>> ''
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls
| Showing 8/1240 results:
| 1. Arma biológica          | 5. Hermandad
| 2. Tortuga marina          | 6. Perro de caza
| 3. Cárcel de muerte le...  | 7. Bat
| 4. Tiburones
>> ''
14:32:18 ~ [en][j][Normal]@[('')]/[y1]: set y
14:32:18 ~ [en][j][Normal]@[('')]/[y0/y1/y2]: cd QWERTY
14:32:18 ~ [en][j][~QWERTY]@[('')]/[[y0/y1/y2]: ls
| Warning. Editing commands disabled due to multiple fielding.
| Warning. No connections were yet added.
>> add Gato
| Error. In order to modify attributes, select a single field.
>> ''
14:32:18 ~ [en][j][~QWERTY]@[('')]/[[y0/y1/y2]: r
14:32:18 ~ [es][v][Andar]@[('')]/[[y0/y1/y2]: ls
| Showing 7/77 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Piedras blancas
| 4. Electrocutar
>> cd 6
14:32:18 ~ <..2>[es][v][Cercenar]@[('')]/[[y0/y1/y2]: ls
| Showing 7/77 results:
| 1. Blanco               | 5. Melón
| 2. Error                | 6. Cantarín
| 3. Atrapar antes po...  | 7. Elegía
| 4. Pifiarla
>> cd 7
14:32:18 ~ <..3>[es][n][Elegía]@[('')]/[[y0/y1/y2]: ls
| Showing 7/35 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Vulgar
| 4. Electrocutar
>> ''
...
14:32:18 ~ <..55>[es][n][Esperanza]@[('')]/[[y0/y1/y2]: goto 33
14:32:18 ~ <33..>[es][n][Canción]@[('')]/[[y0/y1/y2]: goto -1
14:32:18 ~ <55..>[es][n][Esperanza]@[('')]/[[y0/y1/y2]: goto 14
14:32:18 ~ <14..>[es][n][Párbulos]@[('')]/[[y0/y1/y2]: nhist
| Showing nesting history:
| <0> [es][v][Andar]@[('')] -> [es][v][Cercenar]@[('')]
| <1> [es][v][Cercenar]@[('')] -> [es][n][Elegía]@[('')]
...
| <55> [es][n][Humo]@[('')] -> [es][n][Cigarrillo electrónico]@[('')]
14:32:18 ~ <14..>[es][n][Párbulos]@[('')]/[[y0/y1/y2]: cd Perro
| Warning: this action will delete the nested search history. Are you sure? [Y/N]
>> Y


>> Are you sure you want to go back to [es][v][Cercenar]@[('')]?
The nesting history will be lost and you will work tree clean [Y/N]

14:32:18 ~ [es][n][Humo]@[('')]/[[y0/y1/y2]: ls
<103> Showing 7/84 results:
||||| 1. Caminador            ||||| 5. Golfo
||||| 2. Persona              ||||| 6. Cercenar
||||| 3. Atrapar antes po...  ||||| 7. Vulgar
||||| 4. Electrocutar
>> cd ..
14:32:18 ~ [es][n][Cigarrillo electrónico]@[('')]/[[y0/y1/y2]: ''
14:32:18 ~ [es][n][Cigarrillo electrónico]@[('')]/[[y0/y1/y2]: ls
<102> Showing 7/84 results:
||||| 1. Caminador            ||||| 5. Golfo
||||| 2. Persona              ||||| 6. Cercenar
||||| 3. Atrapar antes po...  ||||| 7. Vulgar
||||| 4. Electrocutar
>> hist
| Showing nesting history:
| <0> [es][v][Andar]@[('')] -> [es][v][Cercenar]@[('')]
| <1> [es][v][Cercenar]@[('')] -> [es][n][Elegía]@[('')]
...
| <102> [es][n][Humo]@[('')] -> [es][n][Cigarrillo electrónico]@[('')]
>> goto 28
14:32:18 ~ [es][v][Carraspear]@[('')]/[[y0/y1/y2]: ls
<27> Showing 7/77 results:
|||| 1. Blanco               |||| 5. Melón
|||| 2. Error                |||| 6. Cantarín
|||| 3. Atrapar antes po...  |||| 7. Elegía
|||| 4. Pifiarla
>> ''



>> Y



add-node

delete-node
add-relation
edit-relation
delete-relation

hist : prints out a history of relevant changes during session
status : prints relevant parameters and their current configuration
? : prints what can be done at this current screen
help _ : prints out the explanation for the given command

cd : if only 1 lemma, enter directly. If more than 1 lemma, print out list with numbers.
cd : also to add a new Node
remove : removes the node from the system

set-ncol _ : sets the number of columns
ls : see e_/y_ for the current node
del _ _ _ : deletes this connections
send 19 semset2 / send 19 e2 / 19 e2 / 19 2




# ver varios a la vez



# batching
# fast editing


e / y

del
<
>
ls
clear
r = random node
.ncol

update-attr
transfer-attr
copy
paste

ADVANCED COMMANDS
extract / export
min

MKDIR COMMANDS
commit
push
autosave 

'''



class Placeholder:
    def __init__(self, primary_interface):
        self.primary_interface = primary_interface
    def update(self):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        field = self.primary_interface.current_field
        name = self.primary_interface.current_node
        # 10:46:32 ~ (F/es/-w)[concept]@[(lemma)]/:
        return f"{time_str} ~ (F/w)[{field}]@[{name or ''}(lemma)]/: "

class PrimaryInterface (cmd.Cmd):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.current_node = None
        self.current_field = 'concept'
        self.placeholder = Placeholder(self)
        self.update_prompt()
        self.lang = ['es']
        self.type = ['n']
    
    def update_prompt(self):
        # Default method & attribute for cmd.Cmd
        self.prompt = self.placeholder.update()

    def do_set(self, property):
        if property in self.database.list_langs():
            self.lang.append(property)
        elif property in self.database.list_types():
            self.lang.append(property)

    def do_cd(self, concept_name):
        concept = self.database.find(self.lang, self.type, concept_name, '')
        if concept:
            self.current_node = concept_name
            self.current_field = 'concept'
            self.update_prompt()
        else:
            print(f"No se encontró el concepto: {concept_name}")

    def do_exit(self, arg):
        print("Saliendo...")
        return True

if __name__ == "__main__":
    G = Graph('data.txt')
    cli = PrimaryInterface(G)
    cli.cmdloop()