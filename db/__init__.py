import MySQLdb
from . import config


class Database:
    is_initiated_db = False

    instance = None

    @staticmethod
    def query(qstr, ret_lastid=False):
        """

        :param qstr:
        :param ret_lastid:
        :return: id, result or result (depends on ret_lastid)
        """
        db = MySQLdb.connect(host=config.DBADDR, user=config.DBUSER, passwd=config.DBPASS, db=config.DBNAME,
                             charset='utf8')

        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(qstr)
        db.commit()
        all = cursor.fetchall()
        lastrowid = cursor.lastrowid
        cursor.close()
        if ret_lastid:
            return lastrowid, all
        else:
            return all

    def table_exists(self, name) -> bool:
        rets = Database.query("SHOW TABLES LIKE '%s'" % name)
        return len(rets) > 0

    def select(self, table, fields='*', where='1'):
        """
        Select data from table
        :param table:  table name
        :type table: str

        :param fields: fields
        :type fields: str


        :param where: condition
        :type where: str

        :return: tuple
        """
        return Database.query("SELECT {} FROM {} WHERE {};".format(fields, table, where))

    @staticmethod
    def prepare(*args) -> tuple:
        ret = ()
        for arg in args:
            if type(arg) is int:
                ret += (arg,)
            elif type(arg) is int:
                ret += (arg,)
            elif type(arg) is str:
                ret += ('\'' + MySQLdb.escape_string(arg).decode("utf-8") + '\'',)
            elif arg is None:
                ret += ('NULL',)

        return ret

    def insert(self, table, data) -> int:
        '''
        Inser data into table
        :param table: str, table name
        :param data: dict, data to insert.
        :return: int, last inserted id
        '''
        keys = ()
        values = ()

        for k in data:
            keys += (k,)
            values += (data[k],)

        k = ", ".join('`' + str(i) + '`' for i in keys)
        v = ", ".join(str(i) for i in self.prepare(*values))

        q = "INSERT INTO `{}` ({}) VALUES ({});".format(table, k, v)
        id, data = Database.query(q, True)

        return id

    def update(self, table, data, where) -> int:
        '''
        Make update query.
        :param table: str, table
        :param data: dict, new data
        :param where: str, where
        :return:
        '''
        udata = []

        for k in data:
            udata.append("{}={}".format(*(k,) + self.prepare(data[k])))

        q = "UPDATE `{}` SET {} WHERE {};".format(table, ",".join(udata), where)
        id, data = Database.query(q, True)

        return id


class NotFoundException(Exception):
    pass
