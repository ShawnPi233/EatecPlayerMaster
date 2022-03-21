import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from Ui_Database import Ui_MainWindow
import jaydebeapi
import random
import qtmodern
import time
class DBMS(QMainWindow,Ui_MainWindow):
    temp = ''
    dbopen = False
    functionMode = 0
    # 0 无功能
    # 1 添加用户
    # 2 修改VIP状态
    # 3 修改VIP有效期
    # 4 修改管理员状态
    # 5 删除用户
    def __init__(self,parent=None):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.b_run.clicked.connect(self.run)
        self.b_view_data.clicked.connect(self.view_data)
        self.b_add_row.clicked.connect(self.add_row_data)
        self.b_delete_row.clicked.connect(self.del_row_data)
        self.b_modifyvip.clicked.connect(self.altervip)
        self.b_modifyenddate.clicked.connect(self.altervipdate)
        self.b_modifyadmin.clicked.connect(self.alteradmin)
        self.b_close.clicked.connect(self.close)
        self.b_refresh.clicked.connect(self.refresh)
        self.setWindowTitle("数据管理")
        self.setWindowIcon(QIcon(r"icon.png"))  # 图标添加

    def connectdb(self):
            url = 'jdbc:postgresql://192.168.195.129:26000/eatecuser'
            user = 'dbuser'
            password = 'Bigdata@123'
            # password = 'Gauss#3demo'
            print("正在连接数据库，请稍后...")
            conn = jaydebeapi.connect('org.postgresql.Driver', url, [user, password], '.\postgresql-42.3.1.jar')
            print("数据库已连接")
            self.dbopen = True
            return conn

    # 浏览数据
    def view_data(self):
        try:
            timecount=0
            db = self.connectdb()
            curs = db.cursor()
            curs.execute("SELECT * FROM eatecuser.users")
            data = curs.fetchall()
            model = QStandardItemModel()
            model.setHorizontalHeaderItem(0,QStandardItem("用户名"))
            model.setHorizontalHeaderItem(1, QStandardItem("密码"))
            model.setHorizontalHeaderItem(2, QStandardItem("激活码"))
            model.setHorizontalHeaderItem(3, QStandardItem("播放时间"))
            model.setHorizontalHeaderItem(4, QStandardItem("VIP"))
            model.setHorizontalHeaderItem(5, QStandardItem("VIP有效期"))
            model.setHorizontalHeaderItem(6, QStandardItem("管理员"))
            model.setHorizontalHeaderItem(7, QStandardItem("邮箱"))
            for i in range(0,len(data)):
                for j in range(0,len(data[i])):
                    model.setItem(i,j,QStandardItem(str(data[i][j])))
                if data[i][3]:
                    timecount=timecount+data[i][3]
            self.table_widget.setModel(model)
            self.table_widget.setColumnWidth(0,80)
            self.table_widget.setColumnWidth(1, 80)
            self.table_widget.setColumnWidth(2, 80)
            self.table_widget.setColumnWidth(3, 80)
            self.table_widget.setColumnWidth(4, 50)
            self.table_widget.setColumnWidth(5, 80)
            self.table_widget.setColumnWidth(6, 60)
            self.l_usercount.setText(str(len(data))+"人")
            self.l_timecount.setText(str(timecount//3600)+"时"+str(timecount%60)+"分"+str(timecount%3600)+"秒")
            db.close()
            self.dbopen=False
        except Exception:
            QMessageBox.warning(self, "数据库连接失败", "数据库连接失败，请检查网络连接！")

    # 执行数据库操作
    def run(self):
        try:
            db = self.connectdb()
            curs = db.cursor()
            nametext = self.name_modifytext.text()
            pwtext = self.pw_modifytext.text()
            viptext = self.vip_modifytext.text()
            datetext = self.date_modifytext.text()
            admintext = self.adm_modifytext.text()

            if self.functionMode==0:
                QMessageBox.warning(self,"提示","请先选择左侧功能")
            else:
                if nametext == '':
                    QMessageBox.warning(self, "警告", "用户名无法为空")
                    return  # 如果用户名为空不再往下执行
                # 增
                if self.functionMode==1:
                    if pwtext=='':
                        QMessageBox.warning(self, "警告", "密码无法为空")
                        return
                    else:
                        ran_str = ''.join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 8))  # 产生随机激活码
                        curs.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(nametext))
                        temp = curs.fetchone()
                        if temp:#判断用户是否重名
                            QMessageBox.warning(self,"警告","已存在该用户")
                        else:
                            curs.execute("INSERT INTO eatecuser.users(user_name,user_password,user_cdkey) VALUES ('{}','{}','{}')"
                                         .format(nametext, pwtext, ran_str))
                            QMessageBox.about(self,"","新增用户成功")
                # 改vipstate
                elif self.functionMode==2:
                    try:
                        curs.execute("UPDATE eatecuser.users"
                                     "SET is_vip='{}'"
                                     "WHERE user_name='{}'".format(viptext,nametext))
                        succ=True
                    except:
                        succ=False
                        QMessageBox.about(self, "", "修改失败")
                    if succ:
                        QMessageBox.about(self, "", "修改成功")
                # 改VIP有效期
                elif self.functionMode==3:
                    ifdateright=False
                    # 判断日期是否合法
                    try:
                        time.strptime(datetext,"%Y-%m-%d")
                        ifdateright = True
                    except:
                        ifdateright = False
                    if not ifdateright:
                        QMessageBox.warning(self,"警告","日期格式有误")
                    else:
                        try:
                            curs.execute("UPDATE eatecuser.users SET vip_endtime='{}' WHERE user_name='{}'".format(datetext, nametext))
                        except:
                            QMessageBox.warning(self,"","修改失败")
                # 改管理员
                elif self.functionMode==4:
                    try:
                        curs.execute("UPDATE eatecuser.users SET is_admin='{}' WHERE user_name='{}'".format(admintext, nametext))
                    except:
                        QMessageBox.warning(self,"","修改失败")
                # 删
                elif self.functionMode==5:
                    try:
                        curs.execute("DELETE FROM eatecuser.users WHERE user_name='{}'".format(nametext))
                    except:
                        QMessageBox.warning(self,"","删除失败")
                db.close()
                self.refresh()
        except Exception:
            QMessageBox.warning(self, "数据库连接失败", "数据库连接失败，请检查网络连接！")

    # 刷新
    def refresh(self):
        self.view_data()
    # 添加一行数据行
    def add_row_data(self):
        self.functionMode=1
        self.b_run.setText("添加用户")
        self.pw_modifytext.setEnabled(True)
        self.vip_modifytext.setEnabled(True)
        self.date_modifytext.setEnabled(True)
        self.adm_modifytext.setEnabled(True)
    # 删除一行数据
    def del_row_data(self):
        self.functionMode=5
        self.b_run.setText("删除用户")
        self.pw_modifytext.setEnabled(False)
        self.vip_modifytext.setEnabled(False)
        self.date_modifytext.setEnabled(False)
        self.adm_modifytext.setEnabled(False)
    # 修改VIP状态
    def altervip(self):
        self.functionMode = 2
        self.b_run.setText("修改VIP状态")
        self.pw_modifytext.setEnabled(False)
        self.vip_modifytext.setEnabled(True)
        self.date_modifytext.setEnabled(False)
        self.adm_modifytext.setEnabled(False)
    # 修改VIP有效期
    def altervipdate(self):
        self.functionMode = 3
        self.b_run.setText("修改有效期")
        self.pw_modifytext.setEnabled(False)
        self.vip_modifytext.setEnabled(False)
        self.date_modifytext.setEnabled(True)
        self.adm_modifytext.setEnabled(False)
    # 修改管理员状态
    def alteradmin(self):
        self.functionMode = 4
        self.b_run.setText("修改管理员状态")
        self.pw_modifytext.setEnabled(False)
        self.vip_modifytext.setEnabled(False)
        self.date_modifytext.setEnabled(False)
        self.adm_modifytext.setEnabled(True)
    # # 退出
    # def exit(self):
    #     sys.exit(app.exec_())


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)#自动适配不同dpi的屏幕
    app = QApplication(sys.argv)
    window = DBMS()
    window.show()
    sys.exit(app.exec_())