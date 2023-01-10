# 所使用到的库函数
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import math

Pi = 3.14

# 简单定义一个FFT函数
def myfft(x,t):
    fft_x = fft(x)                                            #  fft计算
    amp_x = abs(fft_x)/len(x)*2                               # 纵坐标变换
    label_x = np.linspace(0,int(len(x)/2)-1,int(len(x)/2))    # 生成频率坐标
    amp = amp_x[0:int(len(x)/2)]                              # 选取前半段计算结果即可
    fs =1/( t[2]-t[1])                                        # 计算采样频率
    fre = label_x/len(x)*fs                                   # 频率坐标变换
    pha = np.unwrap(np.angle(fft_x))                          # 计算相位角并去除2pi跃变
    return amp,fre,pha                                        # 返回幅度和频率

t = np.linspace(0,1,1024)                                     # 时间坐标
x = []

for i in range(0,1024):
    x.append(100 + 10*(math.sin(2*Pi*i*10/1024)) + 20*(math.sin(2*Pi*i*50/1024)) + 30*(math.sin(2*Pi*i*300/1024)))

amp,fre,pha= myfft(x,t)                                       # 调用函数

# 绘图
plt.figure()
plt.plot(t,x)
plt.title('Signal')
plt.xlabel('Time / s')
plt.ylabel('Intencity / cd')

plt.figure()
plt.plot(fre,amp)
plt.title('Amplitute-Frequence-Curve')
plt.ylabel('Amplitute / a.u.')
plt.xlabel('Frequence / Hz')
plt.show()


