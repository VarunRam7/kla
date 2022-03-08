import yaml
import threading
import datetime
import time
from yaml.loader import SafeLoader
import csv

file2A = open("LogFile1.txt", "w")


def waitingTime(typeName, taskName, input, secs):
    ct1 = str(datetime.datetime.now())
    string = ct1 + ';' + typeName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file2A.write(string + '\n')
    time.sleep(int(secs))


noOfDefects = -1


def func(typeName, activity, name):
    global noOfDefects
    if activity['Type'] == 'Task':
        if activity['Function'] == 'TimeFunction':
            flag = True
            if 'Condition' in activity:
                val = int(activity['Condition'][-1])
                sign = activity['Condition'][-3]
                if sign == '>':
                    if noOfDefects < val:
                        flag = False
                if sign == '<':
                    if noOfDefects > val:
                        flag = False
            if flag:
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Entry'
                file2A.write(string + '\n')
                waitingTime(typeName, name, activity['Inputs']['FunctionInput'], activity['Inputs']['ExecutionTime'])
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Exit'
                file2A.write(string + '\n')
        else:
            flag = True
            if 'Condition' in activity:
                val = int(activity['Condition'][-1])
                sign = activity['Condition'][-3]
                if sign == '>':
                    if noOfDefects < val:
                        flag = False
                if sign == '<':
                    if noOfDefects > val:
                        flag = False
            if True:
                if flag:
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + typeName + '.' + name + ' Entry'
                    file2A.write(string + '\n')
                    filename = activity['Inputs']['Filename']
                    string = ct1 + ';' + typeName + '.' + name + ' Executing DataLoad(' + filename + ')'
                    file2A.write(string + '\n')
                    with open(filename, 'r', newline='') as fp:
                        data = csv.reader(file)
                        for _ in data:
                            noOfDefects += 1
                    fp.close()
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + typeName + '.' + name + ' Exit'
                    file2A.write(string + '\n')

    else:
        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Entry'
        file2A.write(string + '\n')
        if activity['Execution'] == 'Sequential':
            seq(typeName + '.' + name, activity['Activities'])
        if activity['Execution'] == 'Concurrent':
            threads = []
            for j in activity['Activities'].keys():
                t = threading.Thread(target=func, args=[typeName + '.' + name, activity['Activities'][j], j])
                threads.append(t)
                t.start()
            for j in range(len(threads)):
                threads[j].join()
        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Exit'
        file2A.write(string + '\n')


def seq(typeName, activities):
    global noOfDefects
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + i + ' Entry'
                file2A.write(string + '\n')
                waitingTime(typeName, i, activities[i]['Inputs']['ExecutionTime'],
                            activities[i]['Inputs']['FunctionInput'])
                ct2 = str(datetime.datetime.now())
                string1 = ct2 + ';' + typeName + '.' + i + ' Exit'
                file2A.write(string1 + '\n')

            elif activities[i]['Function'] == "DataLoad":
                flag = True
                if 'Condition' in activities[i]:
                    val = int(activities[i]['Condition'][-1])
                    symbol = activities[i]['Condition'][-3]
                    if symbol == '>':
                        if noOfDefects < val:
                            flag = False
                    if symbol == '<':
                        if noOfDefects > val:
                            flag = False
                if True:
                    if flag:
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + i + ' Entry'
                        file1.write(string + '\n')
                        filename = activities[i]['Inputs']['Filename']
                        string = ts1 + ';' + typeName + '.' + i + ' Executing DataLoad(' + filename + ')'
                        file1.write(string + '\n')
                        with open(filename, 'r', newline='') as file:
                            data = csv.reader(file)
                            for row in data:
                                noOfDefects += 1
                        file.close()
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + i + ' Exit'
                        file2A.write(string + '\n')

        if activities[i]['Type'] == 'Flow':
            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Entry'
            file2A.write(string + '\n')
            if activities[i]['Execution'] == 'Sequential':
                seq(typeName + '.' + i, activities[i]['Activities'])
            elif activities[i]['Execution'] == 'Concurrent':
                threads = []
                for j in activities[i]['Activities'].keys():
                    t = threading.Thread(target=func, args=[typeName + '.' + i, activities[i]['Activities'][j], j])
                    threads.append(t)
                    t.start()
                for j in range(len(threads)):
                    threads[j].join()

            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Exit'
            file2A.write(string + '\n')


with open('Milestone2A.yaml') as f:
    data3 = yaml.load(f, Loader=SafeLoader)
f.close()

for k in data3.keys():
    ts = str(datetime.datetime.now())
    s = ts + ';' + k + ' Entry'
    file2A.write(s + '\n')
    if data3[k]['Type'] == "Flow":
        if data3[k]['Execution'] == 'Sequential':
            seq(k, data3[k]['Activities'])
    ts = str(datetime.datetime.now())
    s = ts + ';' + k + ' Exit'
    file2A.write(s + '\n')

file2A.close()
