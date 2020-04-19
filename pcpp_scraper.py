from pcpartpicker import API
import pandas as pd
import numpy as np
import json
from collections import defaultdict

def get_components(part_type="all"):
    '''
    If part_type not specified, returns dictionary where
    'key' is the part type and 'value' is an array containing 
    part component fields. If part_type is provided, returns 
    array of part components for specified part_type
    '''

    if part_type != "all" and part_type not in api.supported_parts:
        raise Exception("Argument 'part_type' is not a supported part. Type 'print(get_components().keys()' to view valid parts")
        return

    if part_type == "all":
        components = {}
        for part in api.supported_parts:
            components[part] = sorted(f for f in dir(api.retrieve(part)[part][1]) if not f.startswith('__'))
    else:
        part = part_type
        components = sorted(f for f in dir(api.retrieve(part)[part][1]) if not f.startswith('__'))
    
    return components

def list_part_quantities():
    '''
    List out al parts and there quantities
    '''
    num_parts = 0
    all_parts = api.retrieve_all()

    print("\nList of PC parts and quantities:\n")

    for part in api.supported_parts:
        print("{0}: {1}".format(part, len(all_parts[part])))
        all_parts[part]
        num_parts += len(all_parts[part])

    print("\nTotal: {0}".format(num_parts))

def add_to_parts_dict_as_df(part, dict):
    parts_dict = defaultdict(list)
    retrieved_parts = api.retrieve(part)[part]
    for p in retrieved_parts:
        for key, comp in vars(p).items():
            parts_dict[key].append(comp)
    
    dict[part] = pd.DataFrame.from_dict(parts_dict)
    return dict

def create_parts_dict(part_type="all"):
    '''
    If part_type not specified, returns dictionary where
    'key' is the part type and 'value' is a DataFrame of parts. 
    If part_type is provided, returns DataFrame of part 
    for specified part_type
    '''

    if part_type != "all" and part_type not in api.supported_parts:
        raise Exception("Argument 'part_type' is not a supported part. Type 'print(get_components().keys()' to view valid parts")
        return

    parts_dict = {}
    if part_type == "all":
        for part in api.supported_parts:
            parts_dict = add_to_parts_dict_as_df(part, parts_dict)
    else:
        parts_dict = add_to_parts_dict_as_df(part_type, parts_dict)
            
    return parts_dict


if __name__ == "__main__":
    api = API('us')
    
    # print(get_components())
    list_part_quantities()
    parts_dict = create_parts_dict()