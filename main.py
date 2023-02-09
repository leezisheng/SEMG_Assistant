#-*-coding:utf-8 -*-

'''
    @Project ：SEMG_Assistant
    @File    ：main.py
    @description：
        主程序，工作流程如下：
        （1） 选择端口，配置端口相关参数，在完成通信同步后，读取STM32发送的电压数据（f约为300Hz左右），放入暂存数组中
        （2）
        （3）
        （4）
        （5）
        （6）
        （7）
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================

# 串口通信相关依赖库
import SerialCommunication
# 绘图相关依赖库
import CurveDrawing
import matplotlib.pyplot as plt
# 多线程相关的库
import threading
# 时间相关的库
import time

# ============================================== 全局变量 ==============================================





# ============================================== 函数定义 ==============================================
# 串口读取线程
def Thread_SerialDataRecv():

    while True:
        # 经测试：STM32发送频率f=2000Hz，发送两个帧头/0x55/0x55，
        # 上位机不接收停止位，即size=12时，效果最好-玄学
        SerialCommunication.Serial_Data_Receive(lock, port = None, size = 12)

# 原始SEMG绘图线程
def Thread_Generate_Original_SEMG_Data():

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

if __name__ == '__main__':
    lock = threading.Lock()
    thread_rcv  = threading.Thread(target=Thread_SerialDataRecv)
    thread_plot = threading.Thread(target=Thread_Generate_Original_SEMG_Data)
    thread_rcv.start()
    thread_plot.start()










