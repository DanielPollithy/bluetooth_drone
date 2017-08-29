from subprocess import Popen


def switch_off():
    popen = Popen(['sudo', './touch_switch', 'off'])
    popen.wait()


def switch_on():
    popen = Popen(['sudo', './touch_switch', 'on'])
    popen.wait()
