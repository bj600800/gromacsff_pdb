# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 14:40
# @Author  : Eric_Douzhixin
# @File    : renumber_pdb.py

import os
import numpy as np

# define a function to print list content line by line
def printlines(list):
    for i in list:
        print(i)

pdbdir = 'F:\subject\\active\CBM-cellulose\gromacs\charmm-gui&cellulose-builder\\256all\crystal-2021-01-15_382020818'
pdbfile = '' #存储待重新排序的pdb文件
for file in os.listdir(pdbdir):
    if file == 'crystal.pdb':
        pdbfile = file

info = [] #存储pdb所有信息
with open(os.path.join(pdbdir, pdbfile), 'r') as text:
    for i in text:
        i = i.split()
        info.append(i)

#删除最后的END
info.pop()

#生成两个索引的数组用于迭代
chainnum = []
for i in range(22):
    i = 'M'+ str(i)
    chainnum.append(i)
''' chainnum = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 
     'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19']'''
resinum = list(range(1,13)) # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#存PDB信息到三维数组
renumber = np.ones((20,12,23), dtype=list)

# 把所有信息按照三维数组存起来（20，12，23），20条链，12个糖环，23个原子
for i in chainnum:
    for j in resinum:
        count = 0
        for line in info:
            if line[4] == str(j) and line[10] == i:
                renumber[chainnum.index(i)][resinum.index(j)][count] = line
                count += 1
renumber = renumber.tolist()

# 重新排序
with open(os.path.join(pdbdir, 'out.pdb'), 'w', newline='') as f:
    for chain in renumber:
        chain = list(filter(lambda x: x != 1, chain))
        chain = chain[::-1]
        for resi in chain:
            for atom in resi:
                if type(atom) == list:
                    atom[3] = 'BGLC'

                    a = '{:>}{: >7}{}{: <4}{:>4}{: >5}{: >12}{: >8}{: >8}{: >6}{: >6}{}{: <4}{: >2}'\
                        .format(atom[0],atom[1],'  ',atom[2],atom[3],atom[4],atom[5],atom[6],atom[7],atom[8],atom[9]
                                ,'      ',atom[10],atom[11])
                    f.writelines(a)
                    f.write('\n')

output = [] #最终完成的pdb
# 重新标号
with open(os.path.join(pdbdir, 'out.pdb'), 'r', newline='') as read:
    cont = read.readlines()
    for line in cont:
        line = line.split()
        output.append(line)

with open(os.path.join(pdbdir, 'output.pdb'), 'w', newline='') as do:
    for i, element in enumerate(output):
        element[1] = i+1
        if element[4] == '12':
            element[4] = 1
        if element[4] == '11':
            element[4] = 2
        if element[4] == '10':
            element[4] = 3
        if element[4] == '9':
            element[4] = 4
        if element[4] == '8':
            element[4] = 5
        if element[4] == '7':
            element[4] = 6
        if element[4] == '6':
            element[4] = 7
        if element[4] == '5':
            element[4] = 8
        if element[4] == '4':
            element[4] = 9
        if element[4] == '3':
            element[4] = 10
        if element[4] == '2':
            element[4] = 11
        if element[4] == '1':
            element[4] = 12
        a = '{:>}{: >7}{}{: <4}{:>4}{: >5}{: >12}{: >8}{: >8}{: >6}{: >6}{}{: <4}{: >2}' \
            .format(element[0], element[1], '  ', element[2], element[3], element[4], element[5], element[6], element[7], element[8], element[9]
                    , '      ', element[10], element[11])
        do.writelines(a)
        do.write('\n')
    do.write('END')