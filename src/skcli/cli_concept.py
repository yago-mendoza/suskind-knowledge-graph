
'''
TERMINAL CONCEPT

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter -e
| Entered editor mode on filters:
| f1/type('w').lang('es')
| f2/starts('clar')

>> rm f1                                            # rm all
>> Y                                                Warning: do you want ro remove f1 filter? [Y/N]
>> contains('esonate').lang('en') > f1              # (> f1 is optional)
>> ''
14:32:09 ~ [es][n][concept]@[(lemma)]/: filter
| Showing defined filters:
| f1/starts('clar')
| f2/contains('esonate').lang('en')
14:32:11 ~ [es][n][concept]@[(lemma)]/: r -favorite  # busqueda random por filtro favorito
14:32:11 ~ [en][n][Dinero]@[('')]/: r -f2            # random but applying the filter
14:32:15 ~ [en][v][Resonate]@[('')]/: ls -f1         # watches but applying the filter
14:32:15 ~ [en][v][Resonate]@[('')]/: set f1
14:32:04 ~ [es][n][Resonate]@[('')]/: filter
| Entered editor mode on filters:
| [>] f1/type('w').lang('es')                        # ahora está puesto este por defecto, y si no se aplica un arg, se usará
| f2/starts('clar')
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
14:32:18 ~ [en][j][~QWERTY]@[('')]/[y0/y1/y2]: ls
| Warning. Editing commands disabled due to multiple fielding.
| Warning. No connections were yet added.
>> add Gato
| Error. In order to modify attributes, select a single field.
>> ''
14:32:18 ~ [en][j][~QWERTY]@[('')]/[y0/y1/y2]: set es n     # preparing the entry
14:32:18 ~ [es][n][~QWERTY]@[('')]/[y0/y1/y2]: set y1
14:32:18 ~ [en][j][~QWERTY]@[('')]/[y1]: ls
| Warning. No connections were yet added.
>> add Perro
>> ''
14:32:18 ~ [en][j][QWERTY]@[('')]/[y0/y1/y2]: r
14:32:18 ~ [es][v][Andar]@[('')]/[y0/y1/y2]: ls
| Showing 7/77 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Piedras blancas
| 4. Electrocutar
>> cd 6
14:32:18 ~ [es][v][Cercenar]@[('')]/[y0/y1/y2]: ls
| Showing 7/77 results:
| 1. Blanco               | 5. Melón
| 2. Error                | 6. Cantarín
| 3. Atrapar antes po...  | 7. Elegía
| 4. Pifiarla
>> r
14:32:18 ~ [es][n][Elegía]@[('')]/[y0/y1/y2]: ls
| Showing 7/35 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Vulgar
| 4. Electrocutar         | 8. Rata
| ...                     | ...
>> r

14:32:18 ~ <54..>[es][n][Canción]@[('')]/[y0/y1/y2]: cd ..                            # retornaria al node previ al de consulta nested

>> N
14:32:18 ~ <54..>[es][n][Canción]@[('')]/[y0/y1/y2]: goto -1
14:32:18 ~ <55>[es][n][Esperanza]@[('')]/[y0/y1/y2]: goto 14
14:32:18 ~ <14..>[es][n][Párbulos]@[('')]/[y0/y1/y2]: nhist -c / nhist
| Showing nesting history:
| <0> [es][v][Andar]@[('')] -> [es][v][Cercenar]@[('')]
| <1> [es][v][Cercenar]@[('')] -> [es][n][Elegía]@[('')]
...
| <55> [es][n][Humo]@[('')] -> [es][n][Cigarrillo electrónico]@[('')]
14:32:18 ~ <14..>[es][n][Párbulos]@[('')]/[y0/y1/y2]: ls
| Showing 7/35 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Vulgar
| 4. Electrocutar
>> cd 4
14:32:18 ~ <14.1>[es][n][Electrocutar]@[('')]/[y0/y1/y2]: nhist -c
| Warning. No depth was acquired yet.
14:32:18 ~ <14.1>[es][n][Electrocutar]@[('')]/[y0/y1/y2]: nhist   # 'cd ..' would return me to 14 after a warning
| Showing nested history:                                          # & 'ret' wwould return me to first node of all after a warning
| 1. <14..>[es][n][Párbulos]@[('')]
14:32:18 ~ <14.1>[es][n][Electrocutar]@[('')]/[y0/y1/y2]: cd 1
| Warning: this action will delete the nested search history. Are you sure? [Y/N]
>> Y
14:32:18 ~ <14..>[es][n][Párbulos]@[('')]/[y0/y1/y2]: sr
| Warning: this action will delete the nested search history. Are you sure? [Y/N]
>> Y
14:32:18 ~ [es][n][Párbulos]@[('')]/[y0/y1/y2]: cd ..
14:32:18 ~ [es][v][Andar]@[('')]/[y0/y1/y2]: nhist
| Warning. Working tree clean.
14:32:18 ~ [es][v][Andar]@[('')]/[y0/y1/y2]: hist
| Error. Needs argument 'lim'.
14:32:18 ~ [es][v][Andar]@[('')]/[y0/y1/y2]: hist 40 80
| Showing last visited nodes:
| ...
| /40 14:32:18 ~ [en][j][Normal]@[('')]/[y0/y1/y2]
| /41 14:33:16 ~ [es][v][Vejar]@[('')]/[e0]
...
| /80 14:33:16 ~ [es][v][Vejar]@[('')]/[e0]
14:32:18 ~ [es][v][Andar]@[('')]/[y0/y1/y2]: cd -40
| Warning: this action will delete the search history. Are you sure? [Y/N]
>> Y
14:32:18 ~ [en][j][Normal]@[('')]/[y0/y1/y2]: name -e
>> Banco
| Warning. There's already 2 entries called 'Banco'. Select one to merge.
|  1. [es][n][Banco]@[('institución')]
|  2. [es][n][Banco]@[('mobiliario')]
|  3. <new_lemma>
>> 3                                             # could've also directly writen the new lemma
| SYS. Enter the lemma for the new entry.
>> grupo
14:32:18 ~ [en][j][Banco]@[('grupo')]/[y0/y1/y2]: lemma -e
| Other lemmas for this entry are ...
|  1. Institución
|  2. Mobiliario
|  3. <new_lemma>
>> Grupo
14:32:18 ~ [en][j][Banco]@[('Grupo')]/[y0/y1/y2]: lemma -e
14:32:18 ~ [en][j][Banco]@[('Grupo')]/[y0/y1/y2]: rm
| Warning. Are you sure you want to remove this node (1159 edges)? [Y/N]
>> Y
14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]: ?                # returns to the last node
| The actions allowed at this status are ...
| : cd, set/unset, lemma, name, rm, undo.
| For further information, input '<action> --help'.
14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]: ls
| Showing 7/35 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Vulgar
| 4. Electrocutar
>> tf 4 6 1 7 > y0
>>
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



FUTUROS #############################################################################

| Showing nested history:
| root: [0] Andar(/7)
|       └── [1] Cercenar (<6th> of 7)
|            ├── [2] Elegía (<7th> of 7)
|            └── [3] Esperanza (<42th> of 102)

cd ..
| Warning: this action will delete the nested search history. Are you sure? [Y/N]


# ADDITIONAL IMPLEMENTATIONS ###########################
- undo
- status (already set, to do)
- ? # info of what can be done in the screen
- help ___
- suggestions
- and changing words from category (transfer)
- traduccion con filter, no con funcion explicita (same for merging synset1's, just a way to merge nodes and them also)

Useful symbols

<, >
clear, copy, paste
extract / export, min
commit, push, autosave 

# OBSERVATIONS AND VERY FUTURE STEPS
- min_path
- reduce a set
- search method
- decide where to use 'rich' colors
- I dont need a hist of every single action done. So hist will be just for visited nodes.

'''