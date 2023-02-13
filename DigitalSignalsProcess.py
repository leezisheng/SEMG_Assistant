#-*-coding:utf-8 -*-

'''
    @Project ：SEMG_Assistant
    @File    ：DigitalSignalsProcess.py
    @description：
        肌电传感器相关数据计算，包括：
        (1) 快速FFT计算其幅值和相位
        (2) 频域特征计算：中值频率、均值频率、重心频率、均方频率、频率方差
        (3) 时域特征计算: 最大值、最小值、均值、方差、有效值
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================
import numpy as np
from scipy.fftpack import fft
import math
from matplotlib import pyplot as plt
import numpy as np
import statistics

# ============================================== 全局变量 ==============================================

# 采样率
SAMPLE_FRE       = 280

#设置生成音频的采样率
#1s产生44100个信号
TEST_SAMPLE_RATE = 44100
#设置生成音频时间的长度
TEST_DURATION    = 5

# SEMG信号类
class Semg_Feature_Class:

    # 初始化方法
    def __init__(self,signal_max,signal_min,signal_mean,signal_var,signal_rms,Median_frequency,Mean_frequency,Cog_frequency,MSE_frequency,Var_frequency):
        # #初始化实例属性
        self.t_max  = signal_max
        self.t_min  = signal_min
        self.t_mean = signal_mean
        self.t_var  = signal_var
        self.t_rms  = signal_rms

        self.f_med  = Median_frequency
        self.f_mean = Mean_frequency
        self.f_cog  = Cog_frequency
        self.f_mse  = MSE_frequency
        self.f_var  = Var_frequency

    # 打印属性
    def detail(self):
        print("========================时域特征========================")
        print("最大值：",self.t_max)
        print("最小值：",self.t_min)
        print("平均值：",self.t_mean)
        print("方差：  ",self.t_var)
        print("有效值：",self.t_rms)
        print("========================频域特征========================")
        print("中值频率：",self.f_med)
        print("均值频率：",self.f_mean)
        print("重心频率：",self.f_cog)
        print("均方频率：",self.f_mse)
        print("频率方差：",self.f_var)

    # 更新数据
    def Update_Feature(self,signal_max,signal_min,signal_mean,signal_var,signal_rms,Median_frequency,Mean_frequency,Cog_frequency,MSE_frequency,Var_frequency):
        self.t_max  = int(signal_max)
        self.t_min  = int(signal_min)
        self.t_mean = int(signal_mean)
        self.t_var  = int(signal_var)
        self.t_rms  = int(signal_rms)

        self.f_med  = int(Median_frequency)
        self.f_mean = int(Mean_frequency)
        self.f_cog  = int(Cog_frequency)
        self.f_mse  = int(MSE_frequency)
        self.f_var  = int(Var_frequency)

# ============================================== 函数定义 ==============================================

# 产生一段虚拟的音频信号
def generate_audio_wave(freq,sample_rate,duration):
    """产生一段虚拟的音频信号
    :param freq: 信号的频率
    :param sample_rate: 信号的采样率
    :param duration: 信号采样的时长
    :return:
    """
    #生成一段时间序列
    t = np.linspace(0,duration,sample_rate*duration,endpoint=False)
    #设置产生音频信号的频率
    frequencies = t * freq
    #设置音频信号的输出的幅值
    y = np.sin((2 * np.pi) * frequencies)
    return t,y

# 快速傅里叶变换
def Get_Signals_FFT(Signal_List,Sample_frequency):
    '''
    :param Signal_List: 信号列表
    :param Sample_frequency: 采样频率
    :return:
            amp [list]: 幅度
            fre [list]: 频率坐标
            pha [list]: 相位
    '''

    try:
        #  fft计算
        fft_x = fft(Signal_List)
        # 纵坐标变换
        amp_x = abs(fft_x) / len(Signal_List) * 2
        # 生成频率坐标
        label_x = np.linspace(0, int(len(Signal_List) / 2) - 1, int(len(Signal_List) / 2))
        # 选取前半段计算结果即可
        amp = amp_x[0:int(len(Signal_List) / 2)]
        # 计算采样频率
        fs = Sample_frequency
        # 频率坐标变换
        fre = label_x / len(Signal_List) * fs
        # 计算相位角并去除2pi跃变
        pha = np.unwrap(np.angle(fft_x))

        return  amp,fre,pha
    except Exception as e :
        print("exception ： ", e)
        print("FFT计算错误")
        return 0, 0, 0, 0, 0

# 计算时域特征：包括最大值、最小值、均值、方差、有效值
def Get_Time_Domain_Features(Signal_List):
    '''
    :param Signal_List: 信号列表
    :return:
            max  : 最大值
            min  : 最小值
            mean : 平均值
            var  : 方差
            rms  : 有效值
    '''
    try:
        signal_max  = max(Signal_List)
        signal_min  = min(Signal_List)
        signal_mean = statistics.mean(Signal_List)
        signal_var  = statistics.variance(Signal_List)
        signal_rms  = math.sqrt(sum([x ** 2 for x in Signal_List]) / len(Signal_List))

        return signal_max,signal_min,signal_mean,signal_var,signal_rms
    except Exception as e :
        print("exception ： ", e)
        print("时域特征计算错误")
        return 0,0,0,0,0

# 计算频域特征：包括中值频率、均值频率、重心频率、均方频率、频率方差
def Get_Fre_Domain_Features(amp_list,fre_list = []):
    '''
    :param amp_list          : 幅度列表
    :param fre_list          : 频率列表
    :return:
            Median_frequency : 中值频率 —— 功率谱值中值
            Mean_frequency   : 均值频率 —— 功率谱值平均值
            Cog_frequency    : 重心频率 —— 用来描述信号在频谱中分量较大的信号成分的频率，反映信号功率谱的分布情况
            MSE_frequency    : 均方频率 —— 均方根频率：均方频率的算数平方根。均方根频率可以看做惯性半径，可以反馈出信号的频率分布
            Var_frequency    : 频率方差 —— 信号频率分布越离散，频率方差越大
    '''

    # 频谱分析指的是将信号做傅里叶变换从而进行分析，频谱分析是包括幅频谱和相频谱两张图的，最常用的是幅频谱

    # 能量信号和功率信号的分别：
    #   能量就是信号的平方在区间(-∞,+∞)上的积分
    #   功率就是能量与“无穷长的时间”的比值
    #   能量有限、功率为零的信号为能量信号；能量无限、功率有限的信号为功率信号
    #   现实世界中大部分信号：如温度、传感器电压信号均为功率信号

    # 频谱衍生的谱：
    #   （1）能量谱：能量谱也叫能量谱密度，能量谱密度描述了信号或时间序列的能量如何随频率分布。
    #               能量谱是原信号傅立叶变换的平方。
    #   （2）功率谱：功率谱是功率谱密度函数（PSD）的简称，它定义为单位频带内的信号功率。
    #               功率谱是针对功率信号来说的，维纳-辛钦定理证明了：一段信号的功率谱等于这段信号自相关函数的傅里叶变换
    #               求功率谱就有了两种方法：
    #                   （1）直接法：(傅立叶变换的平方)/(区间长度)
    #                   （2）相关函数法：自相关函数的傅里叶变换
    #   （3）倒频谱：信号功率谱对数值进行傅立叶逆变换的结果（信号→求功率谱→求对数→求傅里叶逆变换）
    #               频谱（功率谱）反应的频率特征点横坐标是频率f（Hz），在倒频谱中对应的特征点的横坐标是时间t（s），而f与t互为倒数。
    #               从这里也可以看出，虽然倒频谱也叫“频谱”，其横坐标却并不是频率，而是时间。
    #               1.方便提取、分析原频谱图上肉眼难以识别的周期性信号
    #                   倒频谱能较好地检测出功率谱上的周期成分，通常在功率谱上无法对边频的总体水平作出定量估计，而倒频谱对边频成分具有“概括”能力，
    #                   能较明显地显示出功率谱上的周期成分，将原来谱上成族的边频带谱线简化为单根谱线，便于观察，
    #                   而齿轮发生故障时的振动频谱具有的边频带一般都具有等间隔（故障频率）的结构，利用倒频谱这个优点，可以检测出功率谱中难以辨识的周期性信号。
    #               2.受传感器的测点位置及传输途径的影响小
    #                   这是倒频谱的第二个好处。对于布置在不同位置的传感器，由于传递路径不同，其功率谱也不相同。但在倒频谱上，
    #                   由于信号源的振动效应和传递途径的效应分离开来，代表齿轮振动特征的倒频率分量几乎完全相同，只是低倒频率段存在由于传递函数差异而产生的影响。
    #                   在进行倒频谱分析时，可以不必考虑信号测取时的衰减和标定系数所带来的影响。这一优点对于故障识别极为有用。

    # FFT和PSD都是表示的频谱特性，帮助我们找出峰值的位置，那么有了FFT为什么还要提出PSD？
    #   信号分为确定信号和随机信号，而确定信号又分为能量信号和功率信号，随机信号一定是功率信号。
    #   根据狄里赫利条件，能量信号可以直接进行傅里叶变换，而功率信号不行。
    #   对于无法做傅里叶变换的信号，只能走一步弯路，先求自相关，再做傅里叶。
    #   但是物理意义上就是功率谱了。不过总之得到了信号的频率特性。

    # 既然为什么随机信号的一次FFT没有意义却还能(傅立叶变换的平方)/(区间长度)得到功率谱？
    #   对随机信号直接做FFT的做法其实就是截断成能量信号进行处理，这种处理不符合随机信号定义
    #   但之所以这样做，是做短时频域分析下作的近似处理。

    try:

        # 求解功率谱
        power_spectrum_list = amp_list*amp_list/len(amp_list)

        # 求解中值频率
        power_spectrum_array = np.array(power_spectrum_list)
        Median_frequency = np.median(power_spectrum_array)
        # 求解均值频率
        Mean_frequency   = statistics.mean(power_spectrum_list)
        # 求解重心频率
        Cog_frequency    = sum(power_spectrum_list*amp_list)/sum(power_spectrum_list)
        # 求解均方频率
        MSE_frequency    = math.sqrt(sum(power_spectrum_list*amp_list*amp_list)/sum(power_spectrum_list))
        # 求解频率方差
        S = []
        for i in range(len(amp_list)):
            Pi = power_spectrum_list[i]
            Fi = amp_list[i]
            Si = Pi*((Fi-Cog_frequency)**2)
            S.append(Si)
        Var_frequency = sum(S)/sum(power_spectrum_list)

        return Median_frequency,Mean_frequency,Cog_frequency,MSE_frequency,Var_frequency
    except Exception as e :
        print("exception ： ", e)
        print("频域特征计算错误")
        return 0, 0, 0, 0, 0

if __name__ == '__main__':

    t, y = generate_audio_wave(2, TEST_SAMPLE_RATE, TEST_DURATION)

    plt.figure()
    plt.plot(t, y)
    plt.show()

    amp,fre,pha = Get_Signals_FFT(y, TEST_SAMPLE_RATE)
    print(Get_Fre_Domain_Features(amp))

    plt.figure()
    plt.plot(fre, amp)
    plt.title('Amplitute-Frequence-Curve')
    plt.ylabel('Amplitute / a.u.')
    plt.xlabel('Frequence / Hz')
    plt.show()
