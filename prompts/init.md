信号分析界面。上传信号，有时频图，频谱图，时频图，可以调参数，可以保存图片。后端用go还是python

前端：Vue.js+typescript+ Vite
后端：Python（使用Flask）

功能：
1. 上传信号文件（支持WAV、mp3等）
2. 显示时频图、频谱图和时频图
3. 可以调整时频图的参数（如窗口大小、重叠率等）。参数有默认值，同时前端给接口可以调整参数。
```python
class Config:
    """Configuration for the spectrogram animation."""
    sr 
    n_fft 
    hop_length
    cmap 
    window_size 
```
5. 可以保存图片到指定位置

代码风格：
1. 前端代码使用Vue.js的单文件组件结构，保持代码清晰和模块化。
2. 后端代码使用Flask框架，保持代码简洁和易读。
3. 前后端通过RESTful API进行通信，确保接口设计合理，易于维护和扩展。
4. 注释清晰，变量命名规范，遵循PEP 8编码规范（Python）和Vue.js最佳实践（前端）。
5. log日志记录用户操作和系统状态，便于调试和维护。后端有日志文件保存
6. dockerize整个应用，方便部署和运行。提供Dockerfile和docker-compose.yml文件。