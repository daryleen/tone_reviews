import openpyxl

# Открываем файл Excel для записи
workbook = openpyxl.Workbook()
sheet = workbook.active

# Открываем текстовый файл для чтения
with open('1.txt', 'r', encoding='utf-8') as file:
    # Считываем строки из текстового файла
    lines = file.readlines()

# Записываем каждое слово в столбик в Excel
for line in lines:
    words = line.strip().split() # Разбиваем строку на слова
for word in words:
    sheet.append([word]) # Добавляем каждое слово в новую ячейку

# Сохраняем результаты в Excel-файл
workbook.save('уникальные_слова.xlsx')

print("Слова успешно записаны в Excel-файл.")