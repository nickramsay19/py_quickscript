import sys
from taskrunner import Task, TaskRunner

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


if __name__ == '__main__':

    defaultTask = Task('default', 'qs version && printf \"\n\" && qs help')
    versionTask = Task(['v', 'version'], 'echo \"QuickScript Version 1.3\nCreated by Nicholas Ramsay \"', 'Shows the current QuickScript version.')

    taskRunner = TaskRunner(enableHelp=True, defaultTask=defaultTask, versionTask=versionTask)
    taskRunner.AddTasks([
        Task(['dock-reset', 'dockreset', 'dreset'], 'defaults delete com.apple.dock; killall Dock', 'Reset the dock to default i.e. on bottom with autohide disabled.'),
        Task(['dock-autohide-delay-0', 'dockquick', 'dquick'], 'defaults write com.apple.dock autohide-delay -float 0; defaults write com.apple.dock autohide-time-modifier -float 0.5; killall Dock', 'Enable quick dock showing with disabled animations.'),
        Task(['dock-orientation-left', 'dockleft', 'dleft'],'defaults write com.apple.dock orientation -string left; killall Dock', 'Places the dock on the left side of the screen.'),
        Task(['dock-orientation-right', 'dockright', 'dright'],'defaults write com.apple.dock orientation -string right; killall Dock', 'Places the dock on the right side of the screen.'),
        Task(['dock-orientation-bottom', 'dockbottom', 'dbottom'], 'defaults write com.apple.dock orientation -string bottom; killall Dock', 'Places the dock on the bottom of the screen.'),
        Task(['dock-autohide-true', 'dockhide', 'dhide'], 'defaults write com.apple.dock autohide -boolean true; killall Dock', 'Enables dock auto hiding.'),
        Task(['dock-autohide-false', 'dockshow', 'dshow'], 'defaults write com.apple.dock autohide -boolean false; killall Dock', 'Enables dock auto hiding.'),
    ])

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