# -*- coding: UTF-8 -*-
'''
    @Project ：SEMG_Assistant
    @File    ：CurveDrawing.py
    @description：
        肌电传感器相关数据曲线绘制，包括：
        （1） 原始电压曲线数据绘制
        （2） 频域曲线绘制
        （3） 时频域曲线绘制
        （4） 时域特征曲线绘制：均方根、能量、过零点
        （5） 频域特征曲线绘制：中值频率、均值频率
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================

import matplotlib.pyplot as plt
import SerialCommunication
import time
import random
import threading

# ============================================== 全局变量 ==============================================

# 每次显示的列表尺寸
MAX_DATALIST_SIZE = 35
# 绘图暂停时间
PLOT_PAUSE_TIME   = 0.1

# 测试生成数据变量
TEST_DATALIST_SIZE          = 40
Test_DataListCount          = 0
Test_Time_List              = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_0_List    = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_1_List    = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_2_List    = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_3_List    = [None]*TEST_DATALIST_SIZE

# ============================================== 函数定义 ==============================================

# 原始SEMG电压波形绘制
def Original_SemgSignal_Plot():

    plt.figure()
    # 使matplotlib的显示模式转换为交互（interactive）模式
    plt.ion()

    while True:
        try:
            # 清除之前画的图
            plt.clf()

            # 获取锁
            lock.acquire()

            # 获取模拟生成数据
            temp_time_list, temp_Voltage_Data_0_List, temp_Voltage_Data_1_List, temp_Voltage_Data_2_List, temp_Voltage_Data_3_List = Get_Test_DataList()
            # 获取计数变量
            temp_DataCount_Val = Get_Test_DataCountValue()

            # 使用完后释放锁
            lock.release()

            # plt.plot(x, y, format_string, **kwargs)
            # x：x轴数据，列表或数组，可选
            # y：y轴数据，列表或数组
            # format_string：控制曲线的格式字符串，可选，由颜色字符、风格字符和标记字符组成
            plt.plot(list(range(temp_DataCount_Val)), temp_Voltage_Data_0_List[:temp_DataCount_Val], 'r')
            plt.plot(list(range(temp_DataCount_Val)), temp_Voltage_Data_1_List[:temp_DataCount_Val], 'b')
            plt.plot(list(range(temp_DataCount_Val)), temp_Voltage_Data_2_List[:temp_DataCount_Val], 'm')
            plt.plot(list(range(temp_DataCount_Val)), temp_Voltage_Data_3_List[:temp_DataCount_Val], 'c')
            print(temp_DataCount_Val)
            print(temp_Voltage_Data_0_List[:temp_DataCount_Val])

            # 设置x轴范围
            plt.xlim(-10, 50)
            # 添加图例
            plt.legend(labels=['Voltage_Data_0', 'Voltage_Data_1','Voltage_Data_2', 'Voltage_Data_3'])

            plt.pause(0.01)
            plt.ioff()

        except Exception as e:
            print("exception ", e)
            print("原始SEMG电压波形绘制出错")

# 模拟数据生成函数
def Generate_Test_Data():
    global Test_DataListCount
    global Test_Time_List
    global Test_Voltage_Data_0_List
    global Test_Voltage_Data_1_List
    global Test_Voltage_Data_2_List
    global Test_Voltage_Data_3_List

    if Test_DataListCount >= TEST_DATALIST_SIZE-1:
        Test_DataListCount = 0

    Test_Time_List[Test_DataListCount]           = time.clock()
    Test_Voltage_Data_0_List[Test_DataListCount] = random.randint(0, 3300)
    Test_Voltage_Data_1_List[Test_DataListCount] = random.randint(0, 3300)
    Test_Voltage_Data_2_List[Test_DataListCount] = random.randint(0, 3300)
    Test_Voltage_Data_3_List[Test_DataListCount] = random.randint(0, 3300)

    Test_DataListCount = Test_DataListCount + 1

# 模拟数据获取函数:计数变量
def Get_Test_DataCountValue():
    global Test_DataListCount

    return Test_DataListCount

# 模拟数据获取函数:模拟时间和电信号数据
def Get_Test_DataList():
    global Test_Time_List
    global Test_Voltage_Data_0_List
    global Test_Voltage_Data_0_List
    global Test_Voltage_Data_0_List
    global Test_Voltage_Data_0_List

    return Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List

# 模拟数据生成线程
def Thread_Generate_Test_Data():

    while True:
        # 获取锁
        lock.acquire()

        # 获取数据
        Generate_Test_Data()

        # 使用完后释放锁
        lock.release()

        time.sleep(1)

if __name__ == '__main__':
    # 生成锁的实例
    lock = threading.Lock()

    thread_generate = threading.Thread(target=Thread_Generate_Test_Data)
    thread_plot     = threading.Thread(target=Original_SemgSignal_Plot)
    thread_generate.start()
    thread_plot.start()








