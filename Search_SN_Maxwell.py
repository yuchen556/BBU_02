# Search SN, if the sn existed in machistory table, then return the 1st row number
import pymysql

# Function description: deal with the scanned SN, to decide from which table to fetch MAC address
# There are two tables: macinfo, machistory
# If the SN was tested, fetch from machistory table
# If the SN has not been tested, fetch from macinfo table, get 7 mac addresses.


class fetch_MAC:
    def __init__(self, logname, SN, mysql_host, mysql_user, mysql_password, mysql_database):
        self.SN = SN
        self.host = mysql_host
        self.user = mysql_user
        self.password = mysql_password
        self.database = mysql_database
        self.logname = logname

    def search_db_sn(self):

        with open(self.logname, 'a+') as f:
            f.write("\r\rstart fetch MAC \r")
        # query0: search the scanned sn is existed in mac_spinel table or not
        query0 = "SELECT * FROM machistory WHERE mac_status = '%s'" % self.SN
        # query01: search the free in the mac_spinel table or not
        query01 = "SELECT * FROM macinfo WHERE mac_status = 'free'"
        # print(self.SN)
        # print(type(self.SN))

        # try:
        mydb = pymysql.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
        mycursor = mydb.cursor()

        # get all the rowcount of this sn
        mycursor.execute(query0)
        result_query0_all = mycursor.fetchall()
        print('result_query0_all is: ', result_query0_all)

        # print(2, self.SN, mycursor.rowcount)

        # for x in result_query0_all:
        #     print(x[1])

        # mycursor.rowcount = 0: if there isn't the sn in machistory table, fetch 7 free mac address from macinfo table;
        if mycursor.rowcount == 0:
            global sn_x0
            with open(self.logname, 'a+') as f:
                f.write("This SN is new one, need fetch new mac_address \r")
            # print("This SN is new one.")
            # print(query01)
            mycursor.execute(query01)
            result_query01_7 = mycursor.fetchmany(7)
            for sn_x0 in result_query01_7:
                print(sn_x0[1])
                with open(self.logname, 'a+') as f:
                    f.write("fetch mac_address: %s \r" % sn_x0[1])

            # insert the 7 mac addresses into machistory.
            mydb = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database)
            mycursor = mydb.cursor()
            # print("test123")

            for sn_x0 in result_query01_7:
                # print("test111")
                query_insert = "INSERT INTO machistory (mac_address, mac_status, project_name)" \
                               " VALUES ('{0:s}', '{1:s}', 'bbu')".format(
                    sn_x0[1], self.SN)
                # print(query_insert)
                mycursor.execute(query_insert)

            mydb.commit()

            for sn_x0 in result_query01_7:
                # print("delete")
                query_delete = "delete from macinfo where mac_address = '{0:s}' ".format(sn_x0[1])
                # print(query_delete)
                mycursor.execute(query_delete)

            mydb.commit()

            #     query11 = " UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d} ".format(inter_sn, sn_x0)
            #     mycursor.execute(query11)

            # for sn_x0 in range(result_query1_int, result_query1_int+7):
            #     query11 = " UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d} ".format(inter_sn, sn_x0)
            #     mycursor.execute(query11)

            # mydb.commit()
            # print(sn_x0)
            return result_query01_7

        # mycursor.rowcount != 0: fetch 7 mac address from machistory which with the sn;
        else:
            print("This SN has been tested before!")
            #
            mydb = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database)
            mycursor = mydb.cursor()

            # get the 1st row # of this sn
            mycursor.execute(query0)
            result_query0_one = mycursor.fetchone()
            result_query0_int = result_query0_one[0]

            print(3, result_query0_one)
            print(4, result_query0_int)

            # mydb = mysql.connector.connect(
            #     host="localhost",
            #     user="root",
            #     passwd="Hoping123",
            #     database="ftdb")
            # mycursor = mydb.cursor()
            #
            # for sn_x1 in range(result_query0_int, result_query0_int+7):
            #     query12 = " UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d} ".format(inter_sn, sn_x1)
            #     mycursor.execute(query12)
            #
            mydb.commit()
            return ('No need to fetch MAC')
        # except:
        #     with open(self.logname, 'a+') as f:
        #         f.write("Operate mysql db error \r")
        #     return('FAIL')
        # finally:
        #     # mycursor.close()
        #     # mydb.close()
        #     with open(self.logname, 'a+') as f:
        #         f.write("Fetched the db row number and Get Mac address \r")
        #     # print("Fetched the db row number and Get Mac address")

    # search free mac address quantity, which dwell in ftdb-macinfo table;

    def search_free_mac(self):
        # query01: search the free in the mac_spinel table or not
        # internal_free = "free"
        internal_free = self.SN

        query01 = "SELECT * FROM machistory WHERE mac_status = '{0:s}'".format(internal_free)

        try:
            mydb = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database)
            mycursor = mydb.cursor()


            # get all the rowcount of this sn
            mycursor.execute(query01)
            result_query0_all = mycursor.fetchall()
            available_mac = int(mycursor.rowcount)
            with open(self.logname, 'a+') as f:
                f.write("Rest MAC address number is: %d \r" % available_mac)
            # print(available_mac)
            return available_mac

        except:
            print("operate mysql db error")
        finally:
            # mycursor.close()
            # mydb.close()
            print("Fetched the db row number and Get Mac address")

    # search_free_mac()
