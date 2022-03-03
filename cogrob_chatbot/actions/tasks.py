#!/usr/bin/env python3

def addItemCommand(basket, item):
    if item in basket.keys():
        basket[item] = int(basket[item]) + 1
    else:
        basket[item] = 1
    
    return basket
                
def showBasket(basket):
    for item in basket:
        print(item, basket[item])
    
def removeItem(basket, item):
    if item in basket.keys():
        basket.pop(item)
    else:
        print('No element to remove')

    return basket

def deleteBasket(basket):
    pass
    


