from superSort import *
import openpyxl
import numpy as np


def create_weights(dataset_word):
    random.seed(2)
    random_weight = []
    for i in range(len(dataset_word)):
        random_weight.append(int(random.random() * 9 + 1))
    return random_weight


net = 0
random_weights = create_weights(dataset_words)
# print(*random_weights)

workbook = openpyxl.load_workbook("результат.xlsx")
sheet = workbook.active

# Загружаем Excel-файл
workbook = openpyxl.load_workbook("результат.xlsx")
sheet = workbook.active

# Считываем данные из ячеек A3 до A502
reviews = []
for row in sheet.iter_rows(min_row=3, max_row=502, min_col=1, max_col=1, values_only=True):
    reviews.append(row[0])

# Считываем значения из ячеек B3 до HH3 и записываем в массив arr
x_values = []
for row in sheet.iter_rows(min_row=3, max_row=3, min_col=2, max_col=249, values_only=True):
    for cell in row:
        if cell is not None:
            x_values.append(cell)
EPOCH = 100
correct_ans = 0
faults = 0
border_net = 1000
count = 0
for i in range(EPOCH):
    # Перемешиваем индексы обучающих примеров перед каждой эпохой
    shuffled_indices = list(range(len(reviews)))
    random.shuffle(shuffled_indices)
    correct_ans = 0
    faults = 0

    for j in shuffled_indices:
        # Установка значения переменной review_tone в зависимости от положения отзыва
        if reviews[j] in reviews[:250]:
            review_tone = 1
        else:
            review_tone = 0
        net = 0

        for k in range(len(random_weights)):
            net += random_weights[k] * x_values[k]
        if (review_tone == 1 and net > border_net) or (review_tone == 0 and net < border_net):
            correct_ans += 1
        elif review_tone == 1 and net < border_net:
            faults += 1
            for n in range(len(random_weights)):
                if x_values[n] == 1:
                    random_weights[n] += 1
        elif review_tone == 0 and net > border_net:
            faults += 1
            for n in range(len(random_weights)):
                if x_values[n] == 1:
                    random_weights[n] -= 1
    # print(*random_weights)
    print(f"Epoch {i+1}: Correct Answers: {correct_ans * 100 / 500}%, Faults: {faults * 100 / 500}%")

