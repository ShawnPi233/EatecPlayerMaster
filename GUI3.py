# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI3.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter
# from PyQt5.QtWidgets import QSlider
# from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 445)
        # MainWindow.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        #视频窗口
        self.wgt_video = myVideoWidget(self.centralwidget)
        self.wgt_video.setEnabled(True)
        self.wgt_video.setVisible(False)
        #self.wgt_video.setGeometry(QtCore.QRect(50, 20, 471, 251))
        self.wgt_video.setGeometry(QtCore.QRect(0, 20, 570, 300))
        self.wgt_video.setObjectName("wgt_video")

        #时间进度文字
        self.lb_time=QtWidgets.QLabel(MainWindow)
        self.lb_time.setText("00:00/00:00")
        self.lb_time.setGeometry(QtCore.QRect(245, 350, 92, 28))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.lb_time.setFont(font)

        self.account_label = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.account_label.setFont(font)
        self.account_label.setGeometry(QtCore.QRect(170, 100, 41, 31))
        self.account_label.setObjectName("account_label")
        # font = QtGui.QFont()
        # font.setFamily("幼圆")

        self.account_text = QtWidgets.QLineEdit(MainWindow)
        self.account_text.setGeometry(QtCore.QRect(220, 100, 191, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.account_text.setFont(font)
        self.account_text.setObjectName("account_text")
        self.account_text.setPlaceholderText("请输入账号")
        self.account_text.setAlignment(QtCore.Qt.AlignCenter)  # 居中显示

        self.password_label = QtWidgets.QLabel(MainWindow)
        # font = QtGui.QFont()
        # font.setFamily("幼圆")
        self.password_label.setFont(font)
        self.password_label.setGeometry(QtCore.QRect(170, 140, 41, 31))
        self.password_label.setObjectName("password_label")
       # 密码框
        self.password_text =QtWidgets.QLineEdit(MainWindow)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.password_text.setFont(font)
        self.password_text.setGeometry(QtCore.QRect(220, 140, 191, 31))
        self.password_text.setObjectName("password_text")
        self.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text.setPlaceholderText("请输入6位以上密码")
        self.password_text.setAlignment(QtCore.Qt.AlignCenter) #居中显示
        #忘记密码
        self.btn_findPassword = QtWidgets.QPushButton(MainWindow)
        # font = QtGui.QFont()
        # font.setFamily("幼圆")
        self.btn_findPassword.setFont(font)
        self.btn_findPassword.setStyleSheet("border:none;font-color:#999999")
        self.btn_findPassword.setGeometry(QtCore.QRect(420, 125, 70, 60))
        self.btn_findPassword.setObjectName("findPassword_label")

        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(50, 350, 92, 28))
        # font = QtGui.QFont()
        # font.setFamily("幼圆")
        self.btn_open.setFont(font)
        self.btn_open.setStyleSheet("")
        self.btn_open.setAutoExclusive(False)
        self.btn_open.setObjectName("btn_open")

        self.btn_fullscreen=QtWidgets.QPushButton(self.centralwidget)
        self.btn_fullscreen.setGeometry(QtCore.QRect(50, 390, 92, 28))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.btn_fullscreen.setFont(font)
        self.btn_fullscreen.setStyleSheet("border:none")
        self.btn_fullscreen.setAutoExclusive(False)
        self.btn_fullscreen.setObjectName("btn_fullscreen")

        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(50, 321, 471, 20))
        self.slider.setMaximum(100)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("sld_video")

        self.btn_play = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play.setGeometry(QtCore.QRect(240, 390, 92, 28))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.btn_play.setFont(font)
        self.btn_play.setStyleSheet("font-size:35px;border:none;")
        self.btn_play.setObjectName("btn_play")

        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(420, 390, 60, 28))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.btn_stop.setFont(font)
        self.btn_stop.setStyleSheet("font-size:35px;border-radius:8px;")
        self.btn_stop.setObjectName("btn_stop")

        self.btn_login = QtWidgets.QPushButton(self.centralwidget)
        self.btn_login.setGeometry(QtCore.QRect(170, 240, 92, 28))
        self.btn_login.setStyleSheet("")
        self.btn_login.setFont(font)
        self.btn_login.setObjectName("btn_login")

        self.btn_rigis = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rigis.setGeometry(QtCore.QRect(315, 240, 92, 28))
        self.btn_rigis.setStyleSheet("")
        self.btn_rigis.setFont(font)
        self.btn_rigis.setObjectName("btn_rigis")


        # self.slider = QtWidgets.QLabel(self.centralwidget)
        # self.slider= QtWidgets.QSlider(Qt.Horizontal)
        # self.slider.setGeometry(QtCore.QRect(270, 340, 50, 50))
        # self.slider.setObjectName("slider")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(430, 350, 92, 28))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.comboBox.setFont(font)


        self.lb_bar = QtWidgets.QLabel(self.centralwidget)
        self.lb_bar.setGeometry(QtCore.QRect(0, 0, 570,25))
        self.lb_bar.setAlignment(QtCore.Qt.AlignCenter)  # 居中显示
        font = QtGui.QFont()
        font.setFamily("幼圆")
        self.lb_bar.setFont(font)
        self.lb_bar.setStyleSheet\
        ("\
        text-align:top;\
        background:#777777;\
        border:none;\
        font-size:15px;\
        color:rgb(30 144 255)\
        ")
        # VIP激活
        self.btn_openVIP = QtWidgets.QPushButton(self.centralwidget)
        self.btn_openVIP.setGeometry(QtCore.QRect(450, 3.5, 18, 18))
        self.btn_openVIP.setStyleSheet \
            ("\
               text-align:top;\
               background:#1E90FF;\
               border-radius:8px;\
               border:none;\
               font-size:15px;\
               color:rgb(255,255,255)\
               ")
        self.btn_openVIP.setFont(font)
        self.btn_openVIP.setToolTip("激活验证码")
        #切换夜间模式
        self.btn_darkmode = QtWidgets.QPushButton(self.centralwidget)
        self.btn_darkmode.setGeometry(QtCore.QRect(475, 3.5, 18, 18))
        self.btn_darkmode.setStyleSheet\
        ("\
        text-align:top;\
        background:#000000;\
        border-radius:8px;\
        border:none;\
        font-size:13px;\
        ")
        self.btn_darkmode.setToolTip("切换夜间/日间模式")
        #缩放按钮
        self.btn_mini = QtWidgets.QPushButton(self.centralwidget)
        self.btn_mini.setGeometry(QtCore.QRect(500, 3.5, 18, 18))
        self.btn_mini.setStyleSheet\
        ("\
        text-align:top;\
        background:#F7D674;\
        border-radius:8px;\
        border:none;\
        font-size:13px;\
        ")

        self.btn_mini.setText("")
        self.btn_mini.setObjectName("left_hint")
        self.btn_mini.setToolTip("最小化")
        #最大化按钮
        self.btn_max = QtWidgets.QPushButton(self.centralwidget)
        self.btn_max.setGeometry(QtCore.QRect(525, 3.5, 18, 18))
        self.btn_max.setStyleSheet\
        ("\
        text-align:top;\
        background:#6DDF6D;\
        border-radius:8px;\
        border:none;\
        font-size:13px;\
        ")
        self.btn_max.setText("")
        self.btn_max.setObjectName("left_mini")
        self.btn_max.setToolTip("最大化")
        #关闭窗口按钮
        self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_close.setGeometry(QtCore.QRect(550, 3.5, 18, 18))
        self.btn_close.setStyleSheet\
        ("\
        text-align:top;\
        background:#F76677;\
        border-radius:8px;\
        border:none;\
        font-size:13px;\
        ")
        self.btn_close.setText("")
        self.btn_close.setObjectName("left_close")

        #音量控制条
        self.volLabel = QtWidgets.QLabel(self.centralwidget)
        self.volLabel.setText("音量")
        self.volLabel.setFont(font)
        self.volLabel.setGeometry(QtCore.QRect(490, 390, 30, 30))

        self.volSlider = QtWidgets.QSlider(self.centralwidget)
        self.volSlider.setOrientation(QtCore.Qt.Vertical)
        self.volSlider.setGeometry(QtCore.QRect(500, 340, 90, 80))
        self.volSlider.setRange(0, 100)
        self.volSlider.setValue(80)  # 默认80%的音量
        self.volSlider.setObjectName("volSlider")

        #统计数据曲线
        self.paint_line=QPainter(self.centralwidget)
        self.paint_line.begin(self)
        self.paint_line.drawRect(150,50,50,50)
        self.paint_line.end()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "食课视频播放器"))
        self.btn_open.setText(_translate("MainWindow", "打开视频"))
        self.btn_play.setText(_translate("MainWindow", "▶"))
        self.btn_stop.setText(_translate("MainWindow", "▶▶"))
        self.btn_fullscreen.setText(_translate("MainWindow", "全屏"))
        # self.slider.setText(_translate("MainWindow", "0%"))
        self.btn_login.setText(_translate("MainWindow", "登录"))
        self.btn_rigis.setText(_translate("MainWindow", "注册"))
        self.btn_openVIP.setText(_translate("MainWindow", "V"))
        self.comboBox.setItemText(0, _translate("MainWindow", " 工具栏"))
        self.comboBox.setItemText(1, _translate("MainWindow", "字幕显示"))
        self.comboBox.setItemText(2, _translate("MainWindow", "关键词显示"))
        self.comboBox.setItemText(3, _translate("MainWindow", "语音识别生成字幕"))
        self.comboBox.setItemText(4, _translate("MainWindow", "食课便笺"))
        self.comboBox.setItemText(5, _translate("MainWindow", "数据管理"))
        self.comboBox.setItemText(6, _translate("MainWindow", "账户管理"))
        self.comboBox.setItemText(7, _translate("MainWindow", "退出登录"))
        self.account_label.setText(_translate("MainWindow", "账号"))
        self.password_label.setText(_translate("MainWindow", "密码"))
        self.btn_findPassword.setText(_translate("MainWindow", "忘记密码"))
        self.lb_bar.setText(_translate("MainWindow", "食课视频播放器"))

from myVideoWidget import myVideoWidget
# import label_rc
