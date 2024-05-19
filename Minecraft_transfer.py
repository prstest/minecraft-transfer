import pygetwindow as gw
import win32gui
import pyautogui
import time
import re

# 要匹配的窗口标题的正则表达式模式
target_pattern = re.compile(r"Minecraft \d+\.\d+\.\d+")

# 定义一个函数来检查当前活动窗口的标题
def check_active_window():
    try:
        # 获取当前活动窗口的句柄
        active_window_handle = win32gui.GetForegroundWindow()
        # 获取当前活动窗口的标题
        if active_window_handle:
            active_window = gw.Window(active_window_handle)
            active_window_title = active_window.title
            return active_window_title
    except Exception as e:
        print(f"获取活动窗口时发生错误: {e}")
    return None

# 定义一个函数来读取文件内容并返回输入数据列表
def read_coordinate(file_path):
    coordinate = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    serial = parts[0].strip()
                    content = parts[1].strip()
                    x = int(parts[2].strip())
                    y = int(parts[3].strip())
                    z = int(parts[4].strip())  # 解析Z轴坐标
                    coordinate.append((serial, content, x, y, z))
                else:
                    print(f"格式错误：{line.strip()} 需要5个部分，但找到了{len(parts)}个部分")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return coordinate

# 读取文件内容
print("================维度================")
print("0：当前世界")
print("1：主世界")
print("2：末地")
print("3：地狱")
print("================坐标================")
coordinate_list = read_coordinate('coordinate.txt')
if not coordinate_list:
    print("坐标列表为空，请检查文件内容和格式。")
    exit()

for serial, content, x, y, z in coordinate_list:
    print(f"{serial}: {content} - 位置({x}, {y}, {z})")
while True:
    # 获取当前活动窗口的标题
    current_title = check_active_window()
    print("")
    user_dimensionality = int(input("请输入维度："))
    user_input = input("请输入序号或内容: ")
    if user_input:
        matched = False
        for serial, content, x, y, z in coordinate_list:
            if user_input == serial or user_input == content:
                # 在执行操作之前再次检查当前活动窗口
                time.sleep(1)
                current_title = check_active_window()
                if current_title and target_pattern.search(current_title):
                    time.sleep(1)
                    pyautogui.hotkey('/')
                    dimension = ""
                    if user_dimensionality == 0:
                        pyautogui.write(f"tp  {x} {y} {z}", interval=0)
                        dimension = "当前世界"
                    elif user_dimensionality == 1:
                        pyautogui.write(f"execute in minecraft:overworld run tp  {x} {y} {z}", interval=0)
                        dimension = "主世界"
                    elif user_dimensionality == 2:
                        pyautogui.write(f"execute in minecraft:the_end run tp {x} {y} {z}", interval=0)
                        dimension = "末地"
                    elif user_dimensionality == 3:
                        pyautogui.write(f"execute in minecraft:the_nether run tp  {x} {y} {z}", interval=0)
                        dimension = "地狱"
                    pyautogui.press('enter')
                    print(f"维度：{dimension}")
                    print(f"已传送到: {content} 坐标为 ({x}, {y}, {z})")
                    matched = True
                    break
                else:
                    print("找不到Minecraft窗口，操作中止。")
                    matched = True
        if matched == False:
            print("输入的序号或内容未找到，请检查输入是否正确。")
    else:
        print("未找到活动窗口，请确保目标窗口是活动状态。")
    
    # 短暂延时以避免高CPU占用
    time.sleep(1)
