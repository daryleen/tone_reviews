from superSort import *
import openpyxl
import random


def create_weights(all_unique_words):
    random.seed(2)
    random_weight = []
    for _ in range(all_reviews_len):
        row = [random.randint(1, 9) for _ in range(all_unique_words+1)]
        random_weight.append(row)
    return random_weight


def evaluate_test_review(test_review, random_weights, border_net):
    net = 0
    for k in range(all_unique_words):
        net += random_weights[0][k] * test_review[k]  # Предполагается, что test_review - это список признаков для тестового отзыва

    if net > border_net:
        return "Положительный отзыв"
    else:
        return "Отрицательный отзыв"


# количество всех отзывов + кол-во уникальных слов для использования в циклах
all_reviews_len = len(positive_reviews) + len(negative_reviews)
all_unique_words = len(dataset_words)
print(all_reviews_len,all_unique_words)
net = 0
random_weights = create_weights(all_unique_words)
print(random_weights[0][0],"\n", random_weights[all_reviews_len-1])
# workbook = openpyxl.load_workbook("результат.xlsx")
# sheet = workbook.active

# Загружаем Excel-файл
workbook = openpyxl.load_workbook("результат.xlsx")
sheet = workbook.active

# Считываем данные из ячеек A3 до A502
reviews = []
for row in sheet.iter_rows(min_row=3, max_row=all_reviews_len+2, min_col=1, max_col=1, values_only=True):
    reviews.append(row[0])

# Считываем значения из ячеек B3 до HH3 и записываем в массив arr
x_values = []
for row in sheet.iter_rows(min_row=3, max_row=all_reviews_len+2, min_col=2, max_col=all_unique_words+1, values_only=True):
    x_values.append(list(row))

test_review = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

EPOCH = 10000
border_net = 1000
count = 0
shuffled_indices = list(range(len(reviews)))
true_rev = []
false_rev = []
all_rev = [str(i) + ("T" if i < 250 else "F") for i in shuffled_indices]
print(all_rev)
random.shuffle(all_rev)
for i in range(EPOCH):
    correct_ans = 0
    faults = 0
    # Перемешиваем индексы обучающих примеров перед каждой эпохой
    for j in range(len(all_rev)):
        net = 0
        for k in range(all_unique_words):
            #print(j,k)
            net += random_weights[j][k] * x_values[j][k]
        if ( "T" in all_rev[j] and net > border_net) or ("F" in all_rev[j] and net < border_net):
            correct_ans += 1
        elif "T" in all_rev[j] and net < border_net:
            faults += 1
            for n in range(all_unique_words):
                if x_values[j][n] == 1:
                    random_weights[j][n] += 1
        elif "F" in all_rev[j] and net > border_net:
            faults += 1
            for n in range(all_unique_words):
                if x_values[j][n] == 1:
                    random_weights[j][n] -= 1
    #print(*random_weights)
    correct_percent = correct_ans * 100 / all_reviews_len
    faults_percent = faults * 100 / all_reviews_len
    print(f"Epoch {i + 1}: Correct Answers: {correct_percent}%, Faults: {faults_percent}%")

answer = evaluate_test_review(test_review, random_weights, border_net)
print(answer)