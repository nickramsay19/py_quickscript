import sys, subprocess

# Define some simple console output themes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''
    --- Custom Task Runner Utilities ---
'''
class Task:
    def __init__(self,name=[],script='',description=''):
        if type(name) == str:
            self.name = [name]
        else:
            self.name = name

        self.script = script
        self.description = description

class TaskRunner:
    def __init__(self, enableHelp=False):
        self.tasks = []
        self.enableHelp = enableHelp

        # update help if enabled
        self.enableHelp

    def __updateHelp(self):
        if self.enableHelp:

            # Generate Output
            out = ''
            for task in self.tasks:

                # for each task, add a new line with names and description
                
                ''' 
                    (1) Show the Task Name
                    - Check if task has multinames and loop through them
                    - Otherwise print the only option
                '''
                if type(task.name) == list:
                    for i, name in enumerate(task.name):
                        if i < len(task.name) - 1:
                            out += bcolors.OKGREEN + name + bcolors.ENDC + ' | '
                        else:
                            out += bcolors.OKGREEN + name + bcolors.ENDC
                else:
                    out += name

                '''
                    (2) Show Description
                '''
                out += ' --> ' + (task.description, '...')[task.description == '']

                '''
                    (3) Add new Line
                '''
                out += '\n'

            # Update with new output
            self.RemoveTask('help', False)
            self.AddTask(Task(['h', 'help'], 'echo \"' + out + '\"'), False)

    def AddTask(self,task, __doUpdateHelp=True):
        if task != Task() and type(task) == Task:
            self.tasks.append(task)

            # update help if enabled as new task has been added
            if __doUpdateHelp: self.__updateHelp()
        else:
            raise Exception('AddTask must take a valid Task object.')

    def AddTasks(self, tasks):
        # add proper error checking
        for task in tasks:
            self.AddTask(task)

    def RemoveTask(self, name='', __doUpdateHelp=True):
        if type(name) == list:
            raise Exception('name must be of type str not list.')

        for task in self.tasks:
            if type(task.name) == list:
                for alias in task.name:
                    if alias == name:
                        self.tasks.remove(task)
                        if __doUpdateHelp: self.__updateHelp()
                        return
            elif task.name == name:
                self.tasks.remove(task)
                if __doUpdateHelp: self.__updateHelp()
                return
        return


    def RunTask(self,name):
        for task in self.tasks:
            if task.name == name or name in task.name:
                for path in self.__execute(task.script):
                    print(path, end="")
                return
        else:
            raise Exception('The script \'' + name + '\' could not be found.')

    def __execute(self,cmd):
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
