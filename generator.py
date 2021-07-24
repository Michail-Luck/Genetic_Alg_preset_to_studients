import numpy as np
import pandas as pd
import random
import math
from script import *

predel= [[5,10],[10,15]]

def created_baza(num_z=100, num_a=2, ogr_p=0.5, ogr_ts=0.1):
    #
    # Функция генерации данных для симуляции реальной задачи
    #
    # num_z    количество заказов
    # num_a      Количество адресов
    # ogr_p    коэффицент вероятности назначения грузоперевозчиков
    # ogr_ts      коэффицент вероятности наложения огранечения по типу ТС

    adres_list = ['Начало']  # список адресов
    zakaz_list = [700000000]  # список заказов
    vol_list = [0]  # список объёмов заказов
    mass_list = [0]  # список масс заказов
    time_list = [0]  # список ограничений по времени
    per_list = [0]  # список предпочтительных грузоперевозчиков
    ogr_list = [0]  # список ограничений по типу тс
    ostatok1 = num_a
    ostatok2 = num_z + 1
    for i in range(num_a):

        num_adres = random.randint(1, int(num_z / 10))
        x = num_adres - int(num_adres * 0.15) if num_adres + ostatok1 < ostatok2 else ostatok2 - ostatok1

        ostatok1 -= 1
        n = random.random()
        if n < ogr_p:
            n1 = 1
        else:
            n1 = 2
        n = random.random()
        if n < ogr_ts:
            n2 = 1
        else:
            n2 = 0
        for j in range(x):
            ostatok2 -= 1
            adres_list.append('Адрес_' + str(i + 1))
            per_list.append(n1)
            ogr_list.append(n2)
            zakaz_list.append(zakaz_list[-1] + 1)
            volume = random.uniform(0.0001, 1.0)
            vol_list.append(round(volume / 10, 4))
            mass = random.uniform(1.0, 100.0)
            mass_list.append(round(((mass) / 1000), 4))

    col = ['Адрес', 'Номера заказов', 'Масса.т', 'Объем.м3', 'Грузоперевозчик', 'Ограничение по ТС']
    df = []
    for i in range(len(mass_list)):
        df.append([adres_list[i], zakaz_list[i], mass_list[i], vol_list[i], per_list[i], ogr_list[i]])

    df_baza = pd.DataFrame(df, columns=col)
    df_baza['Номера заказов'][0] = 0
    adres_list = df_baza['Адрес'].unique().tolist()
    zakaz_list = []
    vol_list = []
    mass_list = []
    per_list = []
    ogr_list = []

    def my_fun(temp_list):
        for ele in temp_list:
            if type(ele) == list:
                my_fun(ele)
            else:
                new_list.append(ele)

    for i in range(len(adres_list)):
        per_list.append(max(df_baza['Грузоперевозчик'][df_baza['Адрес'] == adres_list[i]].tolist()))
        ogr_list.append(max(df_baza['Ограничение по ТС'][df_baza['Адрес'] == adres_list[i]].tolist()))
        zakaz_list.append(df_baza['Номера заказов'][df_baza['Адрес'] == adres_list[i]].tolist())
        new_list = []
        my_fun((df_baza['Объем.м3'][df_baza['Адрес'] == adres_list[i]].tolist()))
        vol_list.append((new_list))
        new_list = []
        my_fun((df_baza['Масса.т'][df_baza['Адрес'] == adres_list[i]].tolist()))
        mass_list.append((new_list))
    new_adr = []
    new_mass = []
    new_vol = []
    new_zak = []
    new_ogr = []
    new_per = []
    for i in range(0, len(adres_list)):
        n_p = ogr_list[i]

        # if sum(vol_list[i])>predel[n_p][1] or sum(mass_list[i])>predel[n_p][0]:
        mas = []
        vol = []
        zak = []

        for j in range(1 if zakaz_list[i] == 0 else len(zakaz_list[i])):
            if sum(mas) + df_baza['Масса.т'][df_baza['Номера заказов'] == zakaz_list[i][j]].tolist()[0] > predel[n_p][
                0] or sum(vol) + df_baza['Объем.м3'][df_baza['Номера заказов'] == zakaz_list[i][j]].tolist()[0] > \
                    predel[n_p][1]:

                new_ogr.append(ogr_list[i])
                new_per.append(per_list[i])
                new_adr.append(adres_list[i])
                new_mass.append(mas)
                new_vol.append(vol)
                new_zak.append(zak)
                mas = []
                vol = []
                zak = []

            else:
                mas.append(df_baza['Масса.т'][df_baza['Номера заказов'] == zakaz_list[i][j]].tolist()[0])
                vol.append(df_baza['Объем.м3'][df_baza['Номера заказов'] == zakaz_list[i][j]].tolist()[0])
                zak.append(zakaz_list[i][j])
                if j == len(zakaz_list[i]) - 1:
                    new_ogr.append(ogr_list[i])
                    new_per.append(per_list[i])
                    new_adr.append(adres_list[i])
                    new_mass.append(mas)
                    new_vol.append(vol)
                    new_zak.append(zak)
                    mas = []
                    vol = []
                    zak = []

    print(len(adres_list), len(mass_list), len(vol_list), len(zakaz_list), len(ogr_list), len(per_list))
    print(len(new_adr), len(new_mass), len(new_vol), len(new_zak), len(new_ogr), len(new_per))
    col = ['Адрес', 'Номера заказов', 'Масса.т', 'Объем.м3', 'Грузоперевозчик', 'Ограничение по ТС']
    df = []
    for i in range(len(new_adr)):
        df.append([new_adr[i], new_zak[i], new_mass[i], new_vol[i], new_per[i], new_ogr[i]])

    df_baza2 = pd.DataFrame(df, columns=col)
    df_baza2.loc['Номера заказов',0] = 0

    return df_baza, df_baza2
df_baza, df_baza2 = created_baza(num_z=1000, num_a=300)
adres_u_list = df_baza2['Адрес'].unique().tolist()
adres_list = df_baza2['Адрес'].values
zakaz_list = df_baza2['Номера заказов'].values
vol_list = df_baza2['Объем.м3'].values
mass_list = df_baza2['Масса.т'].values
per_list = df_baza2['Грузоперевозчик'].values
ogr_list = df_baza2['Ограничение по ТС'].values

def distan(p1, p2):  # функция рассчета расстояния между 2 точек
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


# -------------------------------------------------------------------------------
coord = []
matrix_distance = np.zeros((len(adres_u_list), len(
    adres_u_list)))  # матрица расстояний. колонки и столбцы - сами точки, значения  по ним  - расстояние между точками
for i in range(len(adres_u_list)):
    coord.append([random.uniform(-10, 8), random.uniform(-10, 8)])

for i in range(len(adres_u_list)):
    hot_dist = []
    for j in range(len(adres_u_list)):
        # if j!=i:

        x = distan(coord[i], coord[j])
        hot_dist.append(x)
    if len(hot_dist) != 0:
        matrix_distance[i] = hot_dist
print('Матрица расстояний между узлами графа(входные данные)')
# -------------------------------------------------------------------------------
matrix_distance.shape