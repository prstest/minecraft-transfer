import pygetwindow as gw
import win32gui
import pyautogui
import time
import re
import pyperclip

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
        with open(file_path, 'r', encoding='GBK') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    serial = parts[0].strip()
                    content = parts[1].strip()
                    # 转换为浮点数后取整数部分
                    x = int(float(parts[2].strip()))
                    y = int(float(parts[3].strip()))
                    z = int(float(parts[4].strip()))
                    coordinate.append((serial, content, x, y, z))
                else:
                    print(f"格式错误：{line.strip()} 需要5个部分，但找到了{len(parts)}个部分")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return coordinate

# 读取文件内容
coordinate_list = read_coordinate('coordinate.txt')

print("================维度================")
print("0：提取当前坐标")
print("1：当前世界")
print("2：主世界")
print("3：末地")
print("4：地狱")
print("================坐标================")
for serial, content, x, y, z in coordinate_list:
    print(f"{serial}: {content} ({x}, {y}, {z})")
if not coordinate_list:
    print("坐标列表为空，请检查文件内容和格式。")
    exit()

while True:
    # 获取当前活动窗口的标题
    current_title = check_active_window()
    try:
        user_dimensionality = int(input("请输入维度："))
    except ValueError:
        print("输入错误，请输入有效的数字。")
        continue

    if user_dimensionality == 0:
        time.sleep(3)
        pyautogui.hotkey('f3', 'c')
        clipboard_content = pyperclip.paste()
        pattern = r'tp @s (-?\d+\.\d+) (-?\d+\.\d+) (-?\d+\.\d+)'
        match = re.search(pattern, clipboard_content)
        if match:
            x, y, z = map(int, map(float, match.groups()))
            # 将坐标信息拼接成字符串
            a = f"{x}, {y}, {z}"
            next_serial = str(len(coordinate_list) + 1)
            add_name = input("请输入坐标名字: ")
            coordinate_list.append((next_serial, add_name, x, y, z))
            with open("coordinate.txt", 'a') as file:
                write_ip = f"{next_serial}, {add_name}, {x},{y},{z}\n"
                print(write_ip)
                file.write(write_ip)
        continue
    user_input = input("请输入序号或内容: ")
    if user_dimensionality not in [0, 1, 2, 3, 4]:
        print("输入错误，程序已退出")
        break
    if user_input:
        matched = False
        for serial, content, x, y, z in coordinate_list:
            if user_input == serial or user_input == content:
                time.sleep(1)
                current_title = check_active_window()
                if current_title and target_pattern.search(current_title):
                    time.sleep(1)
                    pyautogui.hotkey('/')
                    dimension = ""
                    if user_dimensionality == 1:
                        pyautogui.write(f"tp {x} {y} {z}", interval=0)
                        dimension = "当前世界"
                    elif user_dimensionality == 2:
                        pyautogui.write(f"execute in minecraft:overworld run tp {x} {y} {z}", interval=0)
                        dimension = "主世界"
                    elif user_dimensionality == 3:
                        pyautogui.write(f"execute in minecraft:the_end run tp {x} {y} {z}", interval=0)
                        dimension = "末地"
                    elif user_dimensionality == 4:
                        pyautogui.write(f"execute in minecraft:the_nether run tp {x} {y} {z}", interval=0)
                        dimension = "地狱"
                    pyautogui.press('enter')
                    print(f"维度：{dimension}")
                    print(f"已传送到: {content} 坐标为 ({x}, {y}, {z})")
                    matched = True
                    break
                else:
                    print("找不到Minecraft窗口，操作中止。")
                    matched = True

        if not matched:
            print("输入的序号或内容未找到，请检查输入是否正确。")
    else:
        print("未找到活动窗口，请确保目标窗口是活动状态。")
