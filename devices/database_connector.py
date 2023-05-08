import mysql.connector

class DatabaseConnector():
    "This class will add the received values into the database."

    def _init_connection(self):
        "This class will init connection to the database."

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fiwareuser",
            database="fiware_project"
        )
        self.cursor = self.mydb.cursor()

    def _close_connection(self):
        "This class will close the connection to the database."

        self.mydb.close()

    def insert_into_real_values(self, data):
        "This class will insert the given data into the table real_values"

        self._init_connection()

        insert_real_value_query = ('INSERT INTO real_values '
        + '(temperature, et0, pluviometry, relativehumidity, soilmoisturetotal, '
        + 'soiltemperature, winddirection, windspeed, t_hour, t_day, t_month, t_year, t_epoch)'
        + 'VALUES (%(temperature)s, %(et0)s, %(pluviometry)s, %(relativehumidity)s, %(soilmoisturetotal)s, '
        + '%(soiltemperature)s, %(winddirection)s, %(windspeed)s, %(t_hour)s, %(t_day)s, %(t_month)s, %(t_year)s, %(t_epoch)s)'
        )

        self.cursor.execute(insert_real_value_query, data)

        self.mydb.commit()

        self._close_connection()

    def insert_into_predicted_values(self, data):
        "This class will insert the given data into the table predicted_values"

        self._init_connection()

        insert_real_value_query = ('INSERT INTO predicted_values '
        + '(temperature, et0, pluviometry, relativehumidity, soilmoisturetotal, '
        + 'soiltemperature, winddirection, windspeed, t_hour, t_day, t_month, t_year, t_epoch)'
        + 'VALUES (%(temperature)s, %(et0)s, %(pluviometry)s, %(relativehumidity)s, %(soilmoisturetotal)s, '
        + '%(soiltemperature)s, %(winddirection)s, %(windspeed)s, %(t_hour)s, %(t_day)s, %(t_month)s, %(t_year)s, %(t_epoch)s)'
        )

        self.cursor.execute(insert_real_value_query, data)

        self.mydb.commit()

        self._close_connection()
