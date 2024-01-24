def parse_field(fielding, long=False, numeric=False):

    if not fielding:
        return None
    
    # fielding = 'synset' / 'semset'
    if isinstance(fielding, str) and len(fielding)==6:
        fielding = [fielding[1]+str(i) for i in range(3)]

    # fielding = '11' / '110000' / 'synset1' / 'e0'
    if isinstance(fielding, str):
        if fielding.isnumeric():
            # 'fielding' str is a numeric permissions code
            binary = fielding.ljust(6,'0') # in case it gave '0's by granted
            fielding = [field for i, field in enumerate(['y0', 'y1', 'y2', 'e0', 'e1', 'e2'])if binary[i] == '1']
        else:
            # 'fielding' is a single str
            fielding = [fielding]

    # fielding = ['synset0', 'semset1'] / ['y0', 'y1', ...] / ['semset0', 'y1']
    parsed_fields = [field[1]+field[-1] if len(field)==7 else field for field in fielding]

    # Now that we know for sure the fields are in short-str format, we proceed to parse them into
    # the requested format (either long or numeric).

    if long:
        parsed_fields = [f"s{field[0]}nset{field[1]}" for field in parsed_fields]
    elif numeric:
        syns = ''.join(['1' if f'y{i}' in parsed_fields else '0' for i in range(3)])
        sems = ''.join(['1' if f'e{i}' in parsed_fields else '0' for i in range(3)])
        parsed_fields = syns+sems
    
    return parsed_fields

    
