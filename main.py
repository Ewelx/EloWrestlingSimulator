import BDConnection
import MainWindows

def main():
    end = False
    cnxn = BDConnection.BDConnection()
    MainWindows.createInterface()
    while(end == False):
        print('test')
    cnxn.close()

main()