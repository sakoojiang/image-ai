import gradio as gr
import markdown
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from commonutils import ImageUtils

#通用抠图
print("加载通用抠图模型")
universal_matting = pipeline(Tasks.universal_matting, model='damo/cv_unet_universal-matting')

#人像抠图
print("加载人像抠图模型")
portrait_matting = pipeline(Tasks.portrait_matting,model='damo/cv_unet_image-matting')



with gr.Blocks() as removeBgApplication:
    def removeBgDefault(input_img):
        result = universal_matting(input_img)
        return result[OutputKeys.OUTPUT_IMG]
    def removeBgHuman(input_img):
        result = portrait_matting(input_img)
        return result[OutputKeys.OUTPUT_IMG]
    with gr.Tab("通用物体抠图"):
        with gr.Row():
            with gr.Column():
                gr.Markdown(markdown.dict["通用抠图0"])
                gr.HTML(ImageUtils.image2HtmlTag("images/通用抠图.png"))
                gr.Markdown(markdown.dict["通用抠图1"])
            with gr.Column():
                with gr.Row():
                    removeBgDefaultImageInput = gr.Image()
                    removeBgDefaultImageOutput = gr.Image(type="pil")
                with gr.Row():
                    removeBgDefaultBtn = gr.Button("提交")
                with gr.Row():
                    gr.Examples([["./images/examples/removebg-default1.jpg"],["./images/examples/removebg-default2.jpg"]],inputs=removeBgDefaultImageInput)

    with gr.Tab("人像抠图"):
        with gr.Row():
            with gr.Column():
                gr.Markdown(markdown.dict["人像抠图0"])
                gr.HTML(ImageUtils.image2HtmlTag("images/人像抠图.png"))
                gr.Markdown(markdown.dict["人像抠图1"])
            with gr.Column():
                with gr.Row():
                    removeBgHumanImageInput = gr.Image()
                    removeBgHumanImageOutput = gr.Image(type="pil")
                with gr.Row():
                    removeBgHumanBtn = gr.Button("提交")
                with gr.Row():
                    gr.Examples( [['./images/examples/renxiang-test1.png'],['./images/examples/renxiang-test2.png']], inputs=removeBgHumanImageInput)
    removeBgDefaultBtn.click(fn=removeBgDefault, inputs=removeBgDefaultImageInput, outputs=removeBgDefaultImageOutput)
    removeBgHumanBtn.click(fn=removeBgHuman,inputs=removeBgHumanImageInput,outputs=removeBgHumanImageOutput)



