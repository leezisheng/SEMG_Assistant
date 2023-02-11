'''
    @Project ：SEMG_Assistant
    @File    ：CsvFileRW.py.py
    @description：
        将SEMG相关数据进行保存，包括：
        （1） 原始SEMG电压值
        （2） SEMG频域幅度值
        （3） SEMG时域特征
        （4） SEMG频域特征
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================

import pandas as pd

# ============================================== 全局变量 ==============================================




# ============================================== 函数定义 ==============================================

# 原始SEMG信号写入csv文件
def Original_SemgSignal_Write(temp_time_data_list,
                              temp_data_list_0,
                              temp_data_list_1,
                              temp_data_list_2,
                              temp_data_list_3,
                              file_path = 'F:\\SEMG_Mechanical_Arm\\code\\SEMG_Assistant\\Dataset\\original_data\\test_data.csv'):
    '''
    :param temp_data_list_0     : 通道0电压值列表
    :param temp_data_list_1     : 通道1电压值列表
    :param temp_data_list_2     : 通道2电压值列表
    :param temp_data_list_3     : 通道3电压值列表
    :param temp_time_data_list  : 时间列表
    :param file_path            : 文件路径
    :return: None
    '''
    try:
        test = pd.DataFrame({
                            'time':temp_time_data_list,
                            'CH0': temp_data_list_0,
                            'CH1': temp_data_list_1,
                            'CH2': temp_data_list_2,
                            'CH3': temp_data_list_3,
                            })

        test.to_csv(file_path, encoding='utf-8')
    except Exception as e :
        print("exception ： ", e)
        print("波形保存错误")