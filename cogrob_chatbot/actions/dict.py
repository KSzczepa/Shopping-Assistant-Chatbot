import os

class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict()
          
    # Function to add key:value 
    def add(self, key, value, quantity=1): 
        # self[key] = value 
        if key not in self:
            self[key] = {value:0}
        if value not in self[key]:
            num = 0
        else:
            num = self[key][value]
        self[key].update({value: num+quantity})


    def remove(self, key, value='none'):
        if value == 'none':
            for iter in self[key]:
                self[key].pop(iter)
            out_msg = f'List has been cleared for {key}.'
        else:
            if value in self[key]:
                self[key].pop(value)
                out_msg = f'Product {value} has been removed from your shopping list.'
            else:
                out_msg = f'Item {value} is not on the list. No elements has been removed.'
        return out_msg


    def show(self, key='all'):
        if key == 'all':
            out_msg = ''
            for key in self:
                out_msg = f'{out_msg}{key} '
                for iter in self[key]:
                    out_msg = f'{out_msg}  {iter} {self[key][iter]}'
                out_msg = f'{out_msg} \n'
            out_msg = os.linesep.join([s for s in out_msg.splitlines() if s])  #delete empty lines
            return out_msg
        else:
            if key in self:
                # print(f'{key}: ')
                out_msg = f'{key} '
                for iter in self[key]:
                    # print('\t',iter, self[key][iter])
                    out_msg = f'{out_msg}  {iter} {self[key][iter]}'
                return out_msg






