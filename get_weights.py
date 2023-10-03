import pickle

# Загрузить переменную random_weights из файла
with open("perfect_weights.pkl", "rb") as file:
    loaded_weights = pickle.load(file)

print("Переменная random_weights загружена из файла:")
print(loaded_weights)
