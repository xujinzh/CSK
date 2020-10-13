# CSK
## CF 类目标跟踪算法之一：CSK

### 代码介绍

代码是论文 ["Exploiting the Circulant Structure of Tracking-by-detection with Kernels" João F. Henriques, Rui Caseiro, Pedro Martins, and Jorge Batista ECCV 2012](http://www.robots.ox.ac.uk/~joao/publications/henriques_eccv2012.pdf) 的 Python 实现。同时，代码也是 [circulant_matrix_tracker](https://github.com/rodrigob/circulant_matrix_tracker) 的重写，将源代码从支持 Python2 改进到支持 Python3， 同时修复了部分错误。

### 代码使用方法

1. git clone https://github.com/xujinzh/CSK.git
2. python run.py -i ./data/surfer

数据使用的是 MILTrack videos 中的 surfer，更多视频请访问 [miltrack data](https://bbabenko.github.io/miltrack.html) 下载。

### 依赖包

- Python3
- Numpy
- Scipy
- Matplotlib



