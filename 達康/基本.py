from streamlit_drawable_canvas import st_canvas
from streamlit import sidebar, dataframe, pyplot, radio as stRadio, title, multiselect, text_input, image as stImage, expander as stExpander, success, file_uploader as flUpldr, json as stJson, button, columns as stCLMN, slider, header ##canvas as stCanvas
from numpy import clip as npClip, max as npMax, nan as npNan
from stUtil import rndrCode
from glob import glob
from pydicom import dcmread
from pandas import DataFrame
from matplotlib.pyplot import subplots, xlabel, ylabel, xlim, ylim
from cv2 import blur, medianBlur, GaussianBlur

def 類型(顯類, ds_array):
    if 顯類 == 'Original':
      return ds_array
    elif 顯類 == 'Mean Filter':
      window=(5, 5)
      return blur(ds_array, window)
    elif 顯類 == 'Median Filter':
      window=3
      return medianBlur(ds_array, window)
    elif 顯類 == 'Gaussian Smoothing':
      window=(5, 5)
      return GaussianBlur(ds_array, window, 0)

def 顯示中介(ds) -> None:
  #common_metadata: dict = {
  #  'DICOM Tag': ['Patient Name', 'Patient Age', 'Patient Sex', 'Patient Birth Date', 'Referring Physician Name', 'Study Date'],
  #  'Value': [str(ds.PatientName), ds.PatientAge, ds.PatientSex, ds.PatientBirthDate, ds.ReferringPhysicianName, ds.StudyDate ]
  #}
  rndrCode([ds.__dict__])
  #map(lambda: hasattrib('Patient', ds), ds.__dict__)
  #df = DataFrame(ds)    #common_metadata
  #df = df.replace(r'^\s*$', npNan, regex=True)
  #header("DICOM Metadata")
  #dataframe(df)

def slider_values(counts, bins):
    header("Bin and Count Range")
    xlim1, xlim2 = slider('Select a x range of values', .0, npMax(bins), (.0, npMax(bins)))
    ylim1, ylim2 = slider('Select a y range of values', 0.0, npMax(counts), (0.0,npMax(counts)))
    return xlim1, xlim2, ylim1, ylim2

def plot_fig(array):
    fig, ax = subplots()
    counts, bins, patches = ax.hist(array.flatten())
    xlim1, xlim2, ylim1, ylim2 = slider_values(counts, bins)
    xlim([xlim1,xlim2])
    ylim([ylim1,ylim2])
    xlabel('Intensities')
    ylabel('Count')
    return fig

def 基本():
  with sidebar:
    title("DICOM Auto-Annotation Tool")
    上傳 = flUpldr("Upload DICOM", type=["dcm"])
    if 上傳: # 調用後端API
      ds=dcmread(上傳)
      response = rqstPOST(f"{BASE_URL}/upload", files={"dicom_file": uploaded_file}).json()  #requests.post

      with stExpander("DICOM Metadata"):
        stJson(response["meta"]) # 顯示元數據
      stImage(f"{BASE_URL}{response['preview_url']}") # 顯示預覽圖像
      canvas = st_canvas(fill_color="rgba(255, 0, 0, 0.3)", stroke_width=3, drawing_mode="rect", height=512, width=512, key="canvas") # 標注畫布
  if not 上傳:
    父='ChestCTwContrast_20200804'
    DCM=glob(f'{父}/*.dcm')
    #for dcm in DCM:
    左頁, 中頁, 右頁=stCLMN([1, 3, 1])
    with 左頁:
      新DCM=map(lambda x:x.split('/')[-1], DCM)
      dcm=stRadio('DCM', 新DCM, horizontal=True, index=0)
    with 中頁:
      ds=dcmread(f'{父}/{dcm}')
      #stImage(ds.pixel_array, caption="DICOM Images", use_column_width=True)
      #from 達康.取得DS import rtrvDS
      from 達康.轉成資框 import 轉成資框
      資框=轉成資框(ds)
      #rndrCode('資框')
      #資框.style.set_caption('資框')
      樣式=[dict(selector="caption", props=[("text-align", "center"), ("font-size", "150%"), ("color", 'black')])]
      資框=資框.style.set_caption("資框").set_table_styles(樣式)
      #df.style.set_caption('Top 10 Fields of Research by Aggregated Funding Amount')
      #資框.style.set_table_attributes("style='display:inline'").set_caption('資框')
      #資框
      dataframe(資框, height=1500)  #, title='資框'
    with 右頁:
      圖=plot_fig(ds.pixel_array) # 顯示預覽圖像
      pyplot(圖)
      #rndrCode(ds)
    if button("Save Annotation"): # 標注提交
      annotation = { "dicom_id": response["meta"]["PatientID"], "coordinates": canvas.json_data, "labels": multiselect("Labels", ["Tumor", "Organ", "Lesion"]) }
      #rqstPOST(f"{BASE_URL}/annotate", json=annotation)
      #success("Annotation saved!")
