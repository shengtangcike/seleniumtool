#coding=utf-8
import pymysql
class MysqlDB(object):
    # ==========封装MySQL基本操作=====================
    def __init__(self):
        # ===========读取MysqlDB.ini文件===========
        self.conn = pymysql.connect(host="192.168.1.106",
                                    port=3306,
                                    user="qtw_db_test",
                                    passwd="qtw_db_test@123",
                                    db="qtw_invest_db",)
        self.cursor = self.conn.cursor()

    # 查询,返回一条数据
    def select_return_A_data(self, select_sql):
        try:
            self.cursor.execute(select_sql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            self.close_db()
        return result


    # 查询,返回一组数据
    def select_return_datas(self, select_sql):
        try:
            self.cursor.execute(select_sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.close_db()
        return result


    # 删除
    def delete(self, del_sql):
        try:
            self.cursor.execute(del_sql)
            self.conn.commit()
        except Exception as e:
            print(e.message)
        finally:
            self.close_db()

    # 更新
    def sql_update(self, update_sql):
        try:
            self.cursor.execute(update_sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close_db()

    # 插入
    def insert(self, insert_sql):
        self.initMD()
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close_db()

            # 关闭数据库连接
    def close_db(self):
        self.conn.close()

if __name__=="__main__":
    a = MysqlDB()
    # b = a.select_return_A_data("SELECT mes_body FROM qtw_invest_db.p2p_sms_record WHERE receive_address = '15600000040' ORDER BY send_time DESC LIMIT 1;")
    b = a.select_return_A_data("SELECT * FROM qtw_invest_db.p2p_user_reg WHERE cif_account='15600000002';")
    print(b)
