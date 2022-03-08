import yaml
import threading
import datetime
import time
from yaml.loader import SafeLoader
import csv

file2B = open("Log4.txt", "w")


def waitingTime(typeName, taskName, input, secs):
    ts1 = str(datetime.datetime.now())
    string = ts1 + ';' + typeName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file2B.write(string + '\n')
    time.sleep(int(secs))


noOfDefects = {}


def func(typeName, activity, name):
    global noOfDefects
    if activity['Type'] == 'Task':
        if activity['Function'] == 'TimeFunction':
            flag = True
            if 'Condition' in activity:
                condition = activity['Condition'][15:20]
                val = int(activity['Condition'][-1])
                symbol = activity['Condition'][-3]
                while condition not in noOfDefects:
                    pass
                if symbol == '>':
                    if noOfDefects[condition] < val:
                        flag = False
                if symbol == '<':
                    if noOfDefects[condition] > val:
                        flag = False
            if flag:
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Entry'
                file2B.write(string + '\n')
                waitingTime(typeName, name, activity['Inputs']['FunctionInput'], activity['Inputs']['ExecutionTime'])
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Exit'
                file2B.write(string + '\n')
            else:
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Entry'
                file2B.write(string + '\n')
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Skipped'
                file2B.write(string + '\n')
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + name + ' Exit'
                file2B.write(string + '\n')

        else:
            flag = True
            if 'Condition' in activity:
                val = int(activity['Condition'][-1])
                symbol = activity['Condition'][-3]
                condition = activity['Condition'][15:20]
                while condition not in noOfDefects:
                    if symbol == '>':
                        if noOfDefects[condition] < val:
                            flag = False
                    if symbol == '<':
                        if noOfDefects[condition] > val:
                            flag = False
                if True:
                    if flag:
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + name + ' Entry'
                        file2B.write(string + '\n')
                        filename = activity['Inputs']['Filename']
                        string = ts1 + ';' + typeName + '.' + name + ' Executing DataLoad(' + filename + ')'
                        file2B.write(string + '\n')
                        with open(filename, 'r', newline='') as fp:
                            data = csv.reader(fp)
                            d = -1
                            for _ in data:
                                d += 1
                            noOfDefects = d
                        fp.close()
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + name + ' Exit'
                        file2B.write(string + '\n')

    else:
        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Entry'
        file2B.write(string + '\n')
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
        file2B.write(string + '\n')


def seq(typeName, activities):
    global noOfDefects
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + i + ' Entry'
                file2B.write(string + '\n')
                waitingTime(typeName, i, activities[i]['Inputs']['FunctionInput'],
                            activities[i]['Inputs']['ExecutionTime'])
                ts1 = str(datetime.datetime.now())
                string1 = ts1 + ';' + typeName + '.' + i + ' Exit'
                file2B.write(string1 + '\n')

            elif activities[i]['Function'] == "DataLoad":
                flag = True
                if 'Condition' in activities[i]:
                    val = int(activities[i]['Condition'][-1])
                    symbol = activities[i]['Condition'][-3]
                    condition = activities['Condition'][15:20]
                    if symbol == '>':
                        if noOfDefects[condition] < val:
                            flag = False
                    if symbol == '<':
                        if noOfDefects[condition] > val:
                            flag = False
                if True:
                    if flag:
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + i + ' Entry'
                        file2B.write(string + '\n')
                        filename = activities[i]['Inputs']['Filename']
                        string = ts1 + ';' + typeName + '.' + i + ' Executing DataLoad(' + filename + ')'
                        file2B.write(string + '\n')
                        with open(filename, 'r', newline='') as file:
                            data = csv.reader(file)
                            count = -1
                            for _ in data:
                                count += 1
                            noOfDefects[i] = count
                        file.close()
                        ts1 = str(datetime.datetime.now())
                        string = ts1 + ';' + typeName + '.' + i + ' Exit'
                        file2B.write(string + '\n')

        if activities[i]['Type'] == 'Flow':
            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Entry'
            file2B.write(string + '\n')
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
            file2B.write(string + '\n')


with open('Milestone2B.yaml') as f:
    data4 = yaml.load(f, Loader=SafeLoader)
f.close()

for k in data4.keys():
    ts = str(datetime.datetime.now())
    s = ts + ';' + k + ' Entry'
    file2B.write(s + '\n')
    if data4[k]['Type'] == "Flow":
        if data4[k]['Execution'] == 'Sequential':
            seq(k, data4[k]['Activities'])
    ts = str(datetime.datetime.now())
    s = ts + ';' + k + ' Exit'
    file2B.write(s + '\n')

file2B.close()