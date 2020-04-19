from pcpartpicker import API
import pandas as pd
import numpy as np
from collections import defaultdict
from pprint import pprint
import os
import logging as log

class PCParts:
    
    log.basicConfig(filename='debug.log',level=log.DEBUG)

    def __init__(self, debug=False, region='us'):
        self.pcpp_api = API(region)
        self.parts = {}
        self.path = './Parts_Scraper/pickle/'
        log.debug("PCParts object init")
        
        #self.refresh_data()

    def set_region(self, new_region):
        '''
        Set region per pcpartspicker API requirements.
        '''

        if new_region in self.pcpp_api.supported_regions:
            self.pcpp_api.set_region(new_region)
        return

    def refresh_data(self):
        '''
        Refresh temp storage cache
        '''
        self.__load_part_data(refresh=True)
    
    def get_JSON(self, part='cpu'):
        if part not in self.pcpp_api.supported_parts:
            raise Exception("Argument 'part' is not a supported part.")
            return
        
        if not self.parts: self.__load_part_data()
        js = self.parts[part].to_json(orient='split')
        return js

    def get_components(self):
        '''
        Returns dictionary of parts and their components as an array
        '''
       
        if not self.parts:
            log.debug("Loading data for all parts...")
            self.__load_part_data("all")
        
        log.debug("Getting part components...")
        
        components = {}
        for part, df in self.parts.items():
            components[part] = [c for c in df.columns]

        return components

    def get_quantities(self):
        '''
        List out all parts and there quantities
        '''

        if not self.parts: self.__load_part_data("all")
        
        log.debug("Getting part quantities...")

        num_parts = 0
        quantities = {}
        for part, df in self.parts.items():
            quantities[part] = len(df.index)
            num_parts += len(df.index)

        log.debug("Quantity of parts: " + str(num_parts))

        return quantities

    def __load_part_data(self, refresh=False):
        '''
        Loads all part data. Refresh=true will refresh temp data storage cache
        '''
        if refresh: load_type = "Refreshing"
        else: load_type = "Loading"

        log.debug("{0} data...".format(load_type))
        
        for part in self.pcpp_api.supported_parts:
            self.__add_part_df_to_dict(part, refresh)

        log.debug("{0} complete.".format(load_type))
        
        return

    def __add_part_df_to_dict(self, part="all", refresh=False):
        '''
        Convert part objects retrieved from PcPartsPicker API to dataframe
            and save as temp data storage(pickle).
        If refresh is specified, overwrite pickle storage files
        '''

        path = self.path + part + '.pkl'
        if os.path.exists(path) and not refresh:
            df = pd.read_pickle(path)
        else:
            parts_dict = defaultdict(list)
            retrieved_parts = self.pcpp_api.retrieve(part)[part]
            for p in retrieved_parts:
                for key, comp in vars(p).items():
                    parts_dict[key].append(comp)
            df = pd.DataFrame.from_dict(parts_dict)
            df.to_pickle(path)
        
        self.parts[part] = df
        return
