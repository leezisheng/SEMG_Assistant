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
import time
import random
import threading
from SerialCommunication import DataSize
import DigitalSignalsProcess

# ============================================== 全局变量 ==============================================

# 是否使用模拟数据生成函数进行多线程测试：0-不启用，1-启用
USE_GENERATE_DATA_THREAD_TEST   = 0

# 绘图暂停时间
PLOT_PAUSE_TIME                 = 0.01

# 测试生成数据变量
TEST_DATALIST_SIZE              = DataSize
Test_DataListCount              = 0
Test_Time_List                  = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_0_List        = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_1_List        = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_2_List        = [None]*TEST_DATALIST_SIZE
Test_Voltage_Data_3_List        = [None]*TEST_DATALIST_SIZE

# ============================================== 函数定义 ==============================================

# 原始SEMG电压波形绘制,包括时域曲线和幅频曲线
# 使用前需要先创建自定义图像，即fig=plt.figure()
def Original_SemgSignal_Plot(fig,temp_data_count_val,temp_data_list_0,temp_data_list_1,temp_data_list_2,temp_data_list_3,temp_time_data_list):
    '''
    :param fig:                 画布
    :param temp_data_count_val: 数组计数变量
    :param temp_data_list_0:    通道0电压值列表
    :param temp_data_list_1:    通道1电压值列表
    :param temp_data_list_2:    通道2电压值列表
    :param temp_data_list_3:    通道3电压值列表
    :param temp_time_data_list: 时间列表
    :return: None
    '''

    # 使matplotlib的显示模式转换为交互（interactive）模式
    plt.ion()

    try:
        # 清除之前画的图
        plt.clf()

        # ================================== 时域曲线绘制 ==================================

        # plt.plot(x, y, format_string, **kwargs)
        # x：x轴数据，列表或数组，可选
        # y：y轴数据，列表或数组
        # format_string：控制曲线的格式字符串，可选，由颜色字符、风格字符和标记字符组成

        fig.add_subplot(2, 4, 1)
        plt.plot(list(range(temp_data_count_val)), temp_data_list_0[:temp_data_count_val], 'r')
        # 添加标题
        plt.title("Raw SEMG signal display:CH0", loc="left",fontsize='x-small',fontweight='heavy')
        # 设置x轴范围
        plt.xlim(-10, TEST_DATALIST_SIZE + 10)
        # 设置标签
        plt.ylabel("Voltage value(mv)", size=10)

        fig.add_subplot(2, 4, 2)
        plt.plot(list(range(temp_data_count_val)), temp_data_list_1[:temp_data_count_val], 'b')
        # 添加标题
        plt.title("Raw SEMG signal display:CH1", loc="left",fontsize='x-small',fontweight='heavy')
        # 设置x轴范围
        plt.xlim(-10, TEST_DATALIST_SIZE + 10)
        # 设置标签
        plt.ylabel("Voltage value(mv)", size=10)

        fig.add_subplot(2, 4, 3)
        plt.plot(list(range(temp_data_count_val)), temp_data_list_2[:temp_data_count_val], 'm')
        # 添加标题
        plt.title("Raw SEMG signal display:CH2", loc="left",fontsize='x-small',fontweight='heavy')
        # 设置x轴范围
        plt.xlim(-10, TEST_DATALIST_SIZE + 10)
        # 设置标签
        plt.ylabel("Voltage value(mv)", size=10)

        fig.add_subplot(2, 4, 4)
        plt.plot(list(range(temp_data_count_val)), temp_data_list_3[:temp_data_count_val], 'c')
        # 添加标题
        plt.title("Raw SEMG signal display:CH3", loc="left",fontsize='x-small',fontweight='heavy')
        # 设置x轴范围
        plt.xlim(-10, TEST_DATALIST_SIZE + 10)
        # 设置标签
        plt.ylabel("Voltage value(mv)", size=10)

        # print(temp_Voltage_Data_0_List[:temp_DataCount_Val])
        # print(temp_data_count_val)

        # ================================== 幅频曲线绘制 ==================================

        temp_semg_data_list_0 = temp_data_list_0[0:temp_data_count_val]
        temp_semg_data_list_1 = temp_data_list_1[0:temp_data_count_val]
        temp_semg_data_list_2 = temp_data_list_2[0:temp_data_count_val]
        temp_semg_data_list_3 = temp_data_list_3[0:temp_data_count_val]

        amp_list_0, fre_list_0, pha_list_0 = DigitalSignalsProcess.Get_Signals_FFT(temp_semg_data_list_0,
                                                                                   DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_1, fre_list_1, pha_list_1 = DigitalSignalsProcess.Get_Signals_FFT(temp_semg_data_list_1,
                                                                                   DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_2, fre_list_2, pha_list_2 = DigitalSignalsProcess.Get_Signals_FFT(temp_semg_data_list_2,
                                                                                   DigitalSignalsProcess.SAMPLE_FRE)
        amp_list_3, fre_list_3, pha_list_3 = DigitalSignalsProcess.Get_Signals_FFT(temp_semg_data_list_3,
                                                                                   DigitalSignalsProcess.SAMPLE_FRE)

        fig.add_subplot(2, 4, 5)
        plt.title("SEMG signal FFT:CH0", loc="left",fontsize='x-small',fontweight='heavy')
        plt.plot(fre_list_0, amp_list_0)
        plt.ylabel('Amplitute / a.u.')
        plt.xlabel('Frequence / Hz')

        fig.add_subplot(2, 4, 6)
        plt.title("SEMG signal FFT:CH1", loc="left",fontsize='x-small',fontweight='heavy')
        plt.plot(fre_list_1, amp_list_1)
        plt.ylabel('Amplitute / a.u.')
        plt.xlabel('Frequence / Hz')

        fig.add_subplot(2, 4, 7)
        plt.title("SEMG signal FFT:CH2", loc="left",fontsize='x-small',fontweight='heavy')
        plt.plot(fre_list_2, amp_list_2)
        plt.ylabel('Amplitute / a.u.')
        plt.xlabel('Frequence / Hz')

        fig.add_subplot(2, 4, 8)
        plt.title("SEMG signal FFT:CH3", loc="left",fontsize='x-small',fontweight='heavy')
        plt.plot(fre_list_3, amp_list_3)
        plt.ylabel('Amplitute / a.u.')
        plt.xlabel('Frequence / Hz')

        plt.pause(PLOT_PAUSE_TIME)
        plt.ioff()

    except Exception as e:
        print("exception ", e)
        print("原始SEMG电压波形绘制出错")

# 模拟数据生成函数
def Generate_Test_Data():
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:

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

    return

# 模拟数据获取函数:计数变量
def Get_Test_DataCountValue():
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:

        global Test_DataListCount
        return Test_DataListCount

    return

# 模拟数据获取函数:模拟时间和电信号数据
def Get_Test_DataList():
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:

        global Test_Time_List
        global Test_Voltage_Data_0_List
        global Test_Voltage_Data_0_List
        global Test_Voltage_Data_0_List
        global Test_Voltage_Data_0_List

        return Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List

    return

# 模拟数据生成线程
def Thread_Generate_Test_Data():
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:

        while True:
            # 获取锁
            lock.acquire()

            # 获取数据
            Generate_Test_Data()

            # 使用完后释放锁
            lock.release()

            time.sleep(0.005)

    return

# 模拟数据生成图表线程
def Thread_Plot_Test_Data():
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:

        fig = plt.figure()

        while True:

            # 获取锁
            lock.acquire()

            Test_Time_List, Test_Voltage_Data_0_List, Test_Voltage_Data_1_List, Test_Voltage_Data_2_List, Test_Voltage_Data_3_List = Get_Test_DataList()
            Test_DataListCount = Get_Test_DataCountValue()

            # 使用完后释放锁
            lock.release()

            Original_SemgSignal_Plot(fig,
                                     Test_DataListCount,
                                     Test_Voltage_Data_0_List,
                                     Test_Voltage_Data_1_List,
                                     Test_Voltage_Data_2_List,
                                     Test_Voltage_Data_3_List)
    return

if __name__ == '__main__':
    # 如果使用模拟数据生成函数进行多线程测试
    if USE_GENERATE_DATA_THREAD_TEST == 1:
        # 生成锁的实例
        lock = threading.Lock()

        # 线程1：模拟数据生成
        thread_generate = threading.Thread(target=Thread_Generate_Test_Data)
        # 线程2：数据绘图
        thread_plot     = threading.Thread(target=Thread_Plot_Test_Data)

        # 开启线程
        thread_generate.start()
        thread_plot.start()









