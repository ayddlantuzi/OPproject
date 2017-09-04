import configparser
import codecs


def getClientConfig():
    configINI = configparser.SafeConfigParser()
    configINI.read('config.ini')
    print('all sections:',configINI.sections())
    for ini in configINI.sections():
        print(configINI.get(ini,'ip')+':'+configINI.get(ini,'port'))


def getServerConfig():
    pass
    


if __name__ =='__main__':
    getConfig()
    