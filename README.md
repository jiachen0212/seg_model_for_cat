# seg_model_for_cat
model for seg my cat, Lihua fugui.

# Reuult
![IMG_5860](https://user-images.githubusercontent.com/29834982/205576981-3bf5b423-3851-4f15-ad1b-aeb1e13779cd.JPG)![IMG_5861](https://user-images.githubusercontent.com/29834982/205576986-03332bfa-edbb-481a-92bb-cabad4238c78.JPG) ![fugui](https://user-images.githubusercontent.com/29834982/205607860-d8fc7388-3e22-4bb6-834d-378f22390b3d.JPG)![fugui1](https://user-images.githubusercontent.com/29834982/205607879-f5b1de5f-5c25-417c-8456-c970d7d5ce02.JPG)![fugui2](https://user-images.githubusercontent.com/29834982/205607883-1ad48c27-b7d7-4335-b803-f80afa04cf8b.JPG)![fugui3](https://user-images.githubusercontent.com/29834982/205607886-3f3e5e4a-71d7-488b-98e7-1b7bd07da01a.JPG)
![fg](https://user-images.githubusercontent.com/29834982/206649933-8f872647-26d8-4a23-b9d6-7de8c2ffa634.jpg)
![Christmas_fugui](https://user-images.githubusercontent.com/29834982/206713892-c6e9a73f-90bf-46c5-aa59-4045e315ccc1.png)

# 实验配置
exp.yaml

# Train Dataset
1. voc中cat数据挑出来train   1119 cats
2.  other cat 网上找到的部分cat数据  172 cats 
3. https://www.robots.ox.ac.uk/~vgg/data/pets/   2371cats

# 其他
分割结果边缘还是不够细节, 应该加一个边缘损失去监督优化的..[工具链上这玩意不方便加,简单粗暴用了个denscrf,优化效果不大稳定.]
