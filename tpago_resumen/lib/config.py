import configparser
import logging, logging.config

def config_init(fileName: str = 'config/config.ini'):
    '''
        Inicializa el archivo config para ser utilizado en el proyecto 

        Parámetros:

        filename: str
            Ruta o nombre del archivo del archivo config.ini
    '''
    config = configparser.ConfigParser()
    config.read(fileName)
    return config

def logger_init(fileName: str = 'config/log.ini', loggerName: str = 'dev'):
    '''
        Inicializa el archivo log para ser utilizado en el proyecto y recopilar los logs.

        Parámetros:

        filename: str
            Ruta o nombre del archivo del archivo log.ini
        loggerName: str
            Nombre del logger a utilizar.
    '''
    logging.config.fileConfig(fileName)
    logger = logging.getLogger(loggerName)
    return logger

__all__ = ['config_init', 'logger_init']