import pyodbc

# Function to establish a connection to the database
def DBConnection():
    # Specify the parameters required for the database connection
    server = 'localhost'
    database = 'WrestlingEloDB'
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                           SERVER=' + server + '; \
                           DATABASE=' + database +';\
                           Trusted_Connection=yes;')

    return cnxn
