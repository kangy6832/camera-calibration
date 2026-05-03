# 🎥 相机标定系统

通过棋盘格标定图片自动标定相机的内参和畸变系数。

## 📁 项目结构

```
相机标定/
├── data/           # 放置标定图片（棋盘格照片）
├── output/         # 输出标定结果
├── src/            # 源代码
│   ├── calibration.py   # 核心标定算法
│   ├── utils.py         # 工具函数
│   └── visualize.py     # 结果可视化
├── requirements.txt # 依赖列表
├── README.md        # 项目说明
└── main.py          # 主程序入口
```

## 🛠️ 使用步骤

### 1. 准备标定图片
- 使用棋盘格 (例如 8x6 格子)
- 拍摄 20-30 张不同角度的图片
- 将图片放入 `data/` 目录

### 2. 运行标定
```bash
source venv/bin/activate
python main.py
```

### 3. 查看结果
- 标定结果保存在 `output/calibration_result.json`
- 验证图片和报告在 `output/` 目录

## 📊 输出结果

标定完成后会输出：
- 相机内参矩阵 (Camera Matrix)
- 畸变系数 (Distortion Coefficients)
- 重投影误差 (Reprojection Error)
- 标定质量评估

## ✨ 当前步骤
- ✅ 项目结构已创建
- ✅ 虚拟环境已配置
- ✅ 依赖包已安装
- ⏳ 下一步：编写核心标定代码
