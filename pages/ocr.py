import gradio as gr
import numpy as np
from PIL import ImageDraw
from PIL import  Image
import cv2
import math
import pandas as pd
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# ocr模型

print("加载ocr模型-基础模型")
ocr_detection = pipeline(Tasks.ocr_detection, model='damo/cv_resnet18_ocr-detection-line-level_damo')
ocr_license_plate_detection = pipeline(Tasks.license_plate_detection, model='damo/cv_resnet18_license-plate-detection_damo')
print("加载ocr模型-通用场景")
ocr_recognition = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-general_damo')
print("加载ocr模型-手写场景")
ocr_recognition_handwritten = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-handwritten_damo')
print("加载ocr模型-文档场景")
ocr_recognition_document = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-document_damo')
print("加载ocr模型-自然场景")
ocr_recognition_scene = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-scene_damo')
print("加载ocr模型-车牌场景")
ocr_recognition_licenseplate = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-licenseplate_damo')

def crop_image(img, position):
    def distance(x1,y1,x2,y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    position = position.tolist()
    for i in range(4):
        for j in range(i+1, 4):
            if(position[i][0] > position[j][0]):
                tmp = position[j]
                position[j] = position[i]
                position[i] = tmp
    if position[0][1] > position[1][1]:
        tmp = position[0]
        position[0] = position[1]
        position[1] = tmp

    if position[2][1] > position[3][1]:
        tmp = position[2]
        position[2] = position[3]
        position[3] = tmp

    x1, y1 = position[0][0], position[0][1]
    x2, y2 = position[2][0], position[2][1]
    x3, y3 = position[3][0], position[3][1]
    x4, y4 = position[1][0], position[1][1]

    corners = np.zeros((4,2), np.float32)
    corners[0] = [x1, y1]
    corners[1] = [x2, y2]
    corners[2] = [x4, y4]
    corners[3] = [x3, y3]

    img_width = distance((x1+x4)/2, (y1+y4)/2, (x2+x3)/2, (y2+y3)/2)
    img_height = distance((x1+x2)/2, (y1+y2)/2, (x4+x3)/2, (y4+y3)/2)

    corners_trans = np.zeros((4,2), np.float32)
    corners_trans[0] = [0, 0]
    corners_trans[1] = [img_width - 1, 0]
    corners_trans[2] = [0, img_height - 1]
    corners_trans[3] = [img_width - 1, img_height - 1]

    transform = cv2.getPerspectiveTransform(corners, corners_trans)
    dst = cv2.warpPerspective(img, transform, (int(img_width), int(img_height)))
    return dst

def order_point(coor):
    arr = np.array(coor).reshape([4, 2])
    sum_ = np.sum(arr, 0)
    centroid = sum_ / arr.shape[0]
    theta = np.arctan2(arr[:, 1] - centroid[1], arr[:, 0] - centroid[0])
    sort_points = arr[np.argsort(theta)]
    sort_points = sort_points.reshape([4, -1])
    if sort_points[0][0] > centroid[0]:
        sort_points = np.concatenate([sort_points[3:], sort_points[:3]])
    sort_points = sort_points.reshape([4, 2]).astype('float32')
    return sort_points
def draw_boxes(image_full, det_result):
    image_full = Image.fromarray(image_full)
    draw = ImageDraw.Draw(image_full)
    for i in range(det_result.shape[0]):
        # import pdb; pdb.set_trace()
        p0, p1, p2, p3 = order_point(det_result[i])
        draw.text((p0[0]+5, p0[1]+5), str(i+1), fill='blue', align='center')
        draw.line([*p0, *p1, *p2, *p3, *p0], fill='green', width=5)
    image_draw = np.array(image_full)
    return image_draw

def text_detection(image_full, ocr_detection):
    det_result = ocr_detection(image_full)
    det_result = det_result['polygons']
    # sort detection result with coord
    det_result_list = det_result.tolist()
    det_result_list = sorted(det_result_list, key=lambda x: 0.01*sum(x[::2])/4+sum(x[1::2])/4)
    return np.array(det_result_list)

def text_recognition(det_result, image_full, ocr_recognition):
    output = []
    for i in range(det_result.shape[0]):
        pts = order_point(det_result[i])
        image_crop = crop_image(image_full, pts)
        result = ocr_recognition(image_crop)
        output.append([str(i+1), result['text'], ','.join([str(e) for e in list(pts.reshape(-1))])])
    result = pd.DataFrame(output, columns=['检测框序号', '行识别结果', '检测框坐标'])
    return result

types_dict = {"通用场景":ocr_recognition, "自然场景":ocr_recognition_scene, "手写场景":ocr_recognition_handwritten, "文档场景":ocr_recognition_document, "车牌场景":ocr_recognition_licenseplate}

def text_ocr(image_full,types):
    if types == '车牌场景':
        det_result = text_detection(image_full, ocr_license_plate_detection)
        ocr_result = text_recognition(det_result, image_full, ocr_recognition_licenseplate)
        image_draw = draw_boxes(image_full, det_result)
    else:
        det_result = text_detection(image_full, ocr_detection)
        ocr_result = text_recognition(det_result, image_full, types_dict[types])
        image_draw = draw_boxes(image_full, det_result)
    textValue = ""
    for value in ocr_result.values:
       contents=value[1]
       for  txt in contents:
           textValue += txt+" "

    return image_draw, ocr_result , textValue

with gr.Blocks() as ocrApp:
    gr.Markdown("#多场景文字识别")
    gr.Markdown("给定图片作为输入，选择相应场景，我们的模型会输出图片中文字行的坐标位置和识别结果。")
    with gr.Row():
        select_types = gr.Radio(label="图像类型选择",
                                choices=["通用场景", "自然场景", "手写场景", "文档场景", "车牌场景"], value="通用场景")
    with gr.Row():
        img_input = gr.Image(label='输入图像', elem_id="fixed_size_img")
        img_output = gr.Image(label='图像可视化效果', elem_id="fixed_size_img")
    with gr.Row():
        btn_submit = gr.Button(value="一键识别")
    with gr.Row():
        text_textArea = gr.TextArea(label="全部文字",lines=1,max_lines=5)
    with gr.Row():
        text_output = gr.components.Dataframe(label='识别结果', headers=['检测框序号', '行识别结果', '检测框坐标'],
                                              wrap=True)
    with gr.Row():
        examples = [['./images/examples/ocr_general.jpg', "通用场景"], ['./images/examples/license_plate_detection.jpg', "车牌场景"],
                    ['./images/examples/ocr_scene.jpg', "自然场景"], ['./images/examples/ocr_table2.jpg', "文档场景"],
                    ['./images/examples/ocr_handwriting.jpg', "手写场景"]]
        examples = gr.Examples(examples=examples, inputs=[img_input, select_types], label='点击示例图片体验OCR效果')
    btn_submit.click(fn=text_ocr, inputs=[img_input, select_types], outputs=[img_output, text_output,text_textArea])
