from sys import argv
from threading import Thread
from time import time
from zipfile import ZipFile


# DIVIDE EL DICCIONARIO EN PARTES IGUALES
def divisor(lst, n):
    p = len(lst) // n
    if len(lst) - p > 0:
        return [lst[:p]] + divisor(lst[p:], n - 1)
    else:
        return [lst]


# MAIN CRACKER
class Craker:
    # EL METODO INIT SE INICIA CADA VEZ QUE INICIES LA CLASE
    def __init__(self, dictionaryArray, zipFile):
        self.dictionary = dictionaryArray
        self.zip = zipFile
        self.thread = Thread(target=self.__cracker)
        self.__running = True

    # INICIA EL CRACKING
    def run(self):
        self.thread.start()

    # CRACKER
    def __cracker(self):
        Zip = ZipFile(self.zip, mode="r")
        start_time = time()
        for password in self.dictionary:
            if not self.__running: break
            try:
                Zip.extractall(pwd=bytes(password, 'utf-8'))
            except:
                pass
            else:
                print(chr(27) + "[0;31m" + "Password Found: " + chr(27) + "[0;32m" + password)
                print(chr(27) + "[0;31m" + "Time to Find: " + chr(27) + "[0;32m" + str(round(abs(time() - start_time), 4)))
                self.__stop_all()

    # PARAR TODOS LOS THREADS
    @staticmethod
    def __stop_all():
        global cracker_list
        for object_ in cracker_list:
            object_.__running = False


if __name__ == '__main__':
    if len(argv) < 3: print("Usage:\nzipcracker.py <dictionary> <zip> [options]\n\nOptions:\nThreads: <threads>\nDelimeter: <delimeter>");exit()

    with open(argv[1], "r", errors="ignore") as file:
        dictionary = file.read().split(argv[4] if len(argv) >= 5 else "\n")
        print(chr(27) + "[0;33m" + "Dictionary lenght: ", len(dictionary))

    amount_threads = int(argv[3]) if len(argv) >= 4 else 1
    equitative_dict = divisor(dictionary, amount_threads)
    with open("log.txt", "w") as dict_:
        dict_.write(str(equitative_dict))

    cracker_list = []
    for thread in range(len(equitative_dict)):
        cracker = Craker(equitative_dict[thread], argv[2])
        cracker_list.append(cracker)
        cracker.run()
    print(chr(27) + "[0;36m" + "Started threads: ", len(cracker_list))
