from os import system


if __name__ == '__main__':
    system('screen -S backend python3 be_server.py &')
    system('screen -r backend')
    system('cd backend/')
    system('python3 be_server.py &')



    # be_server = system('screen -S backend')
