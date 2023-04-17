# 用于x86  CPU环境的docker构建文件
FROM  registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-py37-torch1.11.0-tf1.15.5-1.4.3
ENV types removebg,changebg
ENV XDG_CACHE_HOME /mnt/workspace/.cache

RUN pip install --no-cache-dir   gradio -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir  scikit-image -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --no-cache-dir  easydict -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir  fairseq -i  https://pypi.tuna.tsinghua.edu.cn/simple

ADD image-ai.tar.gz /opt/
WORKDIR /opt/image-ai
ENTRYPOINT ["python","-u","main.py"]