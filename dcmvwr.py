from streamlit import sidebar, text_input, radio as stRadio
#BASE_URL = "http://localhost:8000"
MENU, 表單=[], ['顯示', 'vtk', '標注', '自動化', '轉成fhir']    #, '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')

def apply_windowing(arr, ds):
  center = ds.WindowCenter
  width = ds.WindowWidth
  y_min = center - width/2
  y_max = center + width/2
  return npClip((arr - y_min) / (y_max - y_min) * 255, 0, 255).astype(np.uint8)

with sidebar:
  menu=stRadio('表單', MENU, horizontal=True, index=0)
  srch=text_input('搜尋', '')
if menu==len(表單):
  pass
elif menu==MENU[2]:
  #標注
  pass
elif menu==MENU[1]: #標注
  from 達康.vtkUtil import DICOMViewer
  dicom_folder_path = r'path/to/dicom/folder'
  viewer = DICOMViewer(dicom_folder='ChestCTwContrast_20200804', view_orientation='sagittal', debug=True)
  viewer.render()
elif menu==MENU[0]: #顯示
  from 達康.基本 import 基本
  基本()
