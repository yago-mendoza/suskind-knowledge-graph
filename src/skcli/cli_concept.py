
'''



# 1.1. Editing filters

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter -e
| Entered editor mode on filters:
| f1/type('w').lang('es')
| f2/starts('clar')
>> rm f1
>> add contains('esonate').lang('en')
>> ''
14:32:04 ~ [es][n][concept]@[(lemma)]/:

# 1.2. Sowing filters

14:32:04 ~ [es][n][concept]@[(lemma)]/: filter
| Showing filters:
| f1/lang('es').contains('trent')
| f2/starts('clar')
14:32:04 ~ [es][n][concept]@[(lemma)]/:

2. r ####################################
##########################################

14:32:11 ~ [es][n][concept]@[(lemma)]/: r -l -t   # random pero fijando lang and type
14:32:11 ~ [es][n][Queso]@[('')]/: r              # truly random
14:32:11 ~ [en][j][Small]@[('')]/: r -f           # will select a favorite one
No results founds.                                # si no encuentra resultados.

4. set ####################################
##########################################

# 4.1. Setting default global filter

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


6. ls CLI ###########################################
##########################################

>> del 8 7 6  # borrar entradas

>> del 8 7 6 -r  # refreshes (shows)

>> refresh  # refreshes (shows)

>> add Alto, Normal (te refieres a...?) # tiene que existir
| Error. Node 'asdf' was not found, hence, not included.

97. ? ##########################################
##########################################

| Displaying options at this point:
| ls : displays the nodes.
| status : shows the variables.
| Write '<command> ?' to obtain more info.

98. status #####################################
##########################################

14:32:18 ~ [en][j][Normal]@[('')]/[y1]: ls --status
| Showing 'ls' set parameters:
| .rand -off  (randomization)
| .sort -off  (sorting)
| .slit -off  (sliting output)
| .ncol 2     (nº of columns)
| .abbr -off  (abbreviating results)





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

14:32:18 ~ [en][j][Tall]@[('')]/[y0/y1/y2]: ls
| Showing 7/35 results:
| 1. Caminador            | 5. Golfo
| 2. Persona              | 6. Cercenar
| 3. Atrapar antes po...  | 7. Vulgar
| 4. Electrocutar
>> 4 6 1 7 > y0

TERMINAL
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

NESTED_HISTORY
| Showing nested history:
| root: [0] Andar(/7)
|       └── [1] Cercenar (<6th> of 7)
|            ├── [2] Elegía (<7th> of 7)
|            └── [3] Esperanza (<42th> of 102)
cd ..
| Warning: this action will delete the nested search history. Are you sure? [Y/N]


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

'''