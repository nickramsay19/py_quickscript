import sys
from taskrunner import Task, TaskRunner
    
if __name__ == '__main__':

    # setup taskrunner
    taskRunner = TaskRunner(
        enableHelp = True, 
        defaultTask = Task('default', 'qs version && printf \"\n\" && qs help'), 
        versionTask = Task(['v', 'version'], 'echo \"QuickScript Version 1.3\nCreated by Nicholas Ramsay \"', 'Shows the current QuickScript version.')
    )

    # get tasks from file and add to taskRunner
    with open('tasks.csv', 'r') as f:
        for l in f.readlines(0):
            segments = l.split(', ')
            taskRunner.AddTask(Task(segments[0].split(' '), segments[1], segments[2]))


    # Run the command line argument task
    try:
        if len(sys.argv[1:]) < 1:
            taskRunner.RunTask('')
        else:
            for arg in sys.argv[1:]:
                taskRunner.RunTask(arg)
            
    except Exception as e:
        print('\033[91m' + str(e) + '\033[0m\n')
        taskRunner.RunTask('help')