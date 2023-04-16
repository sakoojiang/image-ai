import  gradio as gr

import markdown

import torch
from commonutils import ImageUtils
import os,time



from diffusers import StableDiffusionPipeline

torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32

print(torch_dtype)

table_diffusion = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-v0.1",torch_dtype=torch_dtype)
if torch_dtype==torch.float16:
    torch.backends.cudnn.benchmark = True
    table_diffusion.to('cuda')


def text2Image(prompt: str,negative_prompt: str,num_inference_steps: int,
               width: int,
               height:  int,
               progress=gr.Progress()):
    tts_start = int(time.time())
    def callback(step, tensor, c):
        tts_end = int(time.time())

        cost_every = (tts_end-tts_start)*1.0/step
        cost_every = round(cost_every,2)
        progress(step*1.0/num_inference_steps, desc="正在生成图片,step： " + str(step) + "/" + str(num_inference_steps) + "(迭代平均耗时" + str(cost_every) + "秒)..." )

    progress(0, desc="正在生成图片,step: 0/" + str(num_inference_steps) + ".....")
    output = table_diffusion(prompt=prompt,num_inference_steps=num_inference_steps
                             , negative_prompt=negative_prompt
                             , width=width,height=height
                             , callback=callback)
    image = output.images[0]
    image.save("result.png")
    return image




with gr.Blocks(title="中文StableDiffusion-文本生成图像-通用领域") as textCn2ImageApp:
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown(markdown.dict["中文文生图0"])
            gr.HTML(ImageUtils.image2HtmlTag("./images/tushenwen.jpg"))
            gr.Markdown(markdown.dict["中文文生图1"])
        with gr.Column(scale=3):
            prompt = gr.Textbox(label="提示词",elem_id="prompt")
            negative_prompt = gr.Textbox(label="反向提示词",elem_id="negative_prompt")
            numInferenceSteps = gr.Slider(minimum=25,maximum=100,value=50,label="迭代次数",info="迭代次数越多，效果越好",step=1)
            with  gr.Row():
                with gr.Column():
                    width = gr.Slider(minimum=256,maximum=1024,value=512,label="图片宽度",step=1)
                with gr.Column():
                    height =gr.Slider(minimum=256,maximum=1024,value=512,label="图片高度",step=1)
            sumit_bnt = gr.Button(value="提交", elem_id="sumit_bnt")
            examples = gr.Examples(examples=[
                ["铁马冰河入梦来，3D绘画。"],
                ["飞流直下三千尺，油画。"],
                ["女孩背影，日落，唯美插画。"],
                ["铁马冰河入梦来，概念画，科幻，玄幻，3D"],
                ["中国海边城市，科幻，未来感，唯美，插画。"],
                ["废土风,超现实风景,破败的巨大人形机甲躺在冰川之间,科幻风格,蒸汽朋克风"],
                ["那人却在灯火阑珊处，色彩艳丽，古风，资深插画师作品，桌面高清壁纸。"],
            ] , inputs=prompt)
            outputImg = gr.Image(type="pil")
        sumit_bnt.click(text2Image , inputs=[prompt,negative_prompt, numInferenceSteps , width , height] , outputs=outputImg)



