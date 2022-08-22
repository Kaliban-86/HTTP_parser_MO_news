import pickle

with open('news_list.data', 'rb') as f:
   file = pickle.load(f)


for i in range(len(file)):
    print(file[i])
    print()