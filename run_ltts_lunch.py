from os import system


if __name__ == '__main__':
    system('screen -S backend')
    system('cd backend/')
    system('be_server.py')

    # be_server = system('screen -S backend')
