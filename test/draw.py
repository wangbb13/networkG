# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
mpl.rcParams['axes.unicode_minus'] = False


def draw_plot(x, DL, DS, DT, DG, filename, y_title):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号
    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    , 
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,5))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框
    
    plt.plot(x,DL,"b--",marker="*", label="LFR",linewidth=2)
    plt.plot(x,DS,"r-",marker="D", label="SNG",linewidth=2)
    plt.plot(x,DT,"g--",marker="^", label="TrillionG",linewidth=2)
    plt.plot(x,DG,"k-",marker="o", label="gMark",linewidth=2)
    
    group_labels=['1k','2k','3k','4k','5k',' 6k','7k','8k','9k','10k'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    # plt.title("diameter",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("number of nodes",fontsize=13,fontweight='bold')
    plt.ylabel(y_title,fontsize=13,fontweight='bold')
    plt.xlim(1,10)         #设置x轴的范围
    #plt.ylim(0.5,1)
    
    # plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细
    
    plt.savefig(filename,format='png')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()


def diameter():
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    DL = np.array([4, 4, 3, 3, 3, 3, 3, 3, 3, 3])
    DS = np.array([16, 13, 18, 11, 13, 15, 16, 15, 12, 14])
    DT = np.array([10, 10, 12, 12, 14, 16, 12, 11, 15, 18])
    DG = np.array([12, 11, 11, 13, 13, 12, 12, 12, 12, 12])
    draw_plot(x, DL, DS, DT, DG, "diameter.png", "diameter")


def avg_path_len():
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    DL = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    DS = np.array([5, 4, 5, 3, 4, 4, 4, 4, 4, 4])
    DT = np.array([3, 3, 3, 3, 4, 4, 4, 3, 4, 4])
    DG = np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    draw_plot(x, DL, DS, DT, DG, "avgPathLen.png", "average path length")


def avg_cc():
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    DL = np.array([0.12263062, 0.119376035, 0.11667116, 0.111405551, 0.11051078, 0.1077789, 0.107841426, 0.111552333, 0.11129218, 0.102659616])
    DS = np.array([0.051878315, 0.043563079, 0.03901166, 0.03866596, 0.026656672, 0.036764383, 0.02718568, 0.02738377, 0.032224568, 0.028402009])
    DT = np.array([0.171852848, 0.129174024, 0.084942625, 0.102731617, 0.043906096, 0.058978161, 0.05957286, 0.086405551, 0.032040357, 0.034554105])
    DG = np.array([0.389097583, 0.394812052, 0.412859739, 0.37119985, 0.351358423, 0.367507493, 0.362061921, 0.358620592, 0.367281716, 0.350085709244901])
    draw_plot(x, DL, DS, DT, DG, "avgCC.png", "average cluster coefficient")


def thousnads():
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2 - 1, 1.01 * height, '%s' % int(height))
    
    sng = [22.91, 47.88, 79.04, 98.82, 126.93, 155.86, 180.98, 215.12, 237.09, 253.68]
    trg = [46.28, 100.37, 121.67, 198.82, 180.96, 250.2, 331.34, 411.18, 309.92, 374.63]


    name=['100k','200k','30k','400k','500k','600k','700k', '800k', '900k', '1000k']
    
    total_width, n = 1.6, 2  
    width = total_width / n 
    x = list(range(0, 40, 4))
    
    plt.figure(figsize=(10,5))
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框
    
    a=plt.bar(x, sng, width=width, label='SNG',fc = 'r')
    for i in range(len(x)):  
        x[i] = x[i] + width
    b=plt.bar(x, trg, width=width, label='TrillionG',fc = 'g')
    

    autolabel(a)
    autolabel(b)
    
    group_labels=['100','200','300','400','500',' 600','700','800','900','1000'] #x轴刻度的标识
    plt.xticks(x,group_labels) #默认字体大小为10

    plt.xlabel('the number of nodes')
    plt.ylabel('execute time (seconds) ')
    # plt.title(u'学生成绩')
    plt.legend()

    plt.savefig('scalability.png',format='png')
    plt.show()


def show_edges():
    expect = np.array([400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000])
    sng = np.array([394.2614, 790.2288, 1216.8774, 1580.0531, 1982.5544, 1982.5544, 2790.5981, 3205.9797, 3570.7014, 3999.4742])
    trg = np.array([353.8361, 708.5277, 754.8614, 1425.5824, 985.9741, 1514.6847, 2166.3132, 2857.8004, 1537.7011, 1979.2572])

    x = np.array([1,2,3,4,5,6,7,8,9,10])

    plt.figure(figsize=(10,5))
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框
    
    plt.plot(x,expect,"b--",marker="*", label="Expect",linewidth=2)
    plt.plot(x,sng,"r-",marker="D", label="SNG",linewidth=2)
    plt.plot(x,trg,"g--",marker="^", label="TrillionG",linewidth=2)
    
    
    group_labels=['100','200','300','400','500',' 600','700','800','900','1000'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    # plt.title("diameter",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("number of nodes",fontsize=13,fontweight='bold')
    plt.ylabel("number of edges",fontsize=13,fontweight='bold')
    plt.xlim(1,10)         #设置x轴的范围
    #plt.ylim(0.5,1)
    
    # plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细
    
    plt.savefig('edges.png',format='png')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()



def main():
    # diameter()
    # avg_path_len()
    # avg_cc()
    # thousnads()
    # show_edges()


if __name__ == '__main__':
    main()
