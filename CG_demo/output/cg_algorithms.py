#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def sign(x):
    if x < 0: 
        return -1
    elif x == 0:
        return 0
    elif x > 0:
        return 1
        
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
        if abs(x1 - x0) >= abs(y1 - y0):
            length = abs(x1 - x0) * 1.0
        else:
            length = abs(y1 - y0) * 1.0
        delt_x = (x1 - x0) / length
        delt_y = (y1 - y0) / length
        x = x0 + 0.5
        y = y0 + 0.5
        i = 1
        while i <= length:
            result.append((math.floor(x), math.floor(y)))
            x = x + delt_x
            y = y + delt_y
            i = i + 1
    elif algorithm == 'Bresenham':
        x = x0
        y = y0
        delta_x = abs(x1 - x0)
        delta_y = abs(y1 - y0)
        s1 = sign(x1 - x0)
        s2 = sign(y1 - y0)
        if delta_y > delta_x:
            temp = delta_x
            delta_x = delta_y
            delta_y = temp
            interchange = 1
        else:
            interchange = 0
        e = 2 * delta_y - delta_x
        for i in range (1, delta_x + 1):
            result.append((x, y))
            while e > 0:
                if interchange == 1:
                    x = x + s1
                else:
                    y = y +s2
                e = e - 2 * delta_x
            if interchange == 1:
                y = y + s2
            else:
                x = x + s1
            e = e + 2 * delta_y
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形 

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    " TODO: boundary bug "
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
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    a = (x1 - x0) / 2
    b = (y1 - y0) / 2
    d = b * b + a * a * (0.25 - b)
    x = 0
    y = b
    
    result.append((xc + x, yc + y))
    result.append((xc + x, yc - y))
    result.append((xc - x, yc - y))
    result.append((xc - x, yc + y))
    
    while b * b * (x + 1) < a * a * (y - 0.5):
        if d < 0:
            d = d + b * b * (2 * x + 3)
        else:
            d = d + b * b * (2 * x + 3) + a * a * ((-2) * y + 2)
            y = y - 1
        x = x + 1
        result.append((xc + x, yc + y))
        result.append((xc + x, yc - y))
        result.append((xc - x, yc - y))
        result.append((xc - x, yc + y))

    while y > 0:
        if d < 0:
            d = d + b * b * (2 * x + 2) + a * a * ((-2) * y + 3)
            x = x + 1
        else:
            d = d + a * a * ((-2) * y + 3)
        y = y - 1
        result.append((xc + x, yc + y))
        result.append((xc + x, yc - y))
        result.append((xc - x, yc - y))
        result.append((xc - x, yc + y))
   
    return result
   

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
    
    
def binomial(n, i):
    a = factorial(n)
    b = factorial(i) * factorial(n - i)
    return a / b
    
    
def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        n = len(p_list) - 1
        for i in range(0, 1000):
            t = i / 1000.0
            x = 0
            y = 0
            for j in range(len(p_list)):
                x0, y0 = p_list[j]
                p = binomial(n, j)
                x = x + p * x0 * math.pow(t, j) * math.pow(1 - t, n - j)
                y = y + p * y0 * math.pow(t, j) * math.pow(1 - t, n - j) 
            result.append((int(x),int(y)))
    else:
        for i in range(len(p_list) - 3):
            delta = 0.01
            t = 0
            while t <= 1:
                b0 = 1 / 6.0 * (1 - t) * (1 - t) * (1 - t)
                b1 = 1 / 6.0 * (3 * t * t * t - 6 * t * t + 4)
                b2 = 1 / 6.0 * ((-3) * t * t * t + 3 * t * t + 3 * t + 1)
                b3 = 1 / 6.0 * t * t * t
                x1, y1 = p_list[i]
                x2, y2 = p_list[i + 1]
                x3, y3 = p_list[i + 2]
                x4, y4 = p_list[i + 3]
                x = b0 * x1 + b1 * x2 + b2 * x3 + b3 * x4
                y = b0 * y1 + b1 * y2 + b2 * y3 + b3 * y4
                result.append((int(x), int(y)))
                t = t + delta
        
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x0 = x0 + dx
        y0 = y0 + dy
        result.append((x0, y0))
    return result

def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    print(r)
    sint = math.sin(math.pi * r / 180)
    cost = math.cos(math.pi * r / 180)
    print(sint)
    print(cost)
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        print("--------")
        print(x0)
        print(y0)
        print("--------")
        x0 = x + (x0 - x) * cost - (y0 - y) * sint
        y0 = y + (x0 - x) * sint + (y0 - y) * cost
        print(x0)
        print(y0)
        result.append((int(x0), int(y0)))
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
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x0 = x0 * s + x * (1 - s)
        y0 = y0 * s + y * (1 - s)
        print(x0)
        print(y0)
        result.append((int(x0), int(y0)))
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
    pass
