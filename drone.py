from multiprocessing import Process
import client
import drone_poller


def run():
    p = Process(target=drone_poller.run)
    p.start()
    client.run()
    p.join()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('[x] quitting...')

