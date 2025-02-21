from pandas import json_normalize
from PIL import Image
from streamlit import sidebar, write as stWrite
from streamlit_drawable_canvas import st_canvas as stCanvas
from streamlit import image as stImage, dataframe

def Annot():
  with sidebar:
    stroke_width = slider("Stroke width: ", 1, 25, 3)
    stroke_color = color_picker("Stroke color hex: ")
    bg_color = color_picker("Background color hex: ", "#eee")
    bg_image = file_uploader("Background image:", type=["png", "jpg"])
    annTools=("freedraw", "line", "rect", "circle", "transform")
    drawing_mode = radio("Drawing tool:", annTools, key='annTools')
    realtime_update = checkbox("Update in realtime", True)
    # Create a canvas component# Fixed fill color with some opacity
    cnvsRslt=stCanvas(fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width, stroke_color=stroke_color, background_color=bg_color, background_image=Image.open(bg_image) if bg_image else None, update_streamlit=realtime_update, height=150, drawing_mode=drawing_mode, key="canvas",)

    # Do something interesting with the image data and paths
    #stWrite(cnvsRslt.image_data)
    imgData=cnvsRslt.image_data
    if imgData: stImage(Image.fromarray(imgData))  #.all()
    if cnvsRslt.json_data: dataframe(json_normalize(cnvsRslt.json_data["objects"]))
