import sys, subprocess

class Task:
    def __init__(self, name=[], script='', description=''):
        if type(name) == str:
            self.name = [name]
        else:
            self.name = name

        self.script = script
        self.description = description

class TaskRunner:
    def __init__(self, enableHelp=False, versionTask=None, defaultTask=None):
        self.tasks = []
        self.enableHelp = enableHelp

        # update version if needed
        self.versionTask = versionTask
        if self.versionTask != None: self.__updateVersion()

        # update help if enabled
        self.enableHelp = enableHelp

        # setup default task
        self.defaultTask = defaultTask

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
            self.AddTask(Task(['h', 'help'], 'echo \"' + out + '\"', 'Shows this list of commands.'), False)

    def __updateVersion(self):
        self.AddTask(self.versionTask, _TaskRunner__doUpdateHelp=True)

    def AddTask(self,task, __doUpdateHelp=True):
        if task != Task() and type(task) == Task:

            # check if command already exists
            for current_task in self.tasks:

                if type(current_task.name) == list:
                    for name in current_task.name:
                        if name == task.name or name in task.name:
                            raise Exception('A task of name \"' + name + '\" already exists.')
                elif current_task.name == task.name or current_task.name in task.name:
                    raise Exception('A task of name \"' + name + '\" already exists.')
                
            # No errors, add new task
            self.tasks.append(task)

            # update help if enabled as new task has been added
            if __doUpdateHelp: self.__updateHelp()
        else:
            raise Exception('AddTask must take a valid Task object.')

    def AddTasks(self, tasks):
        for i, task in enumerate(tasks):
            if i < len(tasks) - 1: 
                self.AddTask(task, _TaskRunner__doUpdateHelp=False)
            else: # only update help on the last task being added
                self.AddTask(task, _TaskRunner__doUpdateHelp=True)

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

        # check if default task
        if name == '' and type(self.defaultTask) == Task:
            for path in self.__execute(self.defaultTask.script):
                print(path, end="")
            return

        # find the correct task and run it
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
