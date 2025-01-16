# question = input('enter text:')
# print(question)

# test = {
#     'living room': 1,
#     'bathroom': 2
# }

# map_name = input('enter map name: ')
# if map_name in test:
#     level = test[map_name]
#     print(level)
# if map_name not in test:
#     levels = list(test.values())
#     test[map_name] = levels[-1] + 1

# print(test)

import os

maps = []
for map_name in os.listdir('PadlockGamePractice/assets/rooms'):
    maps.append(map_name.split('.')[0])

print(maps)