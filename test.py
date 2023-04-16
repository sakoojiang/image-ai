import gradio as gr


def predict(text_input,request: gr.Request):
    # 从 request 对象中获取输入数据
    request_data = request.client.host
    # 将输入数据和 request 数据组合起来进行预测
    result = text_input + ", " + request_data
    return result

iface = gr.Interface(fn=predict, inputs="text", outputs="text")

if __name__ == "__main__":
    iface.launch()