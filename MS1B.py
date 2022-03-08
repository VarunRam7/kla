import yaml
import threading
import time
import datetime
from yaml.loader import SafeLoader

file1B = open("Log2.txt", "w")


def waitingTime(typeName, taskName, input, secs):
    ct1 = str(datetime.datetime.now())
    string = ct1 + ';' + typeName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file1B.write(string + '\n')
    time.sleep(int(secs))


def seq(typeName, activities):
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + i + ' Entry'
                file1B.write(string + '\n')
                waitingTime(typeName, i, activities[i]['Inputs']['FunctionInput'], activities[i]['Inputs']['ExecutionTime'])
                ts2 = str(datetime.datetime.now())
                string1 = ts2 + ';' + typeName + '.' + i + ' Exit'
                file1B.write(string1 + '\n')

        if activities[i]['Type'] == 'Flow':
            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Entry'
            file1B.write(string + '\n')
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
            file1B.write(string + '\n')


def func(typeName, activity, name):
    if activity['Type'] == 'Task':
        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Entry'
        file1B.write(string + '\n')
        waitingTime(typeName, name, activity['Inputs']['FunctionInput'], activity['Inputs']['ExecutionTime'])
        ts2 = str(datetime.datetime.now())
        string1 = ts2 + ';' + typeName + '.' + name + ' Exit'
        file1B.write(string1 + '\n')

    else:

        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Entry'
        file1B.write(string + '\n')
        if activity['Execution'] == 'Sequential':
            seq(typeName + '.' + name, activity['Activities'])
        ts1 = str(datetime.datetime.now())
        string = ts1 + ';' + typeName + '.' + name + ' Exit'
        file1B.write(string + '\n')


with open('Milestone1B.yaml') as f:
    data2 = yaml.load(f, Loader=SafeLoader)
f.close()

for k in data2.keys():
    timestamp = str(datetime.datetime.now())
    s = timestamp + ';' + k + ' Entry'
    file1B.write(s + '\n')
    if data2[k]['Type'] == "Flow":
        if data2[k]['Execution'] == 'Sequential':
            seq(k, data2[k]['Activities'])
    timestamp = str(datetime.datetime.now())
    s = timestamp + ';' + k + ' Exit'
    file1B.write(s + '\n')

file1B.close()
