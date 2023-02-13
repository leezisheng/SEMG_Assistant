#-*-coding:utf-8 -*-

'''
    @Project ：SEMG_Assistant
    @File    ：SoftwareUI.py.py
    @description：
        GUI界面程序：
        显示SEMG信号的时域特征和频域特征
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
#导入designer工具生成的login模块
from SEMG_Assistant_Ui import Ui_Form
import time
import threading
from DigitalSignalsProcess import Semg_Feature_Class
import random

# ============================================== 全局变量 ==============================================

# 信号特征实例化
Semg_0_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_1_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_2_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_3_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
    def UpData(self,Semg_Obj_0,Semg_Obj_1,Semg_Obj_2,Semg_Obj_3):
        # 更新SEMG通道0数据
        self.var_label_time_max_0.setText(str(Semg_Obj_0.t_max))
        self.var_label_time_min_0.setText(str(Semg_Obj_0.t_min))
        self.var_label_time_mean_0.setText(str(Semg_Obj_0.t_mean))
        self.var_label_time_var_0.setText(str(Semg_Obj_0.t_var))
        self.var_label_time_rms_0.setText(str(Semg_Obj_0.t_rms))

        self.var_label_fre_med_0.setText(str(Semg_Obj_0.f_med))
        self.var_label_fre_mean_0.setText(str(Semg_Obj_0.f_mean))
        self.var_label_fre_cog_0.setText(str(Semg_Obj_0.f_cog))
        self.var_label_fre_mse_0.setText(str(Semg_Obj_0.f_mse))
        self.var_label_fre_var_0.setText(str(Semg_Obj_0.f_var))

        # 更新SEMG通道1数据
        self.var_label_time_max_1.setText(str(Semg_Obj_1.t_max))
        self.var_label_time_min_1.setText(str(Semg_Obj_1.t_min))
        self.var_label_time_mean_1.setText(str(Semg_Obj_1.t_mean))
        self.var_label_time_var_1.setText(str(Semg_Obj_1.t_var))
        self.var_label_time_rms_1.setText(str(Semg_Obj_1.t_rms))

        self.var_label_fre_med_1.setText(str(Semg_Obj_1.f_med))
        self.var_label_fre_mean_1.setText(str(Semg_Obj_1.f_mean))
        self.var_label_fre_cog_1.setText(str(Semg_Obj_1.f_cog))
        self.var_label_fre_mse_1.setText(str(Semg_Obj_1.f_mse))
        self.var_label_fre_var_1.setText(str(Semg_Obj_1.f_var))

        # 更新SEMG通道2数据
        self.var_label_time_max_2.setText(str(Semg_Obj_2.t_max))
        self.var_label_time_min_2.setText(str(Semg_Obj_2.t_min))
        self.var_label_time_mean_2.setText(str(Semg_Obj_2.t_mean))
        self.var_label_time_var_2.setText(str(Semg_Obj_2.t_var))
        self.var_label_time_rms_2.setText(str(Semg_Obj_2.t_rms))

        self.var_label_fre_med_2.setText(str(Semg_Obj_2.f_med))
        self.var_label_fre_mean_2.setText(str(Semg_Obj_2.f_mean))
        self.var_label_fre_cog_2.setText(str(Semg_Obj_2.f_cog))
        self.var_label_fre_mse_2.setText(str(Semg_Obj_2.f_mse))
        self.var_label_fre_var_2.setText(str(Semg_Obj_2.f_var))

        # 更新SEMG通道2数据
        self.var_label_time_max_3.setText(str(Semg_Obj_3.t_max))
        self.var_label_time_min_3.setText(str(Semg_Obj_3.t_min))
        self.var_label_time_mean_3.setText(str(Semg_Obj_3.t_mean))
        self.var_label_time_var_3.setText(str(Semg_Obj_3.t_var))
        self.var_label_time_rms_3.setText(str(Semg_Obj_3.t_rms))

        self.var_label_fre_med_3.setText(str(Semg_Obj_3.f_med))
        self.var_label_fre_mean_3.setText(str(Semg_Obj_3.f_mean))
        self.var_label_fre_cog_3.setText(str(Semg_Obj_3.f_cog))
        self.var_label_fre_mse_3.setText(str(Semg_Obj_3.f_mse))
        self.var_label_fre_var_3.setText(str(Semg_Obj_3.f_var))

# 固定的，PyQt5程序都需要QApplication对象
# sys.argv是命令行参数列表，确保程序可以双击运行
app = QApplication(sys.argv)

# 初始化
myWin = MyMainForm()

# ============================================== 函数定义 ==============================================

# 初始化窗口
def Init_UI_Windows():
    global myWin

    # 将窗口控件显示在屏幕上
    myWin.show()
    myWin.setWindowTitle('SEMG Assistant V1.0')

def Delete_UI_Windows():
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())

# 线程1：生成模拟SEMG数据
def Thread_Generate_SEMG_Signal():
    while True:
        # 获取锁
        lock.acquire()

        # 更新SEMG通道0数据
        Semg_0_Feature.Update_Feature(random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300))

        # 更新SEMG通道1数据
        Semg_1_Feature.Update_Feature(random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300))

        # 更新SEMG通道2数据
        Semg_2_Feature.Update_Feature(random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300))

        # 更新SEMG通道3数据
        Semg_3_Feature.Update_Feature(random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300),
                                      random.randint(0, 3300))

        # 使用完后释放锁
        lock.release()

# 线程2：动态更新Ui界面参数
def Thread_Updata_Ui_Data():
    global myWin

    global Semg_0_Feature
    global Semg_1_Feature
    global Semg_2_Feature
    global Semg_3_Feature

    while True:
        # 获取锁
        lock.acquire()

        # 更新Ui界面参数
        myWin.UpData(Semg_0_Feature,Semg_1_Feature,Semg_2_Feature,Semg_3_Feature)
        time.sleep(0.01)

        # 使用完后释放锁
        lock.release()

if __name__ == '__main__':
    # 初始化窗口
    Init_UI_Windows()

    # 创建互斥锁
    lock = threading.Lock()

    # 线程声明
    thread_GenerateData = threading.Thread(target=Thread_Generate_SEMG_Signal)
    # 线程声明
    thread_Updata = threading.Thread(target=Thread_Updata_Ui_Data)

    # 线程开启
    thread_GenerateData.start()
    thread_Updata.start()

    Delete_UI_Windows()
