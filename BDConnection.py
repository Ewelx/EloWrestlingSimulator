import pyodbc

def BDConnection():
    # Paramètres de connexion
    server = 'localhost'
    database = 'WrestlingEloDB'
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                           SERVER=' + server + '; \
                           DATABASE=' + database +';\
                           Trusted_Connection=yes;')

    return cnxn
