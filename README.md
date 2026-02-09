
---

# Fingerprint Matching System based on OpenCV & SIFT

本项目是一个基于 **SIFT 特征点提取**与 **FLANN 快速匹配算法**的指纹识别系统。它能够从指纹数据库中自动检索与样本最匹配的真实指纹，并计算相似度。

---

## 🌟 项目亮点

* **抗干扰性强**：采用 SIFT 算法，即使指纹图像存在平移、旋转、缩放或轻微磨损（Hard 级别扰动），仍能精准匹配。
* **毫秒级检索**：利用 FLANN (Fast Library for Approximate Nearest Neighbors) 构建多叉树索引，大幅提升在大规模数据集中的搜索速度。
* **直观可视化**：自动绘制特征匹配连线（Mapping Lines），并实时显示匹配百分比。

---

## 🛠️ 核心算法流程

1. **特征点检测 (Minutiae Detection)**：通过 SIFT 算子捕捉指纹脊线的端点与分叉点。
2. **特征描述 (Description)**：为每个关键点生成 128 维的特征向量。
3. **最近邻匹配 (KNN Matching)**：在特征空间中寻找距离最近的两个特征点。
4. **Lowe's Ratio Test 筛选**：
* 通过公式：
* 剔除由于指纹纹路重复导致的伪匹配点。


5. **得分计算**：基于匹配点数与图像总特征点的比例得出相似度。

---

## 📂 环境配置

本项目需要以下依赖环境，请在终端执行：

```bash
pip install opencv-python numpy

```

> **注意**：建议使用 `opencv-python` 4.4.0 以上版本以获得更好的 SIFT 性能。

---

## 📊 数据集说明

本项目基于 **SOCOFing** (Sokoto Coventry Fingerprint Dataset) 进行开发。

* **数据来源**：[Kaggle SOCOFing Dataset](https://www.google.com/search?q=https://www.kaggle.com/datasets/belalalsayed/socofing)
* **说明**：由于数据集较大（约 500MB+），本项目仓库**不包含**指纹图片文件。请下载后按以下结构存放：
```text
├── main.py
└── SOCOFing/
    ├── Real/         # 存放 6000 张真实指纹
    └── Altered/      # 存放各种扰动后的指纹样本

```



---

## 🚀 运行指南

1. 克隆或下载本项目到本地。
2. 修改 `main.py` 中的 `sample_path` 和 `real_dir` 为你的本地路径。
3. 运行程序：
```bash
python main.py

```



### 预期结果示例

* **控制台输出**：实时显示当前检索进度及最终的最佳匹配文件名。
* **弹出窗口**：左侧为待识别指纹，右侧为检索到的最佳匹配，两者之间由彩色线段连接。

---

## 📈 后续优化方向 (Roadmap)

* [ ] **图像增强**：引入 Gabor 滤波器或 CLAHE 算法进一步提升低质量指纹的识别率。
* [ ] **几何校验**：加入 RANSAC 算法剔除空间逻辑错误的匹配点。
* [ ] **形态学处理**：增加指纹细化（Skeletization）预处理步骤。

---

## 📜 许可证

本项目采用 [MIT License](https://www.google.com/search?q=LICENSE) 开源协议。

