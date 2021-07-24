import pandas as pd
import random
import networkx as nx
import math
import os
import matplotlib.pyplot as plt
from generator import *

def gen_alg(epoch, num_popul, n_surv, new_mut, zero_bot=[]):
    # ============================
    # === Функция писка оптимального распределения товаров и маршрутов по машинам
    # ============================
    # epoch - количество эпох
    # num_popul -  размер популяций
    # n_surv   - количество выживших после каждой эпохи
    # new_mut  - количество мутировавших ботов в новой эпохе
    def created_bot(adres_list, vol_list, mass_list, n=10, k=0.2, n_add_car=10, k_ts=0.3):
        # Функция создания одного бота
        # n -размер ограничения по максимальныму количеству адресов для одной машины.
        # k -коэффицент распределения количества адресов (чем он больше - тем чаще машинам будет присваиваться  большое количество адресов))
        # n_add_car  - количество машин которые можно задействовать  сверх оптимального.
        # k_ts  - коэффицент распределения типов ТС в боте.
        # ------------------------
        list_ind = [i for i in range(len(adres_u_list))]
        random.shuffle(list_ind)  # Момент рандомизации (он и задаёт все различия ботов между собой)
        # ------------------------

        if sum([sum(i) for i in vol_list]) / predel[0][1] > sum([sum(i) for i in mass_list]) / predel[0][0]:
            min_car = int(sum([sum(i) for i in vol_list]) / predel[0][1])
        else:
            min_car = int(sum([sum(i) for i in mass_list]) / predel[0][0])

        if min_car < int(sum([len(i) for i in zakaz_list[1:]]) / n):
            min_car = int(sum([len(i) for i in zakaz_list[1:]]) / n)

        optimal = int(len(adres_list) / min_car) if int(len(adres_list) / min_car) < n else n
        ns = random.randint(int(min_car), int(min_car + n))

        # ------------------------
        bot = []  # один бот в популяции
        z = 0  # cчетчик для адресов
        end = False
        # ------------------------

        n_car = random.randint(min_car, (min_car + n_add_car))
        for i in range(n_car):
            sp = [0]  # Список адресов которые должна посетить каждая машина
            car = []  # Список машин в боте.  В каждой [0] - Тип ТС этой машины , [1] - фирма грузоперевозчика [2] - список адресов которые нужно посетить
            ns2 = random.random()
            if ns2 < k_ts:
                car.append(1)
            else:
                car.append(0)
            car.append(random.randint(1, 2))
            if k > random.random():  # Генерируем количество адресов для 1  машины
                ns3 = optimal
            else:
                ns3 = random.randint(1, n)
            for j in range(ns3):
                if z < len(list_ind):
                    if list_ind[z] != 0:
                        sp.append(list_ind[z])
                    z += 1
                    if i == n_car - 1 and z < len(list_ind):

                        for k in range(len(list_ind) - z):
                            sp.append(list_ind[z])
                            z += 1

                else:
                    break

            sp = list(set(sp))
            car.append(sp)
            if len(sp) > 1:
                bot.append(car)
        # print(min_car,"min_car")
        # print(optimal,"optimal")
        # for i in bot:
        #   print(len(i[2]))
        return bot

    def time_from_normal(x):
        ch = (x // 1) * 2
        k = 100 / 60
        m = (x % 1 / k) * 100
        if int(m) >= 31:
            ch += 2
        if int(m) > 0 and int(m) < 31:
            ch += 1
        return int(ch)

    def time_way(way, t):
        new_way = []
        x = 0
        for i in range(len(way)):
            if way[i] == 0 and x < t:
                x += 1
                new_way.append(1)

            else:
                if way[i] == 0 and x >= t:
                    new_way.append(0)
                else:
                    new_way.append(1)

            if x < t and i == len(way) - 1:
                new_way.append(1)
        return new_way

        # -------------------------------------------------------------------------------

    def loss_gen(popul, matrix_distance):
        # Функция подсчёта ошибки
        loss_all = []
        loss_bot = []
        for i in range(len(popul)):
            l = 0
            loss_bot.append([])
            for j in range(len(popul[i])):
                loss_bot[i].append([])
                for k in range(len(popul[i][j])):
                    # print(i,j,popul[i][j][k])
                    if k == 0:
                        loss_bot[i][j].append(0)
                    else:
                        loss_bot[i][j].append(matrix_distance[popul[i][j][k - 1]][popul[i][j][k]])
                l += sum(loss_bot[i][j])
            loss_all.append(l)
        return loss_all, loss_bot

    # y,x=loss_gen(created_popul(adres_list, volume_list, predel,100,6),matrix_distance)

    def mut_gen_2(bot):
        # Функция мутации
        bot_mut = []
        for i in range(len(bot)):  # Проходимся по лучшимм ботам
            car = []
            n = random.random()
            if n > 0.5:
                og = 0 if bot[i][0] != 0 else 1
                p = bot[i][1]
            else:
                p = 1 if bot[i][1] != 1 else 2
                og = bot[i][0]
            car.append(og)
            car.append(p)
            sp = bot[i][2][:]

            car.append(sp)

            bot_mut.append(car)
        return bot_mut
        # -------------------------------------------------------------------------------

    def mut_gen(bot, mut):
        # Функция мутации
        bot_mut = []
        for i in range(len(bot)):  # Проходимся по лучшимм ботам
            car = []
            p = bot[i][1]
            og = bot[i][0]
            n = random.random()
            if n < mut:
                p = random.randint(1, 2)
            n = random.random()
            if n < mut:
                og = random.randint(0, 1)
            car.append(og)
            car.append(p)
            sp = bot[i][2][:]

            n = random.random()
            if n < mut and len(sp) > 1:
                z1 = random.random()
                if z1 > 0.7:
                    raz = 1
                else:
                    raz = random.randint(1, 4)
                for q in range(raz):
                    n = random.randint(1, len(sp) - 1)
                    m = random.randint(1, len(sp) - 1)
                    # sp=sp.astype(int).tolist()
                    sp[m], sp[n] = sp[n], sp[m]
            car.append(sp)

            bot_mut.append(car)
        return bot_mut

        # -------------------------------------------------------------------------------

    # Функция сортировки популяции
    def getSurvPopul(popul, val, n_surv, reverse):
        # print(len(val),len(popul))
        newpopul = []  # Двумерный массив для новой популяции
        sval = sorted(val, reverse=reverse)
        # Сортируем зачения в val в зависимости от параметра reverse
        indexes = []
        for i in range(n_surv):  # Проходимся по циклу nsurv-раз (в итоге в newpopul запишется nsurv-лучших показателей)
            index = val.index(sval[i])
            indexes.append(index)
            # print(index)                                         # Получаем индекс i-того элемента sval в исходном массиве val
            newpopul.append(popul[index])

            # В новую папуляцию добавляем элемент из текущей популяции с найденным индексом
        return newpopul, sval, indexes  # Возвращаем новую популяцию (из nsurv элементов) и сортированный список

    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    one_p = epoch / 100
    n = num_popul  # задаём размер популяции
    nnew = n - n_surv
    mut = 0.9  # Количество новых (столько новых ботов создается)                                                             # Количество новых (столько новых ботов создается)
    popul = []  # Двумерный массив популяции, размерностью
    val = []  # Одномерный массив значений этих ботов
    loss = []  # значение ошибки для каждого элемента бота
    res_l = []  # результаты
    # -------------------------------------------------------------------------------
    # старт алгоритма
    # --
    # -----------------------------------------------------------------------------
    popul = []  # генерируем 0 популяцию
    if zero_bot == []:
        zero_bot = created_bot(adres_list, vol_list, mass_list, n=10)

    popul.append(zero_bot)
    for i in range(num_popul):
        popul.append(created_bot(adres_list, vol_list, mass_list, n=10))
    for it in range(epoch):
        val = []  # Пробегаемся по всем эпохам
        for i in range(num_popul):
            l = 0
            for k in range(len(popul[i])):
                # print(i,k)
                og = popul[i][k][0]
                p = popul[i][k][1]
                mas = 0
                vol = 0
                r = 0
                for j in range(len(popul[i][k][2])):
                    if ogr_list[popul[i][k][2][j]] != og and ogr_list[popul[i][k][2][j]] != 0:
                        l += 1000
                    if per_list[popul[i][k][2][j]] != p:
                        l += 100
                    # print(popul[i][k][2][j])
                    mas += sum(mass_list[popul[i][k][2][j]])
                    vol += sum(vol_list[popul[i][k][2][j]])
                    if j < len(popul[i][k][2]) - 1:
                        r += matrix_distance[popul[i][k][2][j], popul[i][k][2][j + 1]]
                if mas > predel[og][1] or vol > predel[og][0]:
                    l += 1000
                if len(popul[i][k][2]) > 12:
                    l += 10000

                l += r
            val.append(l)

            # В пилотнике ф просто берем общую ошибку
        newpopul, sval, indexes = getSurvPopul(popul, val, n_surv,
                                               0)  # Получаем новую популяцию и сортированный список значнией
        res_l.append(sval[0])
        if it % 5 == 0:
            print(it, "- Эпоха. Наименьшее расстояние пройденое всеми машинами - ", sval[0],
                  ". Наибольшее расстояние пройденое машинами-  ",
                  sval[-1])  # Выводим результат 1 лучшего и 1 худшего ботов
        mut_pop = []

        for i in range(nnew - new_mut):
            if it / one_p > 30:
                mut = 0.2
            if it / one_p > 50:
                mut = 0.1
            if it / one_p > 65:
                mut = 0.07
            if it / one_p > 80:
                mut = 0.05
            newpopul.append(created_bot(adres_list, vol_list, mass_list, n=10, k=0.2, n_add_car=10, k_ts=0.3))
            # newpopul.append(mut_gen_2(created_bot(adres_list,vol_list,mass_list,2,predel), mut))
        z = 0

        for i in range(new_mut):
            m1 = mut_gen(newpopul[i], mut)
            m2 = mut_gen_2(newpopul[i])
            newpopul.append(m1)
            newpopul.append(m2)
            z += 1
            if z > 4:
                z = 0
                # Выводим новую популяцию
        popul = newpopul

    plt.plot(res_l, label='Расстояние лучшего бота популяции на каждой эпохе')
    plt.xlabel('Значение')
    plt.xlabel('Эпоха')
    plt.legend()
    plt.show()
    return popul[0]