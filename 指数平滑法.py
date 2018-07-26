import numpy as np
import matplotlib.pyplot as plt


'''
一次移动平均实际上认为最近 N 期数据对未来值影响相同，都加权
1/N；而 N 期以前的数据对未来值没有影响，加权为 0。但是，二次及更高次移动平均数的权数却不
是1/N，且次数越高，权数的结构越复杂，但永远保持对称的权数，即两端项权数小，
中间项权数大，不符合一般系统的动态性。一般说来历史数据对未来值的影响是随时间
间隔的增长而递减的。所以，更切合实际的方法应是对各期观测值依时间顺序进行加权
平均作为预测值。指数平滑法可满足这一要求，而且具有简单的递推形式。
指数平滑法根据平滑次数的不同，又分为一次指数平滑法、二次指数平滑法和三
次指数平滑法等，分别介绍如下。
'''

# 一次指数平滑法
'''
当时间序列的数据较多，比如在 20 个以上时，初始值对以
后的预测值影响很少，可选用第一期数据为初始值。如果时间序列的数据较少，在 20
个以下时，初始值对以后的预测值影响很大，这时，就必须认真研究如何正确确定初始
值。一般以最初几期实际值的平均值作为初始值。

使用没有明显趋势数据
'''
# 模拟数据
data = [50, 52, 47, 51, 49, 48, 51, 40, 48, 52, 51, 59]
data_index = np.array(range(1, len(data) + 1))  # 索引，作图用
data_np = np.array(data, dtype=np.float)  # 转成数组
plt.plot(data_index, data_np, color='b', linewidth=2, label='原始数据')  # 原始数据展示
plt.show()

# 初始值
# a指数平滑法
a = 0.2
s01 = sum(data_np[0:2]) / 2
y1 = s01  # 第一个预测初始值
'''
计算方法
y2 = a * data_np[0] + (1 - a) * y1
y3 = a * data_np[1] + (1 - a) * y2
'''
out = [y1]  # 结果赋值初始化数据
for x in range(0, len(data_np)):  # 最后一个数据为预测数据
    predict = a * data_np[x] + (1 - a) * out[-1]
    out.append(predict)
out_np = np.array(out)  # 输出数据转np
s = sum((out_np[:-1] - data_np)**2 / len(data_np))**0.5  # 预测标准误差


# 指数平滑函数
def moav_index(data_np, y1, a)->(np.array, float):
    '''
    输入目标数组，初始值，平滑指数
    返回，一次平滑值，和标准误差
    '''
    out = [y1]  # 结果赋值初始化数据
    for x in range(0, len(data_np)):  # 最后一个数据为预测数据
        predict = a * data_np[x] + (1 - a) * out[-1]
        out.append(predict)
    out_np = np.array(out)  # 输出数据转np
    s = sum((out_np[:-1] - data_np)**2 / len(data_np))**0.5  # 预测标准误差
    return(out_np, s)


# 二次指数平滑
'''
一次指数平滑法虽然克服了移动平均法的缺点。但当时间序列的变动出现直线趋
势时，用一次指数平滑法进行预测，仍存在明显的滞后偏差。因此，也必须加以修正。
修正的方法与趋势移动平均法相同，即再作二次指数平滑，利用滞后偏差的规律建立直
线趋势模型。这就是二次指数平滑法。
'''
# 模拟数据
data = [676, 825, 774, 716, 940, 1159, 1384, 1524, 1668, 1688, 1958,
        2031, 2234, 2566, 2820, 3006, 3093, 3277, 3514, 3770, 4107]
data_index = np.array(range(1, len(data) + 1))  # 索引，作图用
data_np = np.array(data, dtype=np.float)  # 转成数组
plt.plot(data_index, data_np, color='b', linewidth=2, label='原始数据')  # 原始数据展示
plt.show()

# 一次平滑计算
alf = 0.3
a, b = moav_index(data_np, data_np[0], alf)
# 二次平滑计算
c, d = moav_index(a[1:], a[1], alf)
# 直线趋势模型

at = 2 * a[-1] - c[-1]
bt = alf / (1 - alf) * (a[-1] - c[-1])
# 预测数据
y22 = at + bt * 1
y23 = at + bt * 2
