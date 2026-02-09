import os
import cv2
import numpy as np

# 1. 初始化 SIFT 探测器
# SIFT 会寻找图像中的关键点（如脊线的分叉、端点）并生成描述符
sift = cv2.SIFT_create()

# 2. 读取待识别的样本图像（Altered 文件夹中的图）
# 使用 r"" 原始字符串防止转义字符冲突
sample_path = r"D:\python\FingerPrintMatching\SOCOFing\Altered\Altered-Medium\157__M_Right_index_finger_Obl.BMP"
sample = cv2.imread(sample_path)

# 安全检查：防止路径错误导致程序崩溃
if sample is None:
    print(f"无法读取样本图像: {sample_path}")
    exit()

# 预先计算样本图的关键点 (kp1) 和描述符 (des1)
# 描述符是关键点周围纹理特征的数学总结，用于后续比对
kp1, des1 = sift.detectAndCompute(sample, None)

# 初始化最佳匹配相关的变量
best_score = 0      # 最高匹配得分
filename = None    # 匹配到的文件名
image = None       # 匹配到的图像数据
kp2_best, mp_best = None, None  # 最佳匹配项的关键点和匹配点对

# 3. 准备遍历 Real（真实指纹）数据库
real_dir = r"D:\python\FingerPrintMatching\SOCOFing\Real"
file_list = os.listdir(real_dir)

print("开始比对...")
for counter, file in enumerate(file_list):
    # 每处理 100 张图打印一次进度
    if counter % 100 == 0:
        print(f"已处理: {counter}")

    # 拼接数据库中图片的完整路径
    target_path = os.path.join(real_dir, file)
    fingerprint_image = cv2.imread(target_path)

    if fingerprint_image is None:
        continue  # 如果读取失败，跳过此文件

    # 提取数据库中当前图片的特征点 (kp2) 和描述符 (des2)
    kp2, des2 = sift.detectAndCompute(fingerprint_image, None)
    
    # 健壮性检查：如果图片太模糊提取不到特征，直接跳过
    if des1 is None or des2 is None:
        continue

    # 4. 配置 FLANN 匹配器
    # FLANN 是在大数据集中寻找最近邻特征点的快速算法
    index_params = dict(algorithm=1, trees=10) # 使用 K-D 树算法
    search_params = dict(checks=50)            # 检查次数，值越大越准但越慢
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    try:
        # 使用 K-近邻匹配，找到最相似的 2 个点
        matches = flann.knnMatch(des1, des2, k=2)
    except Exception as e:
        continue

    # 5. 筛选匹配点 (Lowe's ratio test)
    # 只有当最近的点显著优于次近的点时，才认为是一个可靠的匹配
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]
            
    # 计算得分：匹配成功的点数 / 两图中最少关键点数 * 100
    # 这种方式衡量了图像的重合度
    num_keypoints = min(len(kp1), len(kp2))
    if num_keypoints > 0:
        score = len(good_matches) / num_keypoints * 100
        
        # 如果当前得分高于历史最高分，则更新记录
        if score > best_score:
            best_score = score
            filename = file
            image = fingerprint_image
            kp2_best, mp_best = kp2, good_matches

# 6. 显示比对结果
if filename:
    print(f'\n比对完成！')
    print(f'最佳选项 (数据库文件名): {filename}')
    print(f'最高匹配率: {best_score:.2f}%')

    # 将两张图画在一起，用线条连接匹配的特征点
    # flags=2 表示只画出匹配点，不画所有关键点，界面更整洁
    result = cv2.drawMatches(sample, kp1, image, kp2_best, mp_best, None, flags=2)
    
    # 调整结果图大小，方便在屏幕查看
    result = cv2.resize(result, None, fx=2, fy=2) 
    cv2.imshow("Fingerprint Matching Result", result)
    
    # 等待用户按任意键关闭窗口
    cv2.waitKey(0) 
else:
    print("在数据库中未发现匹配项")

cv2.destroyAllWindows()