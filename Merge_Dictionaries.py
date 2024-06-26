#Merging two dictionaries (applicable in python 3.5+)

# Using the ** operator
def merge_dict(dict1, dict2):
    return {**dict1, **dict2}

dict1 = {'a': 10, 'b': 8}
dict2 = {'c': 6, 'd': 4}
dict3 = merge_dict(dict1, dict2)
print(dict3)

