import psutil
import subprocess
import csv
import time


def get_user_input():
    """Функция запрашивает входные данные (путь к файлу и интервал сбора метрик)"""

    file_path = input('Enter path file: ')
    interval = int(input('Enter the interval for collecting statistics (sec): '))
    return file_path, interval


def get_data(file_path, interval):
    """Функция создает процесс для которого будут собираться метрики,
    создает файл для хранения метрик и вносит метрики в файл"""

    # инициализация процесса
    start_process = subprocess.Popen(file_path)
    process = psutil.Process(start_process.pid)

    # инициализация уникального имени для файла с метриками
    name_data = f'{process.name().replace(".", "_")}_{time.strftime("%Y%m%d_%H%M%S", time.gmtime(process.create_time()))}.csv'

    # внесение названий столбцов в файл метрик
    result = ['CPU_usage', 'Working_set', 'Private_bytes', 'Open_hendlers']
    save_data(result, name_data)

    # цикл сбора метрик, их записью в файл и интервальным ожиданием
    while psutil.pid_exists(start_process.pid):
        try:
            result = [round(process.cpu_percent(0.1) / psutil.cpu_count()),
                      process.memory_info().wset,
                      process.memory_info().vms,
                      process.num_handles()]
            save_data(result, name_data)
            time.sleep(interval)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as Exc:
            print(Exc)
            break


def save_data(data, data_file):
    """Функция записывает данные в файл csv"""

    with open(data_file, 'a') as table:
        writer = csv.writer(table)
        writer.writerow(data)


if __name__ == '__main__':
    get_data(*get_user_input())
