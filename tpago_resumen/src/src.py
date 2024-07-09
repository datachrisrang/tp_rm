import pandas as pd
from datetime import datetime
from lib.config import *
import time
from pyhive import hive
import puretransport

class tpago_resumen_mensual:
    '''
    Módulo para elaborar un archivo txt con todos los clientes que han realizado alguna transacción por Tpago 
    en los últimos 6 meses. 
    '''
    def __init__(self):
        # Definición de variables globales
        self.logger = logger_init()
        self.config = config_init()
        self.outputLocalPath = self.config.get('PATH', 'outputlocalpath')
        self.hoy =  datetime.now().strftime('%d%m%Y')
        self.ConfQry=self.config['QUERY']
        self.conndb=self.config['connect.bigdata']
        self.hive_con = None
        self.tpago_resumen_mensual = None
        

    def Connection(self,user,password,db,host,port):
     try:
         self.logger.info('============ Conectando a la Base de Datos ' )
         transport = puretransport.transport_factory(host=host,
                                             port=port,
                                             username=user,
                                         password=password)
         hive_con= hive.connect(username=user, thrift_transport=transport,database=db)
         self.logger.info('============ Conexion Exitosa ' )
     
         return(hive_con)
     except Exception as err:
         self.logger.error(f'Error Conectando a la Base de Datos: {err}')
         raise SystemExit()

    def DataExtraction(self,query,hive_con):
        
        start = time.time()
        self.logger.info('============ Ejecutando Query  ...')
        dataframe=pd.read_sql(query,hive_con)
        finish = time.time()
        self.logger.info('============ Tiempo de Ejecución de Query: ' + str(round(((finish-start)/60),2)) + 'min')
        if len(dataframe)==0:
            self.logger.error('El area de no contiene informacion para la fecha: ' )
            raise Exception('El area de no contiene informacion para la fecha: ' )
            #failed_email(date, err)
            sys.exit()
            
        else:      
            return(dataframe)
    
    def DataLoad(self):
        self.tpago_resumen_mensual = self.DataExtraction(self.ConfQry['tpago_resumen_mensual'],self.hive_con)
    
    def DataTransform(self):
        self.logger.info('============ Transformando datos  ...')
        start = time.time()

        # Formatear la salida SIN encabezado y con "|" como separador
        self.tpago_resumen_mensual = self.tpago_resumen_mensual.to_string(header=False, index=False, sep='|')  

        finish = time.time()
        self.logger.info('============ Tiempo de Transformación de datos: ' + str(round(((finish-start)/60),2)) + 'min')

    def DataSave(self):
        self.logger.info('============ Guardando archivo txt  ...')
        try:
            start = time.time()
            # Guardar como archivo TXT
            with open(f'{self.outputLocalPath}tpago_resumen_mensual_{self.hoy}.txt', 'w') as f:
                f.write(self.tpago_resumen_mensual) 
            self.logger.info('============ Archivo Exportado Satisfactoriamente.')
            finish = time.time()
            self.logger.info('============ Tiempo de exportacion: ' + str(round(((finish-start)/60),2)) + 'min')
        except Exception as err:
            self.logger.error(f'============ No se pudo exportar el archivo solicitado. {err}')   