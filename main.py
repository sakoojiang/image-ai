
import os
import gradio as gr

#  removebg,changebg,repair-photo,human-cartoon,video-cartoon,ocr,cntext2image
if __name__ == '__main__':
    removebg,changebg , repairPhoto,humanCartoon,videoCartoon,ocr,cntext2image= "removebg","changebg","repair-photo","human-cartoon","video-cartoon","ocr","cntext2image"
    appNameDic={
        removebg: "一键抠图",
        changebg:"一键切换图片背景",
        repairPhoto:"旧照片修复",
        humanCartoon: "AI人像多风格漫画",
        ocr: "多场景文字识别",
        videoCartoon:"AI视屏卡通化",
        cntext2image: "中文StableDiffusion-文本生成图像"

    }
    types = os.getenv('types','removebg,changebg')
    concurrency_count = os.getenv("queue",2)


    print("active types="+types)

    actives = types.split(",")


    appNameList = []
    appList = []
    for appKey in actives:
        if appNameDic[appKey]:
            print("激活app:"+appNameDic[appKey])
            appNameList.append(appNameDic[appKey])
        if appKey == removebg:
            from pages.removebg import removeBgApplication
            appList.append(removeBgApplication)
        if appKey == changebg:
            from pages.changebg import changeBgApp
            appList.append(changeBgApp)
        if appKey == humanCartoon:
            from pages.humancartoon import humanCartoonApp
            appList.append(humanCartoonApp)
        if appKey == videoCartoon:
            from pages.videocartoon import videoCartoonApp
            appList.append(videoCartoonApp)
        if appKey == repairPhoto:
            from pages.photorepair import photoRepairApp
            appList.append(photoRepairApp)
        if appKey == cntext2image:
            from pages.cntext2image import textCn2ImageApp
            appList.append(textCn2ImageApp)
        if appKey == ocr:
            from pages.ocr import ocrApp
            appList.append(ocrApp)





    app = gr.TabbedInterface(appList,appNameList)
    app.queue(concurrency_count=concurrency_count).launch(server_name="0.0.0.0")
