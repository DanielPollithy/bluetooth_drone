from multiprocessing import Process
import client
import drone_poller


def run():
    p = Process(target=drone_poller.run)
    p.start()
    client.run()


if __name__ == '__main__':
    run()
