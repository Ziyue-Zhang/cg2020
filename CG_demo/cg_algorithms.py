#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if(abs(x1-x0)>=abs(y1-y0)):
            length=abs(x1-x0)
        else:
            length=abs(y1-y0)
        if (length==0):
            result.append((x0,y0))
            return result
        dx=(float)(x1-x0)/length
        dy=(float)(y1-y0)/length
        i=1
        x=x0
        y=y0
        while(i<=length):
            result.append((int(x+0.5),int(y+0.5)))
            x=x+dx
            y=y+dy
            i+=1
    elif algorithm == 'Bresenham':
        dx=abs(x1-x0)
        dy=abs(y1-y0)
        if(dx==0 and dy==0):
            result.append((x0,y0))
            return result
        gradient_flag=0
        if(dx<dy):
            gradient_flag=1
        if(gradient_flag==1):
            x0,y0=y0,x0
            x1,y1=y1,x1
            dx,dy=dy,dx
        xx=1
        if(x1-x0<0):
            xx=-1
        yy=1
        if(y1-y0<0):
            yy=-1
        p=2*dy-dx
        x=x0
        y=y0
        result.append((x,y))
        while(x!=x1):
            if(p>=0):
                p+=2*dy-2*dx
                y+=yy
            else:
                p+=2*dy
            x+=xx
            if(gradient_flag):
                result.append((y,x))
            else:
                result.append((x,y))        
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    xx=int((x0+x1)/2)
    yy=int((y0+y1)/2)
    a=int((abs(x1-x0))/2)
    b=int((abs(y1-y0))/2)
    p=float(b**2+a**2*(0.25-b))
    x=0
    y=b
    result.append((xx+x,yy+y))
    result.append((xx-x,yy+y))
    result.append((xx+x,yy-y))
    result.append((xx-x,yy-y))
    while(b**2*x<a**2*y):
        if(p<0):
            p+=float(b**2*(2*x+3))
        else:
            p+=float(b**2*(2*x+3)-a**2*(2*y-2))
            y-=1
        x+=1
        result.append((xx+x,yy+y))
        result.append((xx-x,yy+y))
        result.append((xx+x,yy-y))
        result.append((xx-x,yy-y))
    p=float((b*(x+0.5))**2+(a*(y-1))**2-(a*b)**2)
    while(y>0):
        if(p<0):
            p+=float(b**2*(2*x+2)+a**2*(-2*y+3))
            x+=1
        else:
            p+=float(a**2*(-2*y+3))
        y-=1
        result.append((xx+x,yy+y))
        result.append((xx-x,yy+y))
        result.append((xx+x,yy-y))
        result.append((xx-x,yy-y))
    return result

def Bezier_point(n, t, control_point):
    while(n!=1):
        for i in range(0, n-1):
            x0,y0=control_point[i]
            x1,y1=control_point[i+1]
            x=float(x0*(1-t))+float(x1*t)
            y=float(y0*(1-t))+float(y1*t)
            control_point[i]=x,y
        n-=1
    return control_point[0]


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    control_point = []
    if algorithm == 'Bezier':
        m=76800
        for i in range(0, m):
            control_point=p_list
            t = float(i/m)
            x,y=Bezier_point(len(p_list), t, control_point)
            result.append((int(x+0.5),int(y+0.5)))
    elif algorithm == 'B-spline':
        n=len(p_list)
        if(n<4):
            print('请至少输入4个点')
        for i in range(0, n-3):
            x0,y0 = p_list[i]
            x1,y1 = p_list[i+1]
            x2,y2 = p_list[i+2]
            x3,y3 = p_list[i+3]
            p0 = float(-x0/6+x1/2-x2/2+x3/6)
            p1 = float(x0/2-x1+x2/2)
            p2 = float(-x0/2+x2/2)
            p3 = float(x0/6+2*x1/3+x2/6)
            q0 = float(-y0/6+y1/2-y2/2+y3/6)
            q1 = float(y0/2-y1+y2/2)
            q2 = float(-y0/2+y2/2)
            q3 = float(y0/6+2*y1/3+y2/6)
            m=50000
            for i in range(0, m):
                t = float(i/m)
                x = p0*t**3+p1*t**2+p2*t+p3
                y = q0*t**3+q1*t**2+q2*t+q3
                result.append((int(x+0.5),int(y+0.5)))
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x, y in p_list:
        result.append((x+dx,y+dy))
    return result



def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    angel=float(r*math.pi/180)
    cos=math.cos(angel)
    sin=math.sin(angel)
    result = []
    for x0, y0 in p_list:
        x1=int(float(x)+float((x0-x)*cos)-float((y0-y)*sin)+0.5)
        y1=int(float(y)+float((x0-x)*sin)+float((y0-y)*cos)+0.5)
        result.append((x1,y1))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x0, y0 in p_list:
        x1=int(float(x0*s)+float(x*(1-s))+0.5)
        y1=int(float(y0*s)+float(y*(1-s))+0.5)
        result.append((x1,y1))
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    if algorithm == 'Cohen-Sutherland':
        x0,y0 = p_list[0]
        x1,y1 = p_list[1]
        code1=0
        code2=0
        if(x0<x_min):
            code1+=1
        if(x0>x_max):
            code1+=2
        if(y0<y_min):
            code1+=4
        if(y0>y_max):
            code1+=8
        if(x1<x_min):
            code2+=1
        if(x1>x_max):
            code2+=2
        if(y1<y_min):
            code2+=4
        if(y1>y_max):
            code2+=8

        if((code1|code2)==0):
            result=p_list
        elif((code1&code2)!=0):
            result=[[0,0],[0,0]]
        else:
            code=code1|code2
            if(code&1):
                yy=int(float((x_min-x1)*(y0-y1)/(x0-x1))+float(y1)+0.5)
                if(x0<x_min):
                    x0=x_min
                    y0=yy
                elif(x1<x_min):
                    x1=x_min
                    y1=yy
            if(code&2):
                yy=int(float((x_max-x1)*(y0-y1)/(x0-x1))+float(y1)+0.5)
                if(x0>x_max):
                    x0=x_max
                    y0=yy
                elif(x1>x_max):
                    x1=x_max
                    y1=yy
            if(code&4):
                xx=int(float((y_min-y1)*(x0-x1)/(y0-y1))+float(x1)+0.5)
                if(y0<y_min):
                    x0=xx
                    y0=y_min
                elif(y1<y_min):
                    x1=xx
                    y1=y_min
            if(code&8):
                xx=int(float((y_max-y1)*(x0-x1)/(y0-y1))+float(x1)+0.5)
                if(y0>y_max):
                    x0=xx
                    y0=y_max
                elif(y1>y_max):
                    x1=xx
                    y1=y_max
            code1=0
            code2=0
            if(x0<x_min):
                code1+=1
            if(x0>x_max):
                code1+=2
            if(y0<y_min):
                code1+=4
            if(y0>y_max):
                code1+=8
            if(x1<x_min):
                code2+=1
            if(x1>x_max):
                code2+=2
            if(y1<y_min):
                code2+=4
            if(y1>y_max):
                code2+=8
            if((code1|code2)==0):
                result=[[x0,y0], [x1,y1]]
            else:
                result=[[0,0],[0,0]]

    elif algorithm == 'Liang-Barsky':
        x0,y0 = p_list[0]
        x1,y1 = p_list[1]
        p=[x0-x1,x1-x0,y0-y1,y1-y0]
        q=[x0-x_min,x_max-x0,y0-y_min,y_max-y0]
        u1=float(0)
        u2=float(1)
        flag=False
        for i in range(0,4):
            if(p[i]==0 and q[i]<0):
                flag=True
            else:
                if(p[i]==0):
                    continue
                r=float(q[i]/p[i])
                if(p[i]<0):
                    u1=max(u1,r)
                else:
                    u2=min(u2,r)
                if(u1>u2):
                    flag=True
        if(flag==False):
            xx0=int(x0+u1*(x1-x0)+0.5)
            yy0=int(y0+u1*(y1-y0)+0.5)
            xx1=int(x0+u2*(x1-x0)+0.5)
            yy1=int(y0+u2*(y1-y0)+0.5)
            result=[[xx0,yy0],[xx1,yy1]]
        else:
            result=[[0,0],[0,0]]
    return result
