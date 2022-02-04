import psutil
import subprocess
import csv
import time
import datetime


def start_program():
    """Функция для запроса у пользователя пути к файлу и интервала сбора метрик"""

    file_path = input('Enter path file: ')
    interval = int(input('Enter the interval for collecting statistics (seconds): '))
    get_data(file_path, interval)


def get_data(file_path, interval):
    """Функция создает процесс для которого будут собираться метрики,
    создает файл для хранения метрик и вносит метрики в csv файл"""

    # инициализация процесса
    start_process = subprocess.Popen(file_path)
    process = psutil.Process(start_process.pid)

    # инициализация уникального имени для файла с метриками
    name_process = process.name().replace(".", "_")
    date = datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y%m%d_%H%M%S")
    name_data = f'{name_process}_{date}.csv'

    # внесение в файл метрик названия столбцов
    result = ['CPU_usage', 'Working_set', 'Private_bytes', 'Open_hendlers']
    save_data(result, name_data)

    # цикл со сбором метрик с последующей записью в файл
    while psutil.pid_exists(start_process.pid):
        try:
            result = [round(process.cpu_percent(0.1) / psutil.cpu_count(0.1)),
                      process.memory_info().wset,
                      process.memory_info().vms,
                      len(process.open_files())]
            save_data(result, name_data)
            time.sleep(interval)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            break


def save_data(data, data_file):
    """Функция для записи данных в файл"""

    with open(data_file, 'a') as table:
        writer = csv.writer(table)
        writer.writerow(data)


if __name__ == '__main__':
    start_program()
