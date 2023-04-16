import gradio as gr
from modelscope.outputs import OutputKeys
from commonutils import ImageUtils
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# AI绘画 卡通
print("加载AI绘画 卡通模型")
img_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon_compound-models')
print("加载AI绘画 卡通模型-素描")
img_sketch_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-sketch_compound-models')
print("加载AI绘画 卡通模型-3d")
img_3d_cartoon = pipeline(Tasks.image_portrait_stylization,model='damo/cv_unet_person-image-cartoon-3d_compound-models')
print("加载AI绘画 卡通模型-艺术")
img_artstyle_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-artstyle_compound-models')
print("加载AI绘画 卡通模型-手绘")
img_handdrawn_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-handdrawn_compound-models')

with gr.Blocks(title="AI人像多风格漫画", css="#fixed_size_img {height: 240px;} ") as humanCartoonApp:
    style_dict = {"日漫风": "anime", "3D风": "3d", "手绘风": "handdrawn", "素描风": "sketch", "艺术效果": "artstyle"}
    def inference(image, style) :

        style = style_dict[style]
        print("sytle=" + style)
        if style == "anime":
            image = img_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "3d":
            image = img_3d_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "handdrawn":
            image = img_handdrawn_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "sketch":
            image = img_sketch_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "artstyle":
            image = img_artstyle_cartoon(image)[OutputKeys.OUTPUT_IMG]
        return ImageUtils.imageOutput(image)

    gr.HTML('''
          <div style="text-align: center; max-width: 720px; margin: 0 auto;">
                      <div
                        style="
                          display: inline-flex;
                          align-items: center;
                          gap: 0.8rem;
                          font-size: 1.75rem;
                        "
                      >
                        <h1 style="font-family:  PingFangSC; font-weight: 500; line-height: 1.5em; font-size: 32px; margin-bottom: 7px;">
                          AI人像多风格漫画 （Stable-Diffusion卡通系列文生图模型）
                        </h1>
                      </div>
                      <img id="overview" alt="overview" src="https://modelscope.oss-cn-beijing.aliyuncs.com/demo/image-cartoon/demo_sin1.gif" />

                    </div>
          ''')
    gr.Markdown("街拍，人像，团建照片...随意上传您心仪的照片，选择对应风格(日漫风，3D风，手绘风等等)，一键即可转换为不同风格的卡通化图片！多风格的人像模型已经内置好，点点鼠标就可以抢占朋友圈的C位，立刻玩起来吧")
    with gr.Row():
        radio_style = gr.Radio(label="风格选择", choices=["日漫风", "3D风", "手绘风", "素描风", "艺术效果"],
                               value="日漫风")
    with gr.Row():
        img_input = gr.Image(type="pil", elem_id="fixed_size_img")
        img_output = gr.Image(type="pil", elem_id="fixed_size_img")
    with gr.Row():
        btn_submit = gr.Button(value="一键生成", elem_id="blue_btn")
    examples = gr.Examples(examples= [['./images/examples/humancartoon1.png'], ['./images/examples/humancartoon2.png'], ['./images/examples/humancartoon3.png']], inputs=[img_input], outputs=img_output)
    btn_submit.click(inference, inputs=[img_input, radio_style], outputs=img_output)