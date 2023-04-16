import gradio as gr
from modelscope.outputs import OutputKeys
from commonutils import ImageUtils
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

#人像修复
print("加载人像修复模型")
portrait_enhancement = pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')

# 色彩增强
print("加载色彩增强模型")
img_colorization = pipeline(Tasks.image_colorization,  model='damo/cv_ddcolor_image-colorization')


# 图像去噪
print("加载图像去噪模型")
image_denoise_pipeline = pipeline(Tasks.image_denoising, model='damo/cv_nafnet_image-denoise_sidd')


# 图像调色
print("加载图像调色模型")
image_color_enhance = pipeline(Tasks.image_color_enhancement, model='damo/cv_csrnet_image-color-enhance-models')

with gr.Blocks(title="AI老照片修复", css="#overview {margin: auto;max-width: 600px; max-height: 400px; width: 100%;}") as photoRepairApp:
    yes, no = "是", "否"
    def inference(img, colorization_optio, image_denoise_option, color_enhance_option,progress=gr.Progress()) :
        step = 1
        if colorization_optio == yes:
            step += 1
        if image_denoise_option == yes:
            step += 1
        if color_enhance_option == yes:
            step += 1
        echoStep = 1.0/step
        startPrecent = 0
        # 人像修复
        progress(startPrecent, desc="正在进行图像修复.....")
        img = portrait_enhancement(img)[OutputKeys.OUTPUT_IMG]



        # 图像上色
        if colorization_optio == yes:
            startPrecent += echoStep
            progress(startPrecent, desc="正在进行图像上色.....")
            img = img_colorization(img)[OutputKeys.OUTPUT_IMG]
        # 图像去噪
        if image_denoise_option == yes:
            startPrecent += echoStep
            progress(startPrecent, desc="正在进行图像去噪.....")
            img = image_denoise_pipeline(img)[OutputKeys.OUTPUT_IMG]

        # 图像调色
        if color_enhance_option ==yes:
            startPrecent += echoStep
            progress(startPrecent, desc="正在进行图像调色.....")
            img = image_color_enhance(img)[OutputKeys.OUTPUT_IMG]


        progress(1, desc="修复结束，渲染图片")
        return ImageUtils.imageOutput(img)



    examples = [['./images/examples/repair1.jpg'],
                ['./images/examples/repair2.jpg'],
                ['./images/examples/repair3.jpg'],
                ['./images/examples/repair4.jpg'],
                ['./images/examples/repair5.jpg']]

    gr.HTML('''
            <div style="text-align: center; max-width: 720px; margin: 0 auto;">
                <img id="overview" alt="overview" src="https://vigen-video.oss-cn-shanghai.aliyuncs.com/ModelScope/studio_old_photo_restoration/overview_long.gif?OSSAccessKeyId=LTAI4Ffgrqm3FbDKBTk4ddwe&Expires=1992627209&Signature=U0umGRRixAD2qgxvShtReLtxuzM%3D" />
            </div>
          ''')
    gr.Markdown("输入一张老照片，点击一键修复，就能获得由AI完成画质增强、智能上色等处理后的彩色照片！还等什么呢？快让相册里的老照片坐上时光机吧~")
    with gr.Row():
        with gr.Column(scale=2):
            img_input = gr.Image(label="图片", type="pil")
            colorization_option = gr.Radio(label="重新上色", choices=[yes, no], value=yes)
            image_denoise_option = gr.Radio(label="应用图像去噪（存在细节损失风险）", choices=[yes, no],
                                                       value=no)
            color_enhance_option = gr.Radio(label="应用色彩增强（存在罕见色调风险）", choices=[yes, no],
                                                       value=no)
            btn = gr.Button("一键修复")
        with gr.Column(scale=3):
            img_output = gr.Image(type="pil")
    inputs = [img_input, colorization_option, image_denoise_option, color_enhance_option]
    btn.click(fn=inference, inputs=inputs, outputs=img_output)
    gr.Examples(examples, inputs=img_input)

