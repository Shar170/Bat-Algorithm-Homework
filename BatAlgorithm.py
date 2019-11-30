import numpy as np
import math

np.random.seed(100)


class BatAlgorithm():
    def __init__(self, dimensi, n_bat, n_generasi, r0, alpha, gamma, fmin, fmax, b_down, b_up, fungsi, maxCount):
        self.dimensi = dimensi
        self.n_bat = n_bat
        self.n_generasi = n_generasi
        self.alpha = alpha
        self.gamma = gamma
        self.fmin = fmin
        self.fmax = fmax
        self.b_down = b_down
        self.b_up = b_up
        self.fungsi = fungsi
        self.epsilon = 0.001
        self.r0 = r0
        self.maxCount = maxCount

        # инициализировать значения громкости (A) и частоты пульса (r)
        self.A = [0.95 for i in range(self.n_bat)]
        self.r = [self.r0 for i in range(self.n_bat)]

        # инициализация верхней границы и нижней границы для каждой летучей мыши
        self.upbound = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        self.lowbound = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]

        # инициализировать значение 0 для всех летучих мышей
        self.frekuensi = [0.0] * n_bat

        # инициализировать значение v (скорость) для всех летучих мышей
        self.v = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]

        # инициализировать значения х (местоположение / решение) для всех летучих мышей
        self.x = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]

        # инициализировать значение пригодности для всех летучих мышей
        self.nilai_fitness = [0.0] * n_bat
        self.nilai_fitness_minimum = 0.0

        # инициализиуем массив для истории улучшения
        self.history = []

        # инициализация лучшего решения
        self.best = [0.0] * dimensi

    def bat_terbaik(self):
        i = 0
        j = 0
        # найдите лучшее значение приспособленности и отметьте индекс по переменной j
        for i in range(self.n_bat):
            if self.nilai_fitness[i] < self.nilai_fitness[j]:
                j = i

        # сохранить значения каждого измерения в лучшем решении
        for i in range(self.dimensi):
            self.best[i] = self.x[j][i]

        # сохранить ценность приспособленности от лучшего решения
        self.nilai_fitness_minimum = self.nilai_fitness[j]

    def proses_init(self):
        # установить все верхние и нижние параметры, которые были установлены ранее
        for i in range(self.n_bat):
            for j in range(self.dimensi):
                self.lowbound[i][j] = self.b_down
                self.upbound[i][j] = self.b_up

        # генерировать новые решения из нижнего и верхнего пределов и установить все частоты летучих мышей на 0
        # bat не ищет цель v = 0.
        for i in range(self.n_bat):
            self.frekuensi[i] = 0
            for j in range(self.dimensi):
                random = np.random.uniform(0, 1)
                self.v[i][j] = 0.0
                self.x[i][j] = self.lowbound[i][j] + (self.upbound[i][j] - self.lowbound[i][j]) * random
            self.nilai_fitness[i] = self.fungsi(self.x[i])

        # найти летучую мышь с наименьшим значением пригодности (минимум)
        self.bat_terbaik()

    def normalisasi_batas(self, nilai):
        # если значение превышает верхний предел, то установленное значение становится верхним пределом
        if (nilai > self.b_up):
            nilai = self.b_up

        # если значение меньше нижнего предела, установите значение нижнего пределаh
        if (nilai < self.b_down):
            nilai = self.b_down

        return nilai
    def getMaxCount(self):
        return self.maxCount

    def proses_ba(self):
        # матричное решение (много размеров ЛМ х РАЗМЕРНОСТЬ)
        solusi = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        count = 0
        self.proses_init()
        #         print(self.nilai_fitness)
        # np.random.seed(self.dimensi*self.maxCount/(self.maxCount+np.exp(self.dimensi)))
        for n in range(self.n_generasi):
            Arata2 = np.mean(self.A)
            for i in range(self.n_bat):
                random = np.random.uniform(0, 1)
                # найти частоту каждой летучей мыши с помощью уравнения 2
                self.frekuensi[i] = self.fmin + (self.fmax - self.fmin) * random
                for j in range(self.dimensi):
                    # найти новые v и x каждой летучей мыши, используя уравнение 3 и 4 алгоритма летучей мыши
                    self.v[i][j] = self.v[i][j] + (self.x[i][j] - self.best[j]) * self.frekuensi[i]
                    solusi[i][j] = self.x[i][j] + self.v[i][j]
                    solusi[i][j] = self.normalisasi_batas(solusi[i][j])

                random = np.random.uniform(0, 1)
                # если случайное значение [0,1] больше значения частоты пульса летучей мыши, то выполнить локальный
                # поиск на основе лучшей летучей мыши
                if (random > self.r[i]):
                    for j in range(self.dimensi):
                        random = np.random.uniform(-1.0, 1.0)
                        solusi[i][j] = self.best[j] + random * Arata2
                        solusi[i][j] = self.normalisasi_batas(solusi[i][j])

                # рассчитать пригодность нового решения
                nilai_fitness = self.fungsi(solusi[i])

                random = np.random.uniform(0, 1)

                if (random < self.A[i] and nilai_fitness < self.nilai_fitness[i]):
                    self.nilai_fitness[i] = nilai_fitness
                    for j in range(self.dimensi):
                        self.x[i][j] = solusi[i][j]

                if (self.nilai_fitness[i] < self.nilai_fitness_minimum):
                    # заменить лучшее решение
                    self.nilai_fitness_minimum = self.fungsi(solusi[i])
                    for j in range(self.dimensi):
                        self.best[j] = self.x[i][j]

                        # обновлять громкость и частоту пульса каждой летучей мыши
                    self.A[i] = self.A[i] * self.alpha
                    self.r[i] = self.r0 * (1 - math.exp(-1 * self.gamma * i))
            #             print("Ценность поколении для расчёта (", n, ") : ", self.nilai_fitness)
            self.history.append(self.nilai_fitness_minimum)
            #print(n, ' Решение %.4f' % self.nilai_fitness_minimum, '\t', self.best)
            # print("Лучшее решение ", )

            if n > self.maxCount+2:
                if np.min(self.history[n - self.maxCount:n - 2]) <= self.nilai_fitness_minimum:
                    count = count + 1
                    if count >= self.maxCount:
                        print('Улучшений не было в течении ', self.maxCount, ' прошло ', n, 'итераций')
                        print(n, ' Решение %.4f' % self.nilai_fitness_minimum, '\t', self.best)
                        self.history = np.array(self.history)
                        return 0
                else:
                    #print('count сброшен')
                    count = 0
        print('Расчёт закончился по истечению максимума итераций (', self.n_generasi, ')')
        print(self.nilai_fitness_minimum)
        print(self.best)
        return 1
