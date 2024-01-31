import difflib

def parse_idxs_to_single_idxs (string):
    numbers_set = set()
    for part in string.split():
        if '-' in part:
            start, end = map(int, part.split('-'))
            numbers_set.update(range(start, end + 1))
        else:
            numbers_set.add(int(part))
    return sorted(numbers_set)

def find_similars(graph, target_name, k=1):
    scores = [(difflib.SequenceMatcher(None, target_name.lower(), node.name.lower()).ratio(), node) for node in graph]
    top_scores = sorted(scores, key=lambda x: x[0], reverse=True)[:k]
    return [node for ratio, node in top_scores]

def parse_field(*fielding, long=False, numeric=False):

    """
    {y0, y1, y2, e0, e1, e2,
    synset0, synset1, synset2, semset0, semset1, semset2,
    semset, synset,
    e, y,
    '111000' permission fieldings, or '11' (rest 0s)}
    @ STRING / LIST
    -> SHORT / LONG / NUMERIC format ((0-1-2, y-e) sorted)

    INPUT #############################################################
    (either standalone STRING or LIST of strings, or multiple arguments)
    - single short :   parse_field('e1')
    - single long :    parse_field('synset1')
    - global short :   parse_field('e')
    - global long :    parse_field('semset')
    - binary partial : parse_field('111')
    - binary full :    parse_field('111000')
    
    Note : if no fielding arg is used, will pick the WHOLE fielding set.

    OUTPUT #############################################################
    (LIST sorted as (0-1-2) and (y-e))
    -      default : 'short'
    -    long=True : 'long'
    - numeric=True : 'numeric'
    """

    fielding = [item for sublist in fielding for item in (sublist if isinstance(sublist, list) else [sublist])]

    short_y = ['y0', 'y1', 'y2']
    short_e = ['e0', 'e1', 'e2']

    if not fielding:
        parsed = short_y + short_e

    else:

        global_map = {'synset': short_y, 'semset': short_e, 'y': short_y, 'e': short_e}

        def parse_item(item):

            if item.isdigit():
                item = item.ljust(6, '0')
                return [bichar for binary, bichar in zip(item, 'y0 y1 y2 e0 e1 e2'.split()) if binary == '1']
            elif item in global_map:
                return global_map[item]
            elif len(item) == 7:
                return [item[1] + item[-1]]
            else:
                return [item]

        items = [fielding] if isinstance(fielding, str) else fielding
        parsed = sorted(set(sum([parse_item(item) for item in items], [])),
                        key=lambda x: (x[0] == 'e', int(x[1])))

    if numeric:
        return ''.join(['1' if f'y{i}' in parsed else '0' for i in range(3)]) + \
               ''.join(['1' if f'e{i}' in parsed else '0' for i in range(3)])
    elif long:
        return [f"synset{item[1]}" if item[0] == 'y' else f"semset{item[1]}" for item in parsed]

    return parsed
