import pygetwindow as gw
from PIL import ImageGrab, Image
import time
import cv2
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# # Step 1: 获取所有打开的窗口
# windows = gw.getAllTitles()  # 获取所有窗口标题
# print("所有打开的窗口:", windows)
#
# # Step 2: 查找特定窗口的句柄
# window_title = input("请输入要截取的窗口标题: ")
# window = gw.getWindowsWithTitle(window_title)[0]  # 获取特定标题的窗口
#
# # 等待窗口激活
# time.sleep(1)
#
# # 获取窗口的左上角坐标和窗口大小
# left, top, width, height = window.left, window.top, window.width, window.height
# print(f"窗口坐标: ({left}, {top}), 宽度: {width}, 高度: {height}")
#
# # Step 4: 截取窗口区域
# bbox = (left+8, top+31, left + width-8, top + height-8)
# print(bbox)
# screenshot = ImageGrab.grab(bbox=bbox)

# Step 5: 保存并显示截图
# screenshot.save("window_screenshot.png")
# screenshot.show()

# # 初始化全局变量
# start_point = None
# end_point = None
# drawing = False
# regions = []  # 存储所有选择的区域
#
# # 实线绘制函数
# def draw_rectangle(img, start, end, color=(0, 255, 0), thickness=2):
#     cv2.rectangle(img, start, end, color, thickness)
#
# # 鼠标回调函数
# def draw_selection(event, x, y, flags, param):
#     global start_point, end_point, drawing, image_copy, regions
#
#     if event == cv2.EVENT_LBUTTONDOWN:  # 按下鼠标左键
#         drawing = True
#         start_point = (x, y)
#         end_point = None  # 重置结束点
#
#     elif event == cv2.EVENT_MOUSEMOVE:  # 鼠标移动
#         if drawing:
#             end_point = (x, y)
#             image_copy = image.copy()  # 每次绘制前复制原图
#             draw_rectangle(image_copy, start_point, end_point)  # 绘制实线矩形
#             cv2.imshow("Image", image_copy)  # 更新窗口
#
#     elif event == cv2.EVENT_LBUTTONUP:  # 松开鼠标左键
#         drawing = False
#         end_point = (x, y)
#         draw_rectangle(image, start_point, end_point)  # 在原图上绘制实线
#         regions.append((start_point, end_point))  # 添加当前选择区域到列表
#         cv2.imshow("Image", image)  # 更新窗口
#
# # 载入图片
# image_path = 'window_screenshot.png'  # 替换为你的图片路径
# image = cv2.imread(image_path)
# image_copy = image.copy()  # 复制原图用于绘制
#
# # 创建窗口并设置鼠标回调
# cv2.namedWindow("Image")
# cv2.setMouseCallback("Image", draw_selection)
#
# while True:
#     cv2.imshow("Image", image)
#
#     if cv2.waitKey(1) & 0xFF == 27:  # 按 Esc 键退出
#         break
#
# # 打印坐标
# print("选择的区域坐标：")
# for idx, (start, end) in enumerate(regions):
#     print(f"区域 {idx + 1}:")
#     print("起始点:", start)
#     print("结束点:", end)
#
# cv2.destroyAllWindows()

class Graywindow:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def get_main_screen_window():
    """Return the window coordinates for the main gameplay area."""
    return Graywindow(0, 0, 1600, 900)

def calculate_relative_coordinates(window_offset):
    """Calculate absolute window coordinates based on main screen coordinates and offsets."""
    main_window = get_main_screen_window()

    # Get main screen coordinates
    main_x1, main_y1, main_x2, main_y2 = main_window.x1, main_window.y1, main_window.x2, main_window.y2

    # Calculate the absolute coordinates of the window
    x1 = main_x1 + window_offset[0][0]
    y1 = main_y1 + window_offset[0][1]
    x2 = main_x1 + window_offset[1][0]
    y2 = main_y1 + window_offset[1][1]

    return (x1, y1, x2, y2)


# Define offsets for each window
self_blood_offset = ((139, 652), (290, 664))  # Example offsets for (top-left, bottom-right)
self_energy_offset = ((140, 678), (258, 684))
self_magic_offset = ((139, 666), (298, 677))
boss_blood_offset = ((510, 604), (781, 618))
skill_1_offset = ((1099, 530), (1130, 564))  # Top-left and bottom-right for skill 1
skill_2_offset = ((1136, 530), (1168, 565))  # Top-left and bottom-right for skill 2

# Calculate absolute coordinates
self_blood_coords = calculate_relative_coordinates(self_blood_offset)
self_energy_coords = calculate_relative_coordinates(self_energy_offset)
self_magic_coords = calculate_relative_coordinates(self_magic_offset)
boss_blood_coords = calculate_relative_coordinates(boss_blood_offset)
skill_1_coords = calculate_relative_coordinates(skill_1_offset)
skill_2_coords = calculate_relative_coordinates(skill_2_offset)

def plot_windows_on_image(image_path, main_window_coords, window_coords):
    # Load the image
    img = Image.open(image_path)

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Display the image
    ax.imshow(img)

    # Draw the main screen window
    main_rect = patches.Rectangle((main_window_coords[0], main_window_coords[1]),
                                  main_window_coords[2] - main_window_coords[0],
                                  main_window_coords[3] - main_window_coords[1],
                                  linewidth=2, edgecolor='blue', facecolor='none', label='Main Screen Window')
    ax.add_patch(main_rect)

    # Draw all other windows
    window_labels = ['Self Blood', 'Self Energy', 'Self Magic', 'Boss Blood', 'Skill 1', 'Skill 2']
    for (coords, label) in zip(window_coords, window_labels):
        rect = patches.Rectangle((coords[0], coords[1]),
                                 coords[2] - coords[0],
                                 coords[3] - coords[1],
                                 linewidth=2, edgecolor='red', facecolor='none', label=label)
        ax.add_patch(rect)
        # Add label in the center of the rectangle
        ax.text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, label,
                horizontalalignment='center', verticalalignment='center', fontsize=9, color='black')

    # Set limits and labels
    ax.set_xlim(0, img.width)
    ax.set_ylim(img.height, 0)  # Invert y-axis to match image coordinates
    ax.set_title('Game UI Windows Overlay')
    ax.axis('off')  # Hide the axes
    plt.show()


# Assuming you have these coordinates from previous calculations
main_window_coords = (0, 0, 1600, 900)  # Main screen window coordinates
window_coords = [
    self_blood_coords,  # Self Blood
    self_energy_coords,  # Self Energy
    self_magic_coords,  # Self Magic
    boss_blood_coords,  # Boss Blood
    skill_1_coords,  # Skill 1
    skill_2_coords  # Skill 2
]

# Provide the path to your image file
image_path = 'window_screenshot.png'  # Replace with your image path

# Call the plotting function
plot_windows_on_image(image_path, main_window_coords, window_coords)
