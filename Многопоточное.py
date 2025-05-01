#Каждый корпус обрабатывается в отдельном потоке
import threading
import time
import random

class Student:
    def __init__(self, id, has_student_id, bag_size):
        self.id = id
        self.has_student_id = has_student_id
        self.bag_size = bag_size

def process_student(student, building, no_id_students, max_bag_student, lock):
    with lock:
        if not student.has_student_id:
            no_id_students.append(student.id)
        if student.bag_size > max_bag_student[1]:
            max_bag_student[0] = student.id
            max_bag_student[1] = student.bag_size

    if not student.has_student_id or student.bag_size > 30:
        print(
            f"Студент под номером {student.id} требует проверки {building}. Размер сумки: {student.bag_size} . Наличие студенческого билета: {'есть' if student.has_student_id else 'нет'}")
        time.sleep(random.uniform(2, 3))
    else:
        print(f"Студент под номером {student.id} в корпусе {building} не требует проверки.")

def building_thread(building, students, no_id_students, max_bag_student, lock):
    for student in students:
        process_student(student, building, no_id_students, max_bag_student, lock)

def multi_threaded_version():
    buildings = [1, 2, 3, 4]
    students = [Student(i, random.choice([True, False]), random.randint(20, 50)) for i in range(10)]

    no_id_students = []
    max_bag_student = [None, 0]
    lock = threading.Lock()#Блокировка для потокобезопасного доступа к общим данным

    start_time = time.time()

    threads = []
    for building in buildings:
        thread = threading.Thread(target=building_thread,
                                  args=(building, students, no_id_students, max_bag_student, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"Студенты без студенческого билета: {no_id_students}")
    print(f"Студент с самой большой сумкой: Номер студента {max_bag_student[0]}, размер сумки: {max_bag_student[1]}")
    print(f"Программа выполнена за {end_time - start_time:.2f}")

if __name__ == "__main__":
    multi_threaded_version()