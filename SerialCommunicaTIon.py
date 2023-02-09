#-*-coding:utf-8 -*-
'''
    @Project ：SEMG_Assistant
    @File    ：SerialCommunication.py
    @description：
        该文件包括与STM32进行串口通信的函数
        具体通信流程如下：
        The process of communication with the upper computer:
        (1) First of all, STM32 sends the synchronization sequence signal to the upper computer
            The synchronization sequence signal is 0x56 and After send the synchronization signal, STM32 controls LED3 flip level
        (2) After receiving the synchronization signal, the upper computer send to PC the ack signal
            The ack signal is 0x57. After receive the ack signal, STM32 reverses the level of LED4
        (3) After received the ack signal, STM32 sends the data structure
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''
# =============================================== 导入库 ===============================================
import serial
import serial.tools.list_ports
import time
import binascii
import threading

# ============================================== 全局变量 ==============================================

# ---------------------------- 与通信同步相关的变量 ------------------------------
# 同步信号
Sync_Signal = '56'
# 应答信号
Ack_Signal  = bytes.fromhex('57')
# 同步变量接收成功标志位
isSyncSignalFlag = False

# ---------------------------- 与电压数据相关的变量 ------------------------------

# 上一次接收到的电压数据
last_voltage_data_0 = 0
last_voltage_data_1 = 0
last_voltage_data_2 = 0
last_voltage_data_3 = 0

# 电压数据长度
val_data_length     = 8

# 当前接收到的电压值
now_time            = 0
now_voltage_data_0  = 0
now_voltage_data_1  = 0
now_voltage_data_2  = 0
now_voltage_data_3  = 0

# 数据暂存队列
# 队列尺寸
DataSize                = 500
#长度占位 声明长度为size的数据区
now_time_list           = [None]*DataSize
now_voltage_data_0_list = [None]*DataSize
now_voltage_data_1_list = [None]*DataSize
now_voltage_data_2_list = [None]*DataSize
now_voltage_data_3_list = [None]*DataSize
# 记录数据中元素长度
DataListCount           = 0

# ---------------------------- 与代码测试相关的变量 ------------------------------

# 是否启用代码运行速度测试：0-不启用，1-启用
USE_FUNCTIONS_RUN_TIME_TEST  = 0
# 代码运行次数计数
VAL_RunTimeCount             = 0
# 代码运行次数阈值
VAL_RunTimeCountTimes        = 2000
# 电压成功接收次数
VAL_SuccessRecvValValueTimes = 0
# 是否开启线程测试：0-不启用，1-启用
USE_THREAD_TEST              = 0

# ============================================== 函数定义 ==============================================

# 发送应答信号
def Send_Ack(ser_obj):
    global Ack_Signal
    ser_obj.write(Ack_Signal)

# 获取串口设备对应的端口
def Get_Serial_Port():
    '''
    @description  : 获取串口设备对应的端口
    @return {str} : 返回的端口号
    '''
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        print(ports.index(port), port)
    selected = -1

    while selected < 0 or selected >= len(ports):
        print(" 请输入选择的端口号 [ 从0开始 ] : ")
        selected = int(input())
        print("选择的端口号 : ", selected)

    port = ports[selected]
    print("使用的端口名称 ： ", port)
    port = list(port)
    return port[0]

# 打开串口中固定端口并持续接收数据
def Serial_Data_Receive(locker, port = None, size = 11):
    '''
    :description  : 根据数据帧格式对串口接收数据进行解析
    :param port   : 指定读取的端口
    :param size   : 一次读取数据长度(bytes) ，默认11
    :param locker : 互斥锁
    :return       : 单次接收到的数据，16进制显示
    '''

    # 用到的全局变量
    global isSyncSignalFlag
    global Sync_Signal
    global count
    global USE_THREAD_TEST
    global USE_FUNCTIONS_RUN_TIME_TEST

    global now_time
    global now_voltage_data_0
    global now_voltage_data_1
    global now_voltage_data_2
    global now_voltage_data_3

    # 队列尺寸
    global DataSize
    # 长度占位 声明长度为size的数据区
    global now_time_list
    global now_voltage_data_0_list
    global now_voltage_data_1_list
    global now_voltage_data_2_list
    global now_voltage_data_3_list
    # 记录数据中元素长度
    global DataListCount

    # 如果启用代码时间统计功能
    if USE_FUNCTIONS_RUN_TIME_TEST == 1:
        # 声明全局变量：代码运行次数计数变量
        global VAL_RunTimeCount
        # 声明全局变量：代码运行次数阈值
        global VAL_RunTimeCountTimes

    # 选择端口
    if not port:
        locker.acquire()
        port = Get_Serial_Port()
        locker.release()

    # 定义串口对象变量
    serial_obj  = None

    # 轮询读取
    while True :
        try:

            # 获取互斥锁
            locker.acquire()

            if USE_THREAD_TEST == 1:
                lock.acquire()

            # 如果没有创建对象
            if not serial_obj:
                # 创建串口对象,配置串口基本参数，由于STM32使用虚拟串口，这里串口通信参数并不重要
                serial_obj = serial.Serial(port, 115200)

            # 如果串口没有打开
            if not serial_obj.is_open:
                # 串口可以打开
                serial_obj.open()

            # 如果启用代码时间统计功能
            if USE_FUNCTIONS_RUN_TIME_TEST == 1:
                # 如果代码运行到了指定次数
                if VAL_RunTimeCount == VAL_RunTimeCountTimes:
                    VAL_RunTimeCount = 0
                    # 跳出程序循环
                    break

            # 按照单字节读取串口数据
            temp_SyncData = serial_obj.read(1)

            # 将变量转换为16进制后，在转换为str
            temp_SyncData = str(binascii.b2a_hex(temp_SyncData))[2:-1]

            # 判断同步信号是否到来
            if Sync_Signal in temp_SyncData:
                isSyncSignalFlag = True

            # 成功接收同步信号
            if isSyncSignalFlag != False:

                # 发送应答信号
                Send_Ack(serial_obj)
                temp_data = serial_obj.read(size)

                # 打印输出当前接收到的变量，变量的Hex转换成字符串
                # print("Recv Data :", str(binascii.b2a_hex(temp_data))[2:-1])

                # 串口数据解析
                now_time,now_voltage_data_0, now_voltage_data_1, now_voltage_data_2, now_voltage_data_3 = Serial_RecData_Analysis(temp_data)

                # 数据打印输出
                # print("now_time:", now_time)
                # print("now_voltage_data_0:", now_voltage_data_0)
                # print("now_voltage_data_1:", now_voltage_data_1)
                # print("now_voltage_data_2:", now_voltage_data_2)
                # print("now_voltage_data_3:", now_voltage_data_3)

                # 如果缓存数组已经满，则从0开始，用新数据替代旧数据
                if DataListCount == DataSize:
                    DataListCount = 0

                # 放入暂存数组
                now_time_list[DataListCount]           = now_time
                now_voltage_data_0_list[DataListCount] = now_voltage_data_0
                now_voltage_data_1_list[DataListCount] = now_voltage_data_1
                now_voltage_data_2_list[DataListCount] = now_voltage_data_2
                now_voltage_data_3_list[DataListCount] = now_voltage_data_3
                DataListCount = DataListCount + 1

                # print(now_voltage_data_0_list)

                # 释放互斥锁
                locker.release()

                # 如果启用代码时间统计功能
                if USE_FUNCTIONS_RUN_TIME_TEST == 1:
                    # 串口接收到数据，代码运行次数计数变量递增
                    VAL_RunTimeCount = VAL_RunTimeCount + 1

                if USE_THREAD_TEST == 1:
                    lock.release()

            # 接收错误或者未接收到变量
            else:
                # 跳过，执行下一次循环
                continue

        except Exception as e :
            if USE_THREAD_TEST == 1:
                lock.acquire()

            print("exception ： ", e)
            print("串口接收失败")
            if serial_obj:
                serial_obj.close()
            time.sleep(100)

            if USE_THREAD_TEST == 1:
                lock.release()
    return None

# 根据数据帧格式对串口接收数据进行解析
'''
The upper computer receive data structures
    Communication protocol format(通信协议帧)：
    | frame header | | frame header | DataType | DATAx_H | DATAx_L | Stop |
    x = 0~3
    (1) frame header :
        Sending two 0x55 consecutively indicates data arrival
    (2) DataType :
        Indicate whether the data is ADC data of SEMG sensor or Angle and angular velocity data of gyroscope
            ADC_TYPE (0) -Datax The data type is float
            GYROSCOPE_TYPE (1) -Datax The data type is uint16
    (3) DATAx :
        DATAx_H : The high eight bits of data
        DATAx_L : The low eight bits of data
    (4) Stop :
        Sending 0x78 indicates the end of sending a data frame
'''
def Serial_RecData_Analysis(Data_List):
    '''
    @description : 根据数据帧格式对串口接收数据进行解析
    @param  {list} Data_List[]          : 待解析的数据，字节组成的列表
                                          example :  56555500037a03300270023d
    @return {int} temp_voltage_data_x   : 当前接收到的电压数据 , x = 0~3
    @return {int}  temp_time : 接收到数据时的时间
    '''
    # 如果启用代码时间统计功能
    if USE_FUNCTIONS_RUN_TIME_TEST == 1:
        # 声明全局变量：串口接收到有效数据的次数
        global VAL_SuccessRecvValValueTimes

    # 用到的全局变量
    global last_voltage_data_0
    global last_voltage_data_1
    global last_voltage_data_2
    global last_voltage_data_3

    # 电压数据长度
    val_data_length = 8

    # 缓存的临时电压数据
    temp_voltage_data_0 = 0
    temp_voltage_data_1 = 0
    temp_voltage_data_2 = 0
    temp_voltage_data_3 = 0

    # 接收到的时间戳
    temp_time = time.clock()

    try:
        # 寻找起始帧
        Start_Frame = Data_List.index(b'\x55')
        # print("起始帧索引： ",start_frame)
        # print("接收到的数据：",Data_List)

        if USE_FUNCTIONS_RUN_TIME_TEST == 1:
            global VAL_SuccessRecvValValueTimes

        # 接收到了起始帧
        if Start_Frame > 0 :
            # 确认数据类型，电压数据还是陀螺仪数据
            Data_Class = Data_List[Start_Frame+2]
            # print("数据类型 ：",Data_Class)

            # 如果启用代码时间统计功能
            if (USE_FUNCTIONS_RUN_TIME_TEST == 1) and (Start_Frame>0):
                # 串口接收到有效数据的次数加1
                VAL_SuccessRecvValValueTimes = VAL_SuccessRecvValValueTimes + 1

            # 电压类型
            if Data_Class == 0 :
                # 电压数据解析，将四个电压数据（高八位和第八位数据）置于临时列表
                temp_voltage_data_list = Data_List[Start_Frame+3:]
                # print("temp_voltage_data_list: ",str(binascii.b2a_hex(temp_voltage_data_list))[2:-1])

                temp_voltage_data_0_h = temp_voltage_data_list[0]
                temp_voltage_data_0_l = temp_voltage_data_list[1]
                temp_voltage_data_0   = temp_voltage_data_0_h << 8 | temp_voltage_data_0_l
                # print(temp_voltage_data_0)

                temp_voltage_data_1_h = temp_voltage_data_list[2]
                temp_voltage_data_1_l = temp_voltage_data_list[3]
                temp_voltage_data_1 = temp_voltage_data_1_h << 8 | temp_voltage_data_1_l
                # print(temp_voltage_data_1)

                temp_voltage_data_2_h = temp_voltage_data_list[4]
                temp_voltage_data_2_l = temp_voltage_data_list[5]
                temp_voltage_data_2 = temp_voltage_data_2_h << 8 | temp_voltage_data_2_l
                # print(temp_voltage_data_2)

                temp_voltage_data_3_h = temp_voltage_data_list[6]
                temp_voltage_data_3_l = temp_voltage_data_list[7]
                temp_voltage_data_3 = temp_voltage_data_3_h << 8 | temp_voltage_data_3_l
                # print(temp_voltage_data_3)

                # 用新值替换旧值
                last_voltage_data_0 = temp_voltage_data_0
                last_voltage_data_1 = temp_voltage_data_1
                last_voltage_data_2 = temp_voltage_data_2
                last_voltage_data_3 = temp_voltage_data_3

    except Exception as e :
        # print("exception ： ", e)
        # print("串口未检测到起始帧")

        # 电压数据与上次接收到的电压数据相同
        temp_voltage_data_0 = last_voltage_data_0
        temp_voltage_data_1 = last_voltage_data_1
        temp_voltage_data_2 = last_voltage_data_2
        temp_voltage_data_3 = last_voltage_data_3

    return temp_time, temp_voltage_data_0, temp_voltage_data_1, temp_voltage_data_2, temp_voltage_data_3

# 返回当前采集到的电压值和时间戳
def Rect_Now_Val_Values():
    global now_time
    global now_voltage_data_0
    global now_voltage_data_1
    global now_voltage_data_2
    global now_voltage_data_3

    return now_time,now_voltage_data_0,now_voltage_data_1,now_voltage_data_2,now_voltage_data_3

# 返回数据暂存数组列表
def Rect_Val_Cache_List():
    global now_time_list
    global now_voltage_data_0_list
    global now_voltage_data_1_list
    global now_voltage_data_2_list
    global now_voltage_data_3_list

    return now_time_list, now_voltage_data_0_list, now_voltage_data_1_list, now_voltage_data_2_list, now_voltage_data_3_list

# 返回缓存数组当前size的大小
def Rect_DataListCount_Value():
    global DataListCount

    return DataListCount

# 线程一：串口数据接收
def Thread_SerialDataRecv():
    while True:
        global USE_THREAD_TEST

        if USE_THREAD_TEST == 1:
            global USE_FUNCTIONS_RUN_TIME_TEST

            # 如果启用代码时间统计功能
            if USE_FUNCTIONS_RUN_TIME_TEST == 1:
                # 记录程序开始时间
                start_time = time.clock()

            # 经测试：STM32发送频率f=2000Hz，发送两个帧头/0x55/0x55，
            # 上位机不接收停止位，即size=12时，效果最好-玄学
            Serial_Data_Receive(lock, port = None, size = 12)

            # 如果启用代码时间统计功能
            if USE_FUNCTIONS_RUN_TIME_TEST == 1:
                # 记录程序结束时间
                finish_time = time.clock()

            # 如果启用代码时间统计功能
            if USE_FUNCTIONS_RUN_TIME_TEST == 1:
                # 输出程序运行时间
                print("Run time : ", finish_time - start_time)
                print("有效接收数据次数 ：", VAL_SuccessRecvValValueTimes)

# 线程二：串口数据打印
def Thread_PrintValData():

    global USE_THREAD_TEST

    while True:
        if USE_THREAD_TEST == 1:
            lock.acquire()
            time_list, now_voltage_data_0_list, now_voltage_data_1_list, now_voltage_data_2_list, now_voltage_data_3_list = Rect_Val_Cache_List()
            print("time_list:",time_list)
            # print("now_voltage_data_0_list:", now_voltage_data_0_list)
            # print("now_voltage_data_1_list:", now_voltage_data_1_list)
            # print("now_voltage_data_2_list:", now_voltage_data_2_list)
            # print("now_voltage_data_3_list:", now_voltage_data_3_list)
            lock.release()
            time.sleep(1)

if __name__ == '__main__':
    if USE_THREAD_TEST == 1:
        lock = threading.Lock()
        thread_rcv   = threading.Thread(target=Thread_SerialDataRecv)
        thread_print = threading.Thread(target=Thread_PrintValData)
        thread_rcv.start()
        thread_print.start()

    if USE_THREAD_TEST == 0:

        # 如果启用代码时间统计功能
        if USE_FUNCTIONS_RUN_TIME_TEST == 1:
            # 记录程序开始时间
            start_time = time.clock()

        # 经测试：STM32发送频率f=2000Hz，发送两个帧头/0x55/0x55，
        # 上位机不接收停止位，即size=12时，效果最好-玄学
        Serial_Data_Receive(lock, port = None, size = 12)

        # 如果启用代码时间统计功能
        if USE_FUNCTIONS_RUN_TIME_TEST == 1:
            # 记录程序结束时间
            finish_time = time.clock()

        # 如果启用代码时间统计功能
        if USE_FUNCTIONS_RUN_TIME_TEST == 1:
            # 输出程序运行时间
            print("Run time : ", finish_time - start_time)
            print("有效接收数据次数 ：", VAL_SuccessRecvValValueTimes)

