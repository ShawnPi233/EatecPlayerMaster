from PyQt5.QtGui import *
from Ui_MyAccount import Ui_MainWindow
import sys,os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import jaydebeapi
iflogin = True
class MyAcc(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ifdbclose = False
        try:
            fo = open("un.txt", "r")  # 读取已登录的用户名
        except:
            QMessageBox.warning(self,"","用户未登录或无法读取登录信息")
            return
        self.string = fo.read()
        fo.close()
        self.db = self.connectdb()  # 连接数据库
        self.cur = self.db.cursor()
        self.cur.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.string))
        self.data = self.cur.fetchone()
        self.disp_name.setText(self.data[0])
        self.disp_email.setText(self.data[7])
        self.disp_time.setText(str(self.data[3]))
        self.disp_vip.setText(str(self.data[4]))
        self.disp_date.setText(self.data[5])
        self.b_altername.clicked.connect(self.altername)
        self.b_alteremail.clicked.connect(self.alteremail)
        self.b_alterpassword.clicked.connect(self.alterpassword)
        self.b_altertime.clicked.connect(self.cleartime)
        self.b_closedb.clicked.connect(self.closedb)
        self.showplaytime()
        self.setWindowTitle("账号管理")


    def showplaytime(self):
        self.cur.execute("SELECT * FROM eatecuser.userdata")
        timedata = self.cur.fetchall()
        model = QStandardItemModel()
        model.setHorizontalHeaderItem(0, QStandardItem("日期"))
        model.setHorizontalHeaderItem(1, QStandardItem("学习时长(分钟)"))
        for i in range(0,len(timedata)):
            for j in range(1,3):
                model.setItem(i,j-1,QStandardItem(str(timedata[i][j])))
        self.table_playtime.setModel(model)
        self.table_playtime.setColumnWidth(1, 150)

        self.cur.execute("SELECT * FROM eatecuser.notedata")
        notedata = self.cur.fetchall()
        model2 = QStandardItemModel()
        model2.setHorizontalHeaderItem(0, QStandardItem("日期"))
        model2.setHorizontalHeaderItem(1, QStandardItem("笔记数量"))
        model2.setHorizontalHeaderItem(2, QStandardItem("字数统计"))
        for i in range(0, len(notedata)):
            for j in range(1, 4):
                model2.setItem(i, j - 1, QStandardItem(str(notedata[i][j])))
        self.table_note.setModel(model2)

    def altername(self):
        succ=True
        if self.modify_name.text()=="":
            QMessageBox.warning(self,"警告","请输入修改后的用户名")
        else:
            self.cur.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.modify_name.text()))
            t = self.cur.fetchone()
            if t:
                QMessageBox.warning(self, "警告", "已存在该用户")
                succ = False
            else:
                try:
                    self.cur.execute("UPDATE eatecuser.users SET user_name='{}' WHERE user_name='{}'".format(self.modify_name.text(),self.string))
                except:
                    QMessageBox.warning(self,"","修改失败")
                    succ=False
            if succ:
                QMessageBox.about(self,"","修改成功")

    def alteremail(self):
        succ = True
        if self.modify_email.text()=="":
            QMessageBox.warning(self,"警告","请输入新邮箱")
            succ = False
        else:
            try:
                self.cur.execute("UPDATE eatecuser.users SET user_email='{}' WHERE user_name='{}'".format(self.modify_email.text(),self.string))
            except:
                QMessageBox.warning(self,"","修改失败")
                succ = False
        if succ:
            QMessageBox.about(self, "", "修改成功")

    def alterpassword(self):
        succ = True
        if self.modify_password.text()=="" or self.modify_passwordold.text()=="":
            QMessageBox.warning(self,"警告","请输入密码")
            succ = False
        else:
            self.cur.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.string))
            t = self.cur.fetchone()
            if t[1]==self.modify_passwordold.text():
                try:
                    self.cur.execute("UPDATE eatecuser.users SET user_password='{}' WHERE user_name='{}'"
                                     .format(self.modify_password.text(),self.string))
                except:
                    QMessageBox.warning(self,"未知错误","修改失败")
                    succ = False
            else:
                QMessageBox.warning(self, "警告", "旧密码错误")
                succ = False
            if succ:
                QMessageBox.about(self,"","修改成功")

    def cleartime(self):
        succ = True
        try:
            self.cur.execute("UPDATE eatecuser.users SET play_time={} WHERE user_name='{}'"
                             .format('0', self.string))
        except:
            QMessageBox.warning(self, "未知错误", "修改失败")
            succ = False
        if succ:
            QMessageBox.about(self, "", "修改成功")


    def connectdb(self):
        url = 'jdbc:postgresql://192.168.195.129:26000/eatecuser'
        user = 'dbuser'
        password = 'Bigdata@123'
        # password = 'Gauss#3demo'
        print("正在连接数据库，请稍后...")
        conn = jaydebeapi.connect('org.postgresql.Driver', url, [user, password], '.\postgresql-42.3.1.jar')
        print("数据库已连接")
        return conn
    def closedb(self):
        self.db.close()
        print("数据库已关闭")
        self.close()


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)#自动适配不同dpi的屏幕
    app = QApplication(sys.argv)
    window = MyAcc()
    window.show()
    sys.exit(app.exec_())
