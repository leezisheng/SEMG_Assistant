# -*- coding: UTF-8 -*-
'''
    @Project ：SEMG_Assistant
    @File    ：CurveDrawing.py
    @description：
        包括一些小的组件工具函数
    @Author  ：leeqingshui
    @Date    ：2023/1/13 4:56
'''

# =============================================== 导入库 ===============================================

import inspect
import ctypes


# ============================================== 全局变量 ==============================================




# ============================================== 函数定义 ==============================================

# 循环队列
class Queue:
    def __init__(self,size):
        # 以列表的最后一个元素作为队尾
        self.items = [None]*size  #长度占位 声明长度为size的数据区
        self.size =size  #队列的最大长度
        self.head = 0 #队头的索引
        self._length = 0 #记录队列的长度


    def is_empty(self):
        return self._length ==0 # items中实际是有元素的，没有真正pop,只是进行了封装

    def length(self):
        return self._length

    def push(self, item):
        if self.length() == self.size:
            raise ValueError("队列已满")
        else:
            idx = (self.head + self.length()) % self.size #要加入元素的索引
            self.items[idx] = item #赋值
            self._length += 1

    def pop(self):
        # 抛出队首元素
        if self.is_empty():
            raise ValueError("队列为空")
        else:
            value = self.items[self.head]
            self.head = (self.head +1) % self.size #出队之后的队头索引
            self._length -= 1
            return value#时间复杂度为O(1)

    def peek(self):
        if self.is_empty():
            raise ValueError("队列为空")
        return self.items[self.head]

# 异常抛出
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""

    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):
        exctype = type(exctype)

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

    if res == 0:

        raise ValueError("invalid thread id")

    elif res != 1:

        # """if it returns a number greater than one, you're in trouble,

        # and you should call it again with exc=NULL to revert the effect"""

        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

        raise SystemError("PyThreadState_SetAsyncExc failed")

# 停止线程
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

if __name__ == "__main__":
    queue = Queue(100)
    queue.push(1)  # 进入队列
    queue.push(2)
    queue.push(3)
    queue.push(5)
    queue.push(8)
    print(queue.length())  # 队列长度
    print(queue.peek())  # 队头元素
    print(queue.pop())  # 出队
    print(queue.pop())
    print(queue.pop())
    print(queue.items)#应该为空  但其实是有元素的 对使用者而言队列为空  封装
    # print(queue.pop())#注释测试





