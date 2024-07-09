from src.src import tpago_resumen_mensual
from time import time

# Tiempo de inicio 
startTime = time()
if __name__ == '__main__':
    # Instanciar la clase que procesa los archivos de transaciones Tpago mensual
    funcion = tpago_resumen_mensual()

    funcion.hive_con = funcion.Connection(funcion.conndb['UserDB'],funcion.conndb['PasswdDB'],funcion.conndb['DataBaseNanme'],funcion.conndb['host'],funcion.conndb['port'])
    funcion.DataLoad()
    funcion.DataTransform()
    funcion.DataSave()
    
    funcion.logger.info(f'El tiempo de ejecucion fue: {round((time() - startTime)/60,2)} min.')
