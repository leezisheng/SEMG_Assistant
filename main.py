#-*-coding:utf-8 -*-

'''
    @Project ：SEMG_Assistant
    @File    ：main.py
    @description：
        主程序，工作流程如下：
        （1） 选择端口，配置端口相关参数，在完成通信同步后，读取STM32发送的电压数据（f约为300Hz左右），放入暂存数组中
        （2） 绘制原始信号电压值图像
        （3） 对原始信号进行FFT，得到频域幅度值、相位
        （4） 将原始信号的电压值数据保存为CSV文件
        （5） 计算时域特征并保存
        （6） 计算频域特征并保存
        （7） 上位机控制显示
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================

# 串口通信相关依赖库
import SerialCommunication
# 绘图相关依赖库
import CurveDrawing
import matplotlib.pyplot as plt
# 文件存储相关的库
import CsvFileRW
# 数字信号处理相关的库
import DigitalSignalsProcess
from DigitalSignalsProcess import Semg_Feature_Class
# 多线程相关的库
import threading

# ============================================== 全局变量 ==============================================

# 当计数值大于PLOTDATASIZE时，开始绘图
PLOTDATASIZE = 0.8*(SerialCommunication.DataSize)
# 信号特征实例化
Semg_0_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_1_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_2_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)
Semg_3_Feature = Semg_Feature_Class(0,0,0,0,0,0,0,0,0,0)

# ============================================== 函数定义 ==============================================
# 串口读取线程
def Thread_SerialDataRecv():

    while True:
        # 经测试：STM32发送频率f=2000Hz，发送两个帧头/0x55/0x55，
        # 上位机不接收停止位，即size=12时，效果最好-玄学
        SerialCommunication.Serial_Data_Receive(lock, port = None, size = 12)

# 串口数据传递线程
def Thread_SeialDataTrans():
    while True:
        # 获取锁
        lock.acquire()
        Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List = SerialCommunication.Rect_Val_Cache_List()
        Test_DataListCount = SerialCommunication.Rect_DataListCount_Value()
        # 使用完后释放锁
        lock.release()

# 原始SEMG绘图线程:包括时域曲线和幅频曲线
def Thread_Plot_Data():

    fig = plt.figure()

    while True:
        # 获取锁
        lock.acquire()

        Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List = SerialCommunication.Rect_Val_Cache_List()
        Test_DataListCount = SerialCommunication.Rect_DataListCount_Value()

        # 使用完后释放锁
        lock.release()

        CurveDrawing.Original_SemgSignal_Plot(fig,
                                              Test_DataListCount,
                                              Test_Voltage_Data_0_List,
                                              Test_Voltage_Data_1_List,
                                              Test_Voltage_Data_2_List,
                                              Test_Voltage_Data_3_List,
                                              Test_Time_List)

# 特征提取线程：时域特征和频域特征
def Thread_Feature_Extraction():
    global Semg_0_Feature
    global Semg_1_Feature
    global Semg_2_Feature
    global Semg_3_Feature

    while True:
        # 获取锁
        lock.acquire()

        Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List = SerialCommunication.Rect_Val_Cache_List()
        Test_DataListCount = SerialCommunication.Rect_DataListCount_Value()

        # 使用完后释放锁
        lock.release()

        amp_list_0, fre_list_0, pha_list_0 = DigitalSignalsProcess.Get_Signals_FFT(Test_Voltage_Data_0_List[0:Test_DataListCount],DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_1, fre_list_1, pha_list_1 = DigitalSignalsProcess.Get_Signals_FFT(Test_Voltage_Data_1_List[0:Test_DataListCount],DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_2, fre_list_2, pha_list_2 = DigitalSignalsProcess.Get_Signals_FFT(Test_Voltage_Data_2_List[0:Test_DataListCount],DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_3, fre_list_3, pha_list_3 = DigitalSignalsProcess.Get_Signals_FFT(Test_Voltage_Data_3_List[0:Test_DataListCount],DigitalSignalsProcess.SAMPLE_FRE)

        signal_max_0, signal_min_0, signal_mean_0, signal_var_0, signal_rms_0 = DigitalSignalsProcess.Get_Time_Domain_Features(Test_Voltage_Data_0_List[0:Test_DataListCount])
        signal_max_1, signal_min_1, signal_mean_1, signal_var_1, signal_rms_1 = DigitalSignalsProcess.Get_Time_Domain_Features(Test_Voltage_Data_1_List[0:Test_DataListCount])
        signal_max_2, signal_min_2, signal_mean_2, signal_var_2, signal_rms_2 = DigitalSignalsProcess.Get_Time_Domain_Features(Test_Voltage_Data_2_List[0:Test_DataListCount])
        signal_max_3, signal_min_3, signal_mean_3, signal_var_3, signal_rms_3 = DigitalSignalsProcess.Get_Time_Domain_Features(Test_Voltage_Data_3_List[0:Test_DataListCount])

        Median_frequency_0, Mean_frequency_0, Cog_frequency_0, MSE_frequency_0, Var_frequency_0 = DigitalSignalsProcess.Get_Fre_Domain_Features(amp_list_0)
        Median_frequency_1, Mean_frequency_1, Cog_frequency_1, MSE_frequency_1, Var_frequency_1 = DigitalSignalsProcess.Get_Fre_Domain_Features(amp_list_1)
        Median_frequency_2, Mean_frequency_2, Cog_frequency_2, MSE_frequency_2, Var_frequency_2 = DigitalSignalsProcess.Get_Fre_Domain_Features(amp_list_2)
        Median_frequency_3, Mean_frequency_3, Cog_frequency_3, MSE_frequency_3, Var_frequency_3 = DigitalSignalsProcess.Get_Fre_Domain_Features(amp_list_3)

        # 获取锁
        lock.acquire()

        Semg_0_Feature.Update_Feature(signal_max_0, signal_min_0, signal_mean_0, signal_var_0, signal_rms_0,Median_frequency_0, Mean_frequency_0, Cog_frequency_0, MSE_frequency_0, Var_frequency_0)
        Semg_1_Feature.Update_Feature(signal_max_1, signal_min_1, signal_mean_1, signal_var_1, signal_rms_1,Median_frequency_1, Mean_frequency_1, Cog_frequency_1, MSE_frequency_1, Var_frequency_1)
        Semg_2_Feature.Update_Feature(signal_max_2, signal_min_2, signal_mean_2, signal_var_2, signal_rms_2,Median_frequency_2, Mean_frequency_2, Cog_frequency_2, MSE_frequency_2, Var_frequency_2)
        Semg_3_Feature.Update_Feature(signal_max_3, signal_min_3, signal_mean_3, signal_var_3, signal_rms_3,Median_frequency_3, Mean_frequency_3, Cog_frequency_3, MSE_frequency_3, Var_frequency_3)

        # 使用完后释放锁
        lock.release()

# 原始信号电压数据存储线程
def Thread_Original_SemgSignal_Write():

    while True:
        # 获取锁
        lock.acquire()

        Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List = SerialCommunication.Rect_Val_Cache_List()
        Test_DataListCount = SerialCommunication.Rect_DataListCount_Value()

        # 使用完后释放锁
        lock.release()

        CsvFileRW.Original_SemgSignal_Write(Test_Time_List,
                                            Test_Voltage_Data_0_List,
                                            Test_Voltage_Data_1_List,
                                            Test_Voltage_Data_2_List,
                                            Test_Voltage_Data_3_List
                                            )

if __name__ == '__main__':

    # 创建互斥锁
    lock = threading.Lock()

    # 线程声明
    thread_rcv       = threading.Thread(target=Thread_SerialDataRecv)
    thread_plot      = threading.Thread(target=Thread_Plot_Data)
    thread_OCS_save  = threading.Thread(target=Thread_Original_SemgSignal_Write)
    # thread_Feature   = threading.Thread(target=Thread_Feature_Extraction)

    # 线程开启
    thread_rcv.start()
    thread_plot.start()
    thread_OCS_save.start()
    # thread_Feature.start()