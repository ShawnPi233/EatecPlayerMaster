from PyQt5.QtGui import *
from GUI3 import Ui_MainWindow
from myVideoWidget import myVideoWidget
import qtmodern.styles
import qtmodern.windows
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import jaydebeapi
import os
import sys
import qtmodern.styles
import qtmodern.windows
import datetime
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5 import QtCore
import random
from Datebase import DBMS
from MyAccount import MyAcc
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import time
import win32gui #用于截图
import Autosub
keyWords = ''
keyPhrases = ''
# ---------------------------------------------------对话框弹窗类--------------------------------------------------------
class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.resize(250, 100)
        layout = QFormLayout()
        self.lb1 = QLabel("账号")
        self.le1 = QLineEdit()
        layout.addRow(self.lb1, self.le1)
        self.lb2 = QLabel("邮箱")
        self.le2 = QLineEdit()
        layout.addRow(self.lb2, self.le2)
        self.btn3 = QPushButton("发送验证邮件")
        layout.addRow(self.btn3)
        # self.btn3.clicked.connect(self.sendemail)
        self.setLayout(layout)
        self.setWindowTitle("找回密码")
        self.setWindowIcon(QIcon(r"EatecPlayer_logo.png"))  # 任务栏图标添加
    #未使用
    def sendemail(self):
        sender="2379457118@qq.com"
        senderpassword="cumnwzxzrfwcecaf"
        receivers = ['3041276927@qq.com']
        message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
        message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
        message['To'] = Header("测试", 'utf-8')  # 接收者
        subject = 'Python SMTP 邮件测试'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP('smtp.qq.com',465)
            smtpObj.login(sender,"cumnwzxzrfwcecaf")
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

# -----------------------------------------------------激活码验证弹窗-----------------------------------------------
class CodeValidateWindow(QDialog):
    def __init__(self, parent=None):
        self.isVIP = False
        super(CodeValidateWindow, self).__init__(parent)
        self.resize(250, 100)
        self.setWindowTitle("激活VIP")
        layout = QFormLayout()
        self.lb_acc = QLabel("账号")
        self.le_acc = QLineEdit()
        layout.addRow(self.lb_acc, self.le_acc)
        self.lb_code = QLabel("激活码")
        self.le_code = QLineEdit()
        layout.addRow(self.lb_code, self.le_code)
        self.btn_confirmCode = QPushButton("确定激活")
        self.btn_confirmCode.clicked.connect(self.validate_code)

        layout.addRow(self.btn_confirmCode)
        self.setLayout(layout)
        self.setWindowIcon(QIcon(r"icon.png"))  # 任务栏图标添加
    def validate_code(self):
        url = 'jdbc:postgresql://192.168.195.129:26000/eatecuser'
        user = 'dbuser'
        password = 'Bigdata@123'
        conn = jaydebeapi.connect('org.postgresql.Driver', url, [user, password], 'D:\Download\postgresql-42.3.1.jar')
        curs = conn.cursor()
        selectsql = "SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.le_acc.text())
        # curs.execute('set search_path to eatecuser')
        curs.execute(selectsql)
        data = curs.fetchone()
        print(data)
        if data:# 如果查询返回值非空
            if data[4]:
                QMessageBox.warning(self, "提示", "您已经是VIP用户，无需再激活。")
                curs.close()
                conn.close()
                print("数据库已关闭")
                return
        else:
            QMessageBox.warning(self, "激活验证", "激活失败，请检查账号名！")
            curs.close()
            conn.close()
            print("数据库已关闭")
            return
        if data:  # 如果查询返回值非空
            if data[2] == self.le_code.text():
                self.isVIP = True
                curs.execute("UPDATE eatecuser.users SET is_vip=TRUE WHERE user_name='{}'".format(self.le_acc.text()))
        if self.isVIP:
            QMessageBox.about(self, "激活验证", "激活成功，尊敬的SVIP用户！")
        else:
            QMessageBox.warning(self, "激活验证", "激活失败，请检查账号激活码！")
        curs.close()
        conn.close()
        print("数据库已关闭")


# -------------------------------------------------------主窗体类--------------------------------------------------------
class myMainWindow(Ui_MainWindow, QMainWindow, CodeValidateWindow):
    def __init__(self):
        # self.create_sql()  # 创建用户数据库
        # self.isAdmin = False
        # self.isOpen = False
        # self.isLogin = False
        # self.sld_video_pressed = False
        self.keyWords = ''
        self.keyPhrases = ''
        self.loginUser="" #当前登录用户，默认为空
        self.totalPlayTime = 0
        self.isFileOpen = True  # 视频文件是否已打开
        self.isAdmin = True
        self.isOpen = True
        self.isLogin = True
        self.sld_video_pressed = True
        self.app = QApplication(sys.argv)
        super(Ui_MainWindow, self).__init__()
        super(CodeValidateWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(r"icon.png"))  # 图标添加
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.videoFullScreen = False  # 判断当前widget是否全屏
        self.videoFullScreenWidget = myVideoWidget()  # 创建一个全屏的widget
        self.videoFullScreenWidget.setFullScreen(True)
        self.videoFullScreenWidget.hide()  # 不用的时候隐藏起来

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.wgt_video)  # 视频播放输出的widget，就是上面定义的
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

        self.slider.sliderMoved.connect(self.set_position)
        self.slider.valueChanged.connect(self.setClock)  # 设置时间条

        self.btn_open.clicked.connect(self.openVideoFile)  # 打开视频文件按钮
        self.btn_login.clicked.connect(self.login)  # 登录确认
        #------------------------------------------------------
        self.btn_rigis.clicked.connect(self.logup)  # 注册
        #------------------------------------------------------
        self.btn_play.clicked.connect(self.playVideo)  # 播放
        self.btn_stop.clicked.connect(self.pauseVideo)  # 暂停
        self.btn_close.clicked.connect(self.close)
        self.btn_max.clicked.connect(self.videoDoubleClicked)
        self.btn_mini.clicked.connect(self.showMinimized)
        self.btn_darkmode.clicked.connect(self.darkMode)
        self.btn_fullscreen.clicked.connect(self.videoDoubleClicked)
        self.btn_findPassword.clicked.connect(self.findpswd)
        self.btn_openVIP.clicked.connect(self.show_codeValidateWindow)
        self.volSlider.valueChanged.connect(self.volChanged)  # 音量控制
        # self.setWindowFlag(Qt.FramelessWindowHint)  #隐藏边框
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowTitle("多功能视频播放器")
        self.videoFullScreenWidget.doubleClickedItem.connect(self.videoDoubleClicked)  # 双击响应
        self.wgt_video.doubleClickedItem.connect(self.videoDoubleClicked)  # 双击响应
        qss = "QPushButton{color:black;font:幼圆}" \
              "QPushButton:hover{color:#888888}" \
              "QPushButton:!hover { color: black }" \
              "QPushButton:hover { boder:3px blue  }"
        self.setStyleSheet(qss)
        #--------------------------------------------------------------------------------
        # 工具栏调用
        self.comboBox.currentIndexChanged.connect(self.tools_choose)  # 点击下拉列表，触发对应事件
        #------------------------------------------------------------------------------------
        #self.comboBox.activated(self,4).connect(self.show_notebook)
        now = datetime.datetime.now()
        if now.hour >= 17 or now.hour <= 5:
            self.isDark = True
            self.btn_darkmode.setStyleSheet \
                ("text-align:top;background:#FFFFFF;border-radius:8px")
        else:
            self.isDark = False
            self.btn_darkmode.setStyleSheet \
                ("text-align:top;background:#000000;border-radius:8px")
        # self.actionStudy.triggered.connect()
    #-------------------------------------------------------
    def tools_choose(self):  # 响应工具栏事件
        choice = self.comboBox.currentIndex()
        if not self.isLogin:
            QMessageBox.warning(self,"","请先登录")
            return
        if choice==1:
            try:
                Autosub.toSrt(self.videoUrl)
            except:
                QMessageBox.warning(self, "警告", "请先打开视频")
                reply = QMessageBox.question(self,
                                             '添加字幕',
                                             "添加失败，请先打开视频",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.openVideoFile()
                    # self.videoUrl = QFileDialog.getOpenFileUrl(self, "打开视频", filter="MP4文件(*.mp4)")
                    # self.srtFile=Autosub.toSrt(self.videoUrl[0].fileName())
                else:
                    pass
        elif choice==2:
            try:
                import AbstractTest
                self.srtUrl= QFileDialog.getOpenFileUrl(self, "打开生成字幕", filter="SRT字幕文件(*.srt)")
                self.toAbstract(self.srtUrl[0].fileName())
                QMessageBox.about(self, "关键词生成", "生成成功!")
            except: pass
        elif choice==3:
            try:
                Autosub.toSrt(self.videoUrl)
            except:
                QMessageBox.warning(self, "警告", "请先打开视频")
                reply = QMessageBox.question(self,
                                             '添加字幕',
                                             "添加失败，请先打开视频",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    # self.openVideoFile()
                    self.videoUrl = QFileDialog.getOpenFileUrl(self, "打开视频", filter="MP4文件(*.mp4)")
                    self.srtFile=Autosub.toSrt(self.videoUrl[0].fileName())
                else:
                    pass
        elif choice==4:
            self.show_notebook()
        elif choice==5:
            if self.isAdmin:
                self.showDbmanage()
            else:
                QMessageBox.warning(self,"警告","你不是管理员")
        elif choice==6:
            if self.isLogin:
                self.showMyAccount()
            else:
                QMessageBox(self,"警告","请先登录")
        elif choice==7:
            if self.isLogin:
                self.isLogin=False
                self.account_label.show()
                self.password_label.show()
                self.account_text.show()
                self.password_text.show()
                self.btn_login.show()
                self.btn_rigis.show()
                self.btn_findPassword.show()
                os.remove("un.txt")
            else:
                QMessageBox.warning(self,"","还未登录")
    #-------------------------------------------------------
    # 窗体类内方法实现
    def toAbstract(self,srtfile):#生成关键词
        a = 1
        b = 2
        c = 3
        state = a
        text = ''
        with open(srtfile, 'r', encoding='utf-8') as f:  # 打开srt字幕文件，并去掉文件开头的\ufeff
            for line in f.readlines():  # 遍历srt字幕文件
                if state == a:  # 跳过第一行
                    state = b
                elif state == b:  # 跳过第二行
                    state = c
                elif state == c:  # 读取第三行字幕文本
                    if len(line.strip()) != 0:
                        text += ' ' + line.strip()  # 将同一时间段的字幕文本拼接
                        state = c
                    elif len(line.strip()) == 0:
                        with open('test1.txt', 'a', encoding='utf8') as fa:  # 写入txt文本文件中
                            text2 = text.replace(
                                'Conversion failed', '')
                            text2 = text2.replace(
                                '<font color=#FF0000>', '')
                            fa.write(text2.replace('\n', ''))
                            text = '\n'
                            state = a
        import codecs
        from textrank4zh import TextRank4Keyword, TextRank4Sentence
        # 读取文件
        text = codecs.open('test1.txt', 'r', encoding='utf8').read()
        # 关键词和关键短语
        tr4w = TextRank4Keyword()
        tr4w.analyze(text)
        self.keyWords='1、关键词：\n'
        self.keyPhrases='2、关键短语：\n'
        print('关键词：')
        for item in tr4w.get_keywords(num=5, word_min_len=2):  # 提取5个关键词，关键词最少为2个字
            self.keyWords=self.keyWords+str(item.word)+' 权重:'+str(round(item.weight,2))+'\n'
            print(item.word, '权重:', item.weight)
        print()

        print('关键短语：')
        # 从20个关键词中选出出现次数至少为2的关键短语
        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
            self.keyPhrases = self.keyPhrases + str(phrase)+'\n'
            print(phrase)
        print()
        QMessageBox.about(self, '关键词显示', self.keyWords + self.keyPhrases)
        # with open('test2.txt', 'a', encoding='utf8') as self.fb:  # 写入txt文本文件中
        #     self.fb.write(self.keyWords + '\n' + self.keyPhrases + '\n')
        # 摘要
        tr4s = TextRank4Sentence()
        tr4s.analyze(text)
        print('字幕文本：')
        for item in tr4s.get_key_sentences(num=3):
            # index是语句在文本中位置，weight是权重
            print(item.index, item.weight, '\n  ', item.sentence, '\n')

            # -*- encoding:utf-8 -*-

            import codecs
            from textrank4zh import TextRank4Keyword, TextRank4Sentence

            text = codecs.open('./text/01.txt', 'r', 'utf-8').read()
            tr4w = TextRank4Keyword(stop_words_file='./stopword.data')  # 导入停止词

            # 使用词性过滤，文本小写，窗口为2
            tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)

    def formchange(self):
        if self.isMaximized():
            self.showNormal()  # 切换放大按钮图标字体
        else:
            self.showMaximized()
    #打开视频文件
    def openVideoFile(self):
        if self.isLogin:
            self.pureVideo()
            self.videoUrl= QFileDialog.getOpenFileUrl(self, "打开视频",filter="MP4文件(*.mp4)")
            self.player.setMedia(QMediaContent(self.videoUrl[0]))
            self.wgt_video.setVisible(True)
            self.player.pause()  # 播放视频
            self.isOpen = False
            self.playVideo()
            self.isFileOpen=True
            self.totalPlayTime=0 #单次打开视频的播放总时长
        else:
            self.openError()

    def playVideo(self):#控制视频暂停播放按钮
        if self.isFileOpen:#按钮打开视频文件才有效
            if not self.isOpen:#视频暂停，点击继续播放
                self.player.play()
                self.isOpen = True
                self.btn_play.setText("▎▎")
                self.btn_play.setStyleSheet("font-size:15px;border:none")
                self.beginTime=time.time() #开始计时
            else:#视频正在播放，点击暂停
                self.player.pause()
                self.isOpen = False
                self.btn_play.setText("▶")
                self.btn_play.setStyleSheet("font-size:35px;border:none")
                self.playTime=round(time.time()-self.beginTime,2)#统计播放时长，保留两位小数
                self.totalPlayTime+=self.playTime
                print("已播放时间（s）:"+str(self.playTime))

    def pauseVideo(self):
        self.player.pause()

    #统计当前登录用户，当次打开程序后关闭程序前，总共的播放时长
    def playTimeRecord(self):
        if len(self.loginUser)*self.totalPlayTime==0 :#用户未登录，或未观看视频，则不记录
            pass
        else:
            timeStamp=datetime.datetime.now().strftime('%Y-%m-%d') #当前时间
            try:
                db = self.connectdb()
                curs = db.cursor()
            except:
                QMessageBox.warning(self,"","无法连接至数据库")
            try:
                curs.execute("INSERT INTO eatecuser.userdata(user_name,play_date,playtime_once) VALUES ('{}','{}',{})"
                             .format(self.loginUser, timeStamp, str(round(self.totalPlayTime/60.0,2))))
                curs.close()
                db.close()
                print("数据库已关闭")
            except Exception:
                QMessageBox.warning(self, "", "未知错误，无法保存至数据库")

    # 关闭响应方法重写
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '食课视频播放器',
                                     "是否要退出程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            if QMessageBox.question(self, '保存', '是否保存本次播放时长记录?', QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.Yes:
                self.playTimeRecord()
                QMessageBox.about(self, "记录提醒", "您已播放视频"+str(round(self.totalPlayTime/60.0,2))+ "分钟！\n")
            event.accept()
        else:
            event.ignore()
    # 全屏按钮全屏
    def videoFullScreen(self):
        if self.player.duration() > 0:
            if self.videoFullScreen:
                self.player.pause()
                self.videoFullScreenWidget.hide()
                self.player.setVideoOutput(self.wgt_video)
                self.player.play()
                self.videoFullScreen = False
            else:
                self.player.pause()
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.player.play()
                self.videoFullScreen = True

    # 双击视频全屏
    def videoDoubleClicked(self, text):
        if self.player.duration() > 0:  # 开始播放后才允许进行全屏操作
            if self.videoFullScreen:
                self.player.pause()
                self.videoFullScreenWidget.hide()
                self.player.setVideoOutput(self.wgt_video)
                self.player.play()
                self.videoFullScreen = False
            else:
                self.player.pause()
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.player.play()
                self.videoFullScreen = True
#---------------------------------------------------------------------
    def connectdb(self):
        url = 'jdbc:postgresql://192.168.195.129:26000/eatecuser'
        user = 'dbuser'
        password = 'Bigdata@123'
        # password = 'Gauss#3demo'
        print("正在连接数据库，请稍后...")
        try:
            conn = jaydebeapi.connect('org.postgresql.Driver', url, [user, password], '.\postgresql-42.3.1.jar')
            print("数据库已连接")
            return conn
        except:
            print("连接失败")
        # return conn

    # 单击登录，并弹窗提示
    def login(self):
        try:
            db = self.connectdb()
            curs = db.cursor()
            curs.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.account_text.text()))
            data = curs.fetchone()
            # data = self.selectdb(self.account_text.text())
            if data: # 密码校验
                # if data[1] == self.password_text.text():
                if data[1] == self.password_text.text():
                    self.isLogin = True # 设置是否登录flag
            if self.isLogin:
                self.pureVideo()  # 只显示视频 去除登录界面
                if data[4]:
                    QMessageBox.about(self, "登录验证", "登录成功，尊敬的VIP用户！")
                    self.isVIP=True
                else:
                    QMessageBox.about(self, "登录验证", "登录成功！")
                if data[6]:
                    QMessageBox.about(self, "登录验证", "已开启管理员权限")
                    self.isAdmin=True
                fo = open("un.txt", "w")
                fo.write(data[0])
                fo.close()

                self.loginUser=self.account_text.text()#记录当前登录用户的用户名
            else:
                QMessageBox.warning(self, "登录验证", "登录失败，请检查账号密码！")
            curs.close()
            db.close()
            print("数据库已关闭")
        except :
            QMessageBox.warning(self, "数据库连接失败", "数据库连接失败，请检查网络连接！")

    def logup(self):
        try:
            if self.account_text.text() == "" or self.password_text.text() == "":
                QMessageBox.warning(self, "登录验证", "请先输入用户名或密码！")
                return  # 如果为输入完整则直接退出函数
            db = self.connectdb()
            curs = db.cursor()
            curs.execute("SELECT * FROM eatecuser.users WHERE user_name='{}'".format(self.account_text.text()))
            data = curs.fetchone()
            # data = self.selectdb(self.account_text.text())
            if data:
                QMessageBox.warning(self, "登录验证", "账号已存在，请使用其它用户名。")
            else:
                ran_str = ''.join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 8))  # 产生随机激活码
                print(ran_str)
                # 数据依次为 用户名 密码 cdkey 播放时间（秒） isvip vip到期日期 isadmin
                curs.execute("INSERT INTO eatecuser.users(user_name,user_password,user_cdkey) VALUES ('{}','{}','{}')".format(self.account_text.text(), self.password_text.text(), ran_str))
                self.isLogin = True  # 设置是否登录flag
                QMessageBox.warning(self, "登录验证", "注册成功，已自动登录。")
            if self.isLogin:
                self.pureVideo()  # 只显示视频 去除登录界面
            curs.close()
            db.close()
            print("数据库已关闭")
        except :
            QMessageBox.warning(self, "数据库连接失败", "数据库连接失败，请检查网络连接！")
#-----------------------------------------------------------
    # 找回密码
    def findpswd(self):
        self.show_dialog()
        QMessageBox.about(self, "验证邮件", "发送成功，请到邮箱查收！")
        flag = True

    # 打开视频时隐藏登录界面
    def pureVideo(self):
        self.account_label.hide()
        self.password_label.hide()
        self.account_text.hide()
        self.password_text.hide()
        self.btn_login.hide()
        self.btn_rigis.hide()
        self.btn_findPassword.hide()

    def openError(self):
        QMessageBox.about(self, "打开失败", "请先登录账号！")

    # --------------------------------以下为无边框窗口移动实现方法---------------------------#
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # --------------------------------夜间模式实现方法---------------------------#
    def darkMode(self):
        if self.isDark == False:  # 天黑自动夜间模式或手动夜间模式
            qtmodern.styles.dark(self.app)
            self.btn_darkmode.setStyleSheet \
                ("\ text-align:top;\
                background:#FFFFFF;\
                border-radius:8px;\
                border:none;\
                font-size:13px;")
            self.isDark = True
        else:
            qtmodern.styles.light(self.app)
            self.btn_darkmode.setStyleSheet \
                ("\ text-align:top;\
                background:#000000;\
                border-radius:8px;\
                border:none;\
                font-size:13px;")
            self.isDark = False

    # 弹出窗体显示
    def show_dialog(self):
        dialog = MyDialog()
        dialog.show()
        dialog.exec()

    def show_notebook(self):
        note = NotebookWindow()
        note1 = qtmodern.windows.ModernWindow(note)
        note1.show()


    def show_codeValidateWindow(self):
        codeValidateWindow = CodeValidateWindow()
        codeValidateWindow.show()
        codeValidateWindow.exec()
#------------------------------------------------------------------------------
    windowList = []
    def showDbmanage(self):  # 启动管理员的数据库管理系统
        dbms = DBMS()
        self.windowList.append(dbms)
        dbms.show()

    def showMyAccount(self):  # 启动个人账户管理
        accwindow = MyAcc()
        self.windowList.append(accwindow)
        accwindow.show()
#---------------------------------------------------------------------------------

    # ------------------------------------视频进度条------------------------------------------
    def setClock(self):
        tmp1 = self.player.position()
        tmp2 = self.player.duration()
        t1m = str(tmp1 // 1000 // 60).zfill(2)  # 补足2位 //表示整除
        t1s = str(tmp1 // 1000 % 60).zfill(2)  # 同上
        t2m = str(tmp2 // 1000 // 60).zfill(2)  # 同上
        t2s = str(tmp2 // 1000 % 60).zfill(2)  # 同上
        self.lb_time.setText("%s:%s/%s:%s" % (t1m, t1s, t2m, t2s))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

    def volChanged(self):  # 音量调节
        self.player.setVolume(self.volSlider.value())



    # ----------------------------------------工具栏功能实现方法-------------------------------------------

    def __main__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 自动适配不同dpi的屏幕
        self.app = QApplication(sys.argv)
        self.mw = myMainWindow()
        now = datetime.datetime.now()
        if now.hour >= 17 or now.hour <= 5:
            qtmodern.styles.dark(self.app)
        else:
            qtmodern.styles.light(self.app)
        self.mw.show()
        sys.exit(self.app.exec_())

# 记事本
class NotebookWindow(myMainWindow):
    def __init__(self):
        # super(NotebookWindow, self).__init__()
        super(myMainWindow, self).__init__()
        self.setGeometry(600, 500, 570, 445)
        layout = QFormLayout()
        self.lb_text = QLabel("笔记")
        self.le_text = QTextEdit()
        layout.addRow(self.lb_text, self.le_text)
        self.lb_name = QLabel("笔记命名")
        self.le_name = QLineEdit()
        layout.addRow(self.lb_name, self.le_name)
        self.btn_save = QPushButton("保存便笺")
        layout.addRow(self.btn_save)
        self.setLayout(layout)
        self.setWindowIcon(QIcon(r"icon.png"))  # 任务栏图标添加
        self.btn_save.clicked.connect(self.save_notebook)

        self.setWindowTitle("食课便笺")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.setWindowOpacity(0.9)

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') #记录笔记时间
        self.filename = nowTime + '.txt' #根据时间命名默认文件名
        self.openFileName = self.filename
        self.openFilePath = r'Notes:'
        self.isSaved = False
        self.fintText = ''
        self.replaceText = ''
        if(keyWords !=''):
            self.replaceText =self.replaceText+keyWords+'\n'+keyPhrases+'\n'
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 1, 0, 0)

        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

        self.menuFile = QMenu("文件(&F)")
        self.menuEdit = QMenu("编辑(&E)")
        self.menuFormat = QMenu("格式(&D)")
        self.menuView = QMenu("查看(&V)")
        self.menuInsertImg = QMenu("插图(&I)")

        self.menuBar.addMenu(self.menuFile)
        self.menuBar.addMenu(self.menuEdit)
        self.menuBar.addMenu(self.menuFormat)
        self.menuBar.addMenu(self.menuView)
        self.menuBar.addMenu(self.menuInsertImg)

        self.menuFileNew = QAction("新建(&N)")
        self.menuFileNew.setShortcut("Ctrl+N")
        self.menuFile.addAction(self.menuFileNew)
        self.menuFileNew.triggered.connect(self.newFile)

        self.menuImgCut = QAction("插入视频截图")
        self.menuImgCut.setShortcut("Ctrl+I") #快捷键
        self.menuInsertImg.addAction(self.menuImgCut) #将按钮加入初级菜单
        self.menuImgCut.triggered.connect(self.insertCutImg) #槽函数连接



        self.menuImgOut = QAction("插入图片")
        self.menuImgOut.setShortcut("Ctrl+Shift+I") #快捷键
        self.menuInsertImg.addAction(self.menuImgOut) #将按钮加入初级菜单
        self.menuImgOut.triggered.connect(self.insertImg) #槽函数连接

        self.menuFileOpen = QAction("打开(&O)")
        self.menuFileOpen.setShortcut("Ctrl+O")
        self.menuFile.addAction(self.menuFileOpen)
        self.menuFileOpen.triggered.connect(self.openFile)

        self.menuFileSave = QAction("保存(&S)")
        self.menuFileSave.setShortcut("Ctrl+S")
        self.menuFile.addAction(self.menuFileSave)
        self.menuFileSave.triggered.connect(self.saveFile)

        self.menuFileSaveAs = QAction("另存为(&A)...")
        self.menuFile.addAction(self.menuFileSaveAs)
        self.menuFileSaveAs.triggered.connect(self.saveas)

        self.menuFile.addSeparator()
        self.menuExit = QAction("退出(&X)")
        self.menuFile.addAction(self.menuExit)
        self.menuExit.triggered.connect(self.exit)

        self.menuEditUndo = QAction("撤销(&U)")
        self.menuEditUndo.setShortcut("Ctrl+Z")
        self.menuEdit.addAction(self.menuEditUndo)
        self.menuEditUndo.triggered.connect(self.undo)

        self.menuEdit.addSeparator()

        self.menuEditCut = QAction("剪切(&T)")
        self.menuEditCut.setShortcut("Ctrl+X")
        self.menuEdit.addAction(self.menuEditCut)
        self.menuEditCut.triggered.connect(self.cut)

        self.menuEditCopy = QAction("复制(&C)")
        self.menuEditCopy.setShortcut("Ctrl+C")
        self.menuEdit.addAction(self.menuEditCopy)
        self.menuEditCopy.triggered.connect(self.copy)

        self.menuEditPaste = QAction("粘贴(&P)")
        self.menuEditPaste.setShortcut("Ctrl+V")
        self.menuEdit.addAction(self.menuEditPaste)
        self.menuEditPaste.triggered.connect(self.paste)

        self.menuEditDel = QAction("删除(&T)")
        self.menuEditDel.setShortcut("Del")
        self.menuEdit.addAction(self.menuEditDel)
        self.menuEditDel.triggered.connect(self.delete)

        self.menuEdit.addSeparator()
        self.menuEdit.addSeparator()

        self.menuEditAll = QAction("全选(&A)")
        self.menuEditAll.setShortcut("Ctrl+A")
        self.menuEdit.addAction(self.menuEditAll)
        self.menuEditAll.triggered.connect(self.selectAll)

        # self.menuEditDate = QAction("时间/日期(&D)")
        # self.menuEditDate.setShortcut("F5")
        # self.menuEdit.addAction(self.menuEditDate)
        # self.menuEditDate.triggered.connect(self.insertDatetime)

        self.menuFormatWarp = QAction("自动换行(&W)")
        self.menuFormatWarp.setCheckable(True)
        self.menuFormatWarp.setChecked(True)
        self.menuFormat.addAction(self.menuFormatWarp)
        self.menuFormatWarp.changed.connect(self.formatWarp)

        self.menuFormatFont = QAction("字体(&F)...")
        self.menuFormat.addAction(self.menuFormatFont)
        self.menuFormatFont.triggered.connect(self.fontSelect)

        self.menuViewStatusBar = QAction("状态栏(&S)")
        self.menuViewStatusBar.setCheckable(True)
        self.menuViewStatusBar.setChecked(True)
        self.menuView.addAction(self.menuViewStatusBar)
        self.menuViewStatusBar.changed.connect(self.statusBarShow)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.plainTextEdit = QTextEdit(self)
        self.gridLayout.addWidget(self.plainTextEdit)
        self.font = QFont("幼圆", 12)
        self.plainTextEdit.setFont(self.font)
        self.plainTextEdit.cursorPositionChanged.connect(self.cursorPosition)
        self.plainTextEdit.textChanged.connect(self.textChange)

        self.dailywordCount=0 #统计当天个数
        self.dailyNoteCount=0 #统计当天笔记次数
        # self.multiTextEdit = QTextEdit(self)
        # self.gridLayout.addWidget(self.plainTextEdit)
        # with open('test2.txt', 'a', encoding='utf8') as fb:  # 写入txt文本文件中0
        #     self.plainTextEdit.append(fb.read())
        #     fb.close()
        # self.plainTextEdit.appendPlainText("本次视频播放时长："+
        #                                    str(round(self.totalPlayTime/60,2))+"分"+
        #                                    str(round(self.totalPlayTime%60,2))+"秒\n")
        # self.plainTextEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # self.plainTextEdit.customContextMenuRequested[QtCore.QPoint].connect(self.myListWidgetContext)
        qss = "QPushButton{color:black;font:幼圆}" \
              "QPushButton:hover{color:#888888}" \
              "QPushButton:!hover { color: black }" \
              "QPushButton:hover { boder:3px blue  }"
        self.setStyleSheet(qss)
        self.show()
    #插入视频截图
    def insertCutImg(self):
        try:
            hwnd = win32gui.FindWindow("Qt5152QWindowIcon", u'多功能视频播放器')  # 获取视频播放器窗口句柄，Class名由软件Spy++获取
            screen = QApplication.primaryScreen()
            img = screen.grabWindow(hwnd).toImage()
            FName = fr"{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}"  # 文件名初始化
            img.save((r'./Images/'+f"{FName}.jpg"))
            self.tc = self.plainTextEdit.textCursor()  # 获取光标对象
            self.tc.insertImage(img)
        except Exception:
            QMessageBox.warning(self ,"截图失败" ,"截图失败，请稍后再试!")
    def insertImg(self):
        try:
            imgName,imgType= QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
            jpg = QPixmap(imgName).toImage()
            self.tc = self.plainTextEdit.textCursor()  # 获取光标对象
            self.tc.insertImage(jpg)
        except Exception:
            QMessageBox.warning(self,"加载失败","请打开正确的图片格式！")
    # def dropEvent(self, event):
    #     # super().dropEvent(event)
    #     try:
    #         jpg=(QPixmap(event.mimeData().imageData())).toImage()
    #         self.tc=self.plainTextEdit.textCursor()
    #         self.tc.insertImage(jpg)
    #     except:
    #         QMessageBox.warning(self, "拖入失败", "拖入失败，请检查导入文件是否为图片!")
    #     pass
    #统计当前登录用户笔记次数
    def takeNoteRecord(self):
            self.dailyNoteCount+=1
            self.dailywordCount = self.plainTextEdit.toPlainText().__len__()
            QMessageBox.about(self, '记录提醒', '您本次已记录笔记' + str(self.dailywordCount) + '字!')
            timeStamp=datetime.datetime.now().strftime('%Y-%m-%d') #当前时间
            self.loginUser = ''
            try:
                fo = open("un.txt", "r")  # 读取已登录的用户名
                self.loginUser = fo.read()
            except:
                QMessageBox.warning(self, "", "用户未登录或无法读取登录信息")
                return
            if self.loginUser=='':
                QMessageBox.warning(self, "", "用户未登录或无法读取登录信息")
                return
            else:
                fo.close()
            # print(self.loginUser+"  "+timeStamp+"  "+str(self.dailyNoteCount)+"  "+str(self.dailywordCount))
            try:
                db = self.connectdb()
                curs = db.cursor()
                curs.execute("SELECT * FROM eatecuser.notedata WHERE user_name='{}' AND note_date='{}'"
                             .format(self.loginUser,timeStamp))
                temp = curs.fetchall()
                if temp:  # 如果找到该用户当天的笔记数据
                    try:
                        curs.execute("UPDATE eatecuser.notedata SET note_count={},word_count={} WHERE user_name='{}' AND note_date='{}'"
                                     .format(str(self.dailyNoteCount+temp[2]), str(self.dailywordCount+temp[3]), self.loginUser, timeStamp))
                    except:
                        QMessageBox.warning(self,"","未知错误，无法保存至数据库")
                else:  # 如果没有找到该用户当天的笔记数据
                    try:
                        curs.execute("INSERT INTO eatecuser.notedata VALUES ('{}','{}',{},{})"
                                     .format(self.loginUser, timeStamp, str(self.dailyNoteCount), str(self.dailywordCount)))
                    except:
                        QMessageBox.warning(self,"","未知错误，无法保存至数据库")
                    curs.close()
                    db.close()
                    print("数据库已关闭")
            except Exception:
                QMessageBox.warning(self, "数据库连接失败", "数据库连接失败，请检查网络连接！")

    # 关闭窗口重写
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '食课便笺',
                                     "是否要退出程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            if QMessageBox.question(self,'保存','是否保存?',QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.Yes:
                self.save_notebook()
            if QMessageBox.question(self, '保存', '是否保存笔记记录?', QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No) == QMessageBox.Yes:
                self.takeNoteRecord()
                # QMessageBox.about(self, '记录提醒', '您本次已记录笔记' + str(self.dailywordCount) + '字!')
            event.accept()
        else:
            event.ignore()

    def save_notebook(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = nowTime + '.txt'
        f = open(filename, 'w')
        f.write(self.le_text.toPlainText())  # 读取笔记内容
        f.close()
        QMessageBox.about(self, "食课便笺", "保存成功！")

    def get_thread(self, main_thread):
        self.main_thread = main_thread

    def newFile(self):
        self.openFilePath = ''
        self.openFileName = self.filename
        self.setWindowTitle(self.openFileName + ' - 食课便笺')
        self.plainTextEdit.clear()


    def openFile(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "打开", "./", "文本文档 (*.txt);;所有文件 (*)")
        if filename != "":
            self.plainTextEdit.clear()
            with open(filename, 'r', encoding='gb18030', errors='ignore') as f:
                self.plainTextEdit.appendPlainText(f.read())
            f.close()
            self.openFilePath = filename
            self.openFileName = os.path.basename(filename)
            self.setWindowTitle(self.openFileName + ' - 食课便笺')

    def saveFile(self):
        if self.openFilePath == "":
            filename, filetype = QFileDialog.getSaveFileName(self, '保存', './', "文本文档 (*.md);;所有文件 (*)")
            if filename == "":
                return False

            self.openFilePath = filename
            self.openFileName = os.path.basename(filename)
            self.setWindowTitle(self.openFileName + ' - 食课便笺')

        file = open(self.openFilePath, 'w', encoding='gb18030', errors='ignore')
        file.write(self.plainTextEdit.toPlainText())
        file.close()
        self.setWindowTitle(self.openFileName + ' - 食课便笺')
        self.isSaved = True
        return True

    def saveas(self):
        filename, filetype = QFileDialog.getSaveFileName(self, '保存', './', "文本文档 (*.txt);;所有文件 (*)")
        if filename == "":
            return False

        self.openFilePath = filename
        self.openFileName = os.path.basename(filename)
        self.setWindowTitle(self.openFileName + ' - 食课便笺')
        file = open(self.openFilePath, 'w', encoding='gb18030', errors='ignore')
        file.write(self.plainTextEdit.toPlainText())
        file.close()
        self.setWindowTitle(self.openFileName + ' - 食课便笺')
        self.isSaved = True
        return True

    def exit(self):
        if not self.isSaved:
            result = QMessageBox.question(self, '食课便笺', '是否将更改保存到' + self.openFileName,
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if result == QMessageBox.Yes:
                result = self.saveFile()
                if result:
                    QtCore.QCoreApplication.quit()
                else:
                    return False
            elif result == QMessageBox.No:
                QtCore.QCoreApplication.quit()
            else:
                return False

        return True

    def undo(self):
        self.plainTextEdit.undo()

    def cut(self):
        self.plainTextEdit.cut()

    def copy(self):
        self.plainTextEdit.copy()

    def paste(self):
        self.plainTextEdit.paste()

    def delete(self):
        self.plainTextEdit.textCursor().deletePreviousChar()

    def selectAll(self):
        self.plainTextEdit.selectAll()

    # def insertDatetime(self):
    #         datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #         self.plainTextEdit.insertPlainText(datetime)

    def fontSelect(self):
        font, ok = QFontDialog.getFont(self.font)
        if ok:
            self.font = font
            self.plainTextEdit.setFont(font)

    def textChange(self):
        self.isSaved = False
        self.setWindowTitle('食课便笺  ' + self.openFileName)

    def formatWarp(self):
        if self.menuFormatWarp.isChecked():
            self.plainTextEdit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)

    def statusBarShow(self):
        if self.menuViewStatusBar.isChecked():
            self.statusBar.show()
        else:
            self.statusBar.hide()

    # def insertDatetime(self):
    #     self.plainTextEdit.insertPlainText(self.lb_time.text())

    def cursorPosition(self):
        row = self.plainTextEdit.textCursor().blockNumber()
        col = self.plainTextEdit.textCursor().columnNumber()
        self.statusBar.showMessage("行 %d , 列 %d" % (row + 1, col + 1))
    # def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
    #     pass
class Runwindow(myMainWindow):
    def __init__(self):
        super(myMainWindow).__init__()


if __name__ == '__main__':
    rw = Runwindow()
    try:
        os.remove("un.txt")
    except:
        print()
    rw.__main__()
