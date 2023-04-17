import gradio as gr
from tqdm import tqdm
import imageio
import pages.humancartoon as humancartoon
from modelscope.outputs import OutputKeys
from commonutils import VedioUtils
import numpy as np

style_dict = {"日漫风":"anime", "3D风":"3d", "手绘风":"handdrawn", "素描风":"sketch", "艺术效果":"artstyle"}

def inference(filepath, style,request: gr.Request,progress=gr.Progress()):
    frameCnt=VedioUtils.get_frame_count(filepath)
    style = style_dict[style]
    outpath = request.client.host+'.video-out.mp4'
    print(outpath)
    reader = imageio.get_reader(filepath)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(outpath, mode='I', fps=fps, codec='libx264')
    pipeline = None
    if style == "anime":
        pipeline = humancartoon.img_cartoon
    if style == "3d":
        pipeline = humancartoon.img_3d_cartoon
    if style == "handdrawn":
        pipeline = humancartoon.img_handdrawn_cartoon
    if style == "sketch":
        pipeline = humancartoon.img_sketch_cartoon
    if style == "artstyle":
        pipeline = humancartoon.img_artstyle_cartoon
    if pipeline is None:
        return filepath
    step = 0.0
    for _, img in tqdm(enumerate(reader)):
        progress(step/frameCnt, desc="视频正在处理中,当前正在处理第" + str(int(step)) + "/" + str(frameCnt) + "帧....")
        result = pipeline(img[..., ::-1])
        res = result[OutputKeys.OUTPUT_IMG]
        writer.append_data(res[..., ::-1].astype(np.uint8))
        step += 1
    writer.close()
    return outpath


with gr.Blocks(title="AI视频卡通化", css="#fixed_size_img {height: 240px;}") as videoCartoonApp:
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
                              AI视频卡通化
                        </h1>
                      </div>

                    </div>
          ''')
    gr.Markdown("人像、风景、自制视频片段...上传您心仪的短视频，选择对应风格(日漫风，3D风，手绘风等等)，一键即可转换为不同风格的卡通化视频")
    with gr.Row():
        radio_style = gr.Radio(label="风格选择", choices=["日漫风", "3D风", "手绘风", "素描风", "艺术效果"], value="日漫风")
    with gr.Row():
        vid_input = gr.Video(source="upload")
        vid_output = gr.Video()
    with gr.Row():
        btn_submit = gr.Button(value="一键生成", elem_id="blue_btn")
    examples = [['./video/video1.mp4'],
                ['./video/video2.mp4']]
    examples = gr.Examples(examples=examples, inputs=[vid_input])
    btn_submit.click(inference, inputs=[vid_input, radio_style], outputs=vid_output)