import yaml
import time
import datetime
from yaml.loader import SafeLoader

file1A = open("Log.txt", "w")


def waitingTime(typeName, taskName, input, secs):
    ts = str(datetime.datetime.now())
    string = ts + ';' + typeName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file1A.write(string + '\n')
    time.sleep(int(secs))


def seq(typeName, activities):
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ts1 = str(datetime.datetime.now())
                string = ts1 + ';' + typeName + '.' + i + ' Entry'
                file1A.write(string + '\n')
                waitingTime(typeName, i, activities[i]['Inputs']['FunctionInput'], activities[i]['Inputs']['ExecutionTime'])
                ts2 = str(datetime.datetime.now())
                string1 = ts2 + ';' + typeName + '.' + i + ' Exit'
                file1A.write(string1 + '\n')

        if activities[i]['Type'] == 'Flow':
            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Entry'
            file1A.write(string + '\n')
            seq(typeName + '.' + i, activities[i]['Activities'])
            ts1 = str(datetime.datetime.now())
            string = ts1 + ';' + typeName + '.' + i + ' Exit'
            file1A.write(string + '\n')


with open('Milestone1A.yaml') as f:
    data1 = yaml.load(f, Loader=SafeLoader)
f.close()

with open('Milestone1B.yaml') as f:
    data2 = yaml.load(f, Loader=SafeLoader)
f.close()

for i in data1.keys():
    timestamp = str(datetime.datetime.now())
    st = timestamp + ';' + i + ' Entry'
    file1A.write(st + '\n')
    if data1[i]['Type'] == "Flow":
        if data1[i]['Execution'] == 'Sequential':
            seq(i, data1[i]['Activities'])
    timestamp = str(datetime.datetime.now())
    st = timestamp + ';' + i + ' Exit'
    file1A.write(st + '\n')