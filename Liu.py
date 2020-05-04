from MachineTask import MachineTask
from Task import Task

import plotly.figure_factory as ff
import numpy as np
from random import random


def order(tasksList):
    t = 0

    active = []

    ordered = []

    inactive = tasksList.copy()

    li = []

    calculateDi(inactive)

    lastMachineTask = MachineTask()

    while inactive or active:
        t += 1

        for task in inactive:
            if task.r < t:
                active.append(task)
                inactive.remove(task)

        if active:
            currentTask = getWithMinDi(active)
            if currentTask:
                currentMachineTask = MachineTask()
                currentMachineTask.name = currentTask.name
                currentMachineTask.startTime = t - 1

                if lastMachineTask.time != 0:
                    if lastMachineTask.name == currentMachineTask.name:
                        currentMachineTask = lastMachineTask
                    else:
                        ordered.append(lastMachineTask)

                currentMachineTask.time += 1
                currentTask.currentP -= 1

                if currentTask.currentP == 0:
                    removeTaskFromList(active, currentTask)
                    li.append(t - currentTask.dj)

                lastMachineTask = currentMachineTask

        if not active and not inactive and lastMachineTask != 0:
            ordered.append(lastMachineTask)

    print(li)
    print("Max Li = " + str(max(li)))
    return ordered


def removeTaskFromList(tasksList, task):
    for taskAfter in task.after:
        if contains(taskAfter.before, task):
            taskAfter.before.remove(task)
    # for taskBefore in task.before:
    #     if contains(taskBefore.after, task):
    #         taskBefore.after.remove(task)

    tasksList.remove(task)


def contains(task, searched):
    for task in task:
        if task == searched:
            return True
    return False


def calculateDi(tasksList):
    for task in tasksList:
        task.di = task.find_modified_deadline()


def getWithMinDi(tasksList):
    tasksWithNoFather = []

    for task in tasksList:
        if not task.before:
            tasksWithNoFather.append(task)
    if tasksWithNoFather:
        taskWithMinDi = tasksWithNoFather[0]

        for task in tasksWithNoFather:
            if task.di < taskWithMinDi.di:
                taskWithMinDi = task
        return taskWithMinDi
    return None


def link(task1, task2):
    task1.after.append(task2)

    task2.before.append(task1)


def graph(tasksList):
    df = []
    colors = []
    r = lambda: int(random() * 255)

    for task in tasksList:
        df.append(dict(
            Task=str(1),
            Start=str(task.startTime),
            Finish=str(task.startTime + task.time),
            Id=task.name))
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
    fig = ff.create_gantt(df, colors=colors, index_col='Id', task_names='Id', group_tasks=True)
    fig.update_layout(xaxis_showgrid=True)
    fig.update_yaxes(title_text='aaaaaaaaa')
    fig.update_xaxes(title_text='Time')
    fig.layout.xaxis.rangeselector = None
    fig.layout.xaxis.type = 'linear'
    fig.show()


if __name__ == "__main__":
    t1 = Task("T1", 3, 0, 4)
    t2 = Task("T2", 2, 4, 6)
    t3 = Task("T3", 2, 2, 8)
    t4 = Task("T4", 1, 5, 15)
    t5 = Task("T5", 4, 6, 10)
    t6 = Task("T6", 1, 15, 20)
    t7 = Task("T7", 2, 13, 25)

    link(t1, t3)
    link(t3, t5)
    link(t5, t7)
    link(t2, t4)
    link(t4, t6)
    link(t4, t5)
    link(t6, t7)

    tasks = [t1, t2, t3, t4, t5, t6, t7]

    orderedTasks = order(tasks)

    graph(orderedTasks)

    # p
    # 3
    # 2
    # 2
    # 1
    # 4
    # 1
    # 2
    #     r
    #     0
    #     4
    #     2
    #     5
    #     6
    #     15
    #     13
    #         dj
    #         4
    #         6
    #         8
    #         15
    #         10
    #         20
    #         25
