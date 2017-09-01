from subprocess import Popen


def switch_off():
    popen = Popen(['sudo', '/home/linaro/bluetooth_drone/touch_switch', 'off'])
    popen.wait()


def switch_on():
    popen = Popen(['sudo', '/home/linaro/bluetooth_drone/touch_switch', 'on'])
    popen.wait()
