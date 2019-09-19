import sys, subprocess
from taskrunner import Task, TaskRunner

if __name__ == '__main__':
    taskRunner = TaskRunner(enableHelp=True)
    taskRunner.AddTasks([
        Task(['dock-reset', 'dockreset', 'dreset'], 'defaults delete com.apple.dock; killall Dock', 'Reset the dock to default i.e. on bottom with autohide disabled.'),
        Task(['dock-autohide-delay-0', 'dockquick', 'dquick'], 'defaults write com.apple.dock autohide-delay -float 0; defaults write com.apple.dock autohide-time-modifier -float 0.5; killall Dock', 'Enable quick dock showing with disabled animations.'),
        Task(['dock-orientation-left', 'dockleft', 'dleft'],'defaults write com.apple.dock orientation -string left; killall Dock', 'Places the dock on the left side of the screen.'),
        Task(['dock-orientation-bottom', 'dockbottom', 'dbottom'], 'defaults write com.apple.dock orientation -string bottom; killall Dock', 'Places the dock on the bottom of the screen.'),
        Task(['dock-autohide-true', 'dockhide', 'dhide'], 'defaults write com.apple.dock autohide -boolean true; killall Dock', 'Enables dock auto hiding'),
        Task(['dock-autohide-false', 'docknohide', 'dnohide'], 'defaults write com.apple.dock autohide -boolean false; killall Dock', 'Enables dock auto hiding'),
    ])

    # Run the command line argument task
    try:
        taskRunner.RunTask(sys.argv[1])
    except Exception as e:
        print(e)