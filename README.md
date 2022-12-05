# seg_model_for_cat
model for seg my cat, Lihua fugui.

# Reuult
![fugui2](https://user-images.githubusercontent.com/29834982/205576956-efc96ceb-5e52-4434-b7cd-6d4146075cf5.JPG)![IMG_5860](https://user-images.githubusercontent.com/29834982/205576981-3bf5b423-3851-4f15-ad1b-aeb1e13779cd.JPG)![IMG_5861](https://user-images.githubusercontent.com/29834982/205576986-03332bfa-edbb-481a-92bb-cabad4238c78.JPG) 

# 实验配置
exp.yaml

 Train Dataset
1. voc中cat数据挑出来train   1119 cats
2.  other cat 网上找到的部分cat数据  172 cats 
3. https://www.robots.ox.ac.uk/~vgg/data/pets/   2371cats

# 其他
分割结果边缘还是不够细节, 应该加一个边缘损失去监督优化的..[工具链上这玩意不方便加,简单粗暴用了个denscrf,优化效果不大稳定.]
