from pydicom.errors import InvalidDicomError
from streamlit import dataframe
from pandas import DataFrame
from stUtil import rndrCode

def 轉成資框(ds):
  try:
    data = []
    for elem in ds: # 獲取標籤名稱
      tag_name = elem.name if elem.name != '' else 'Unknown'
      if elem.VR == "SQ": # 獲取標籤值
        value = f"Sequence with {len(elem.value)} item(s)"
      else:
        try: value = str(elem.value)
        except: value = "Unable to convert"

      data.append({
        'Tag': f"{elem.tag}",
        'Name': tag_name,
        'VR': elem.VR,
        'Value': value,
        'Group': f"{elem.tag.group:04x}",
        'Element': f"{elem.tag.element:04x}"
      })
      df = DataFrame(data)
      #df.attrs['file_path'] = file_path # 添加基本文件信息作為元數據
      df.attrs['TransferSyntaxUID'] = getattr(ds, 'TransferSyntaxUID', 'Unknown')   #transfer_syntax_uid
      if hasattr(ds, 'pixel_array'): # 如果存在圖像數據，添加圖像信息
        df.attrs['image_shape'] = ds.pixel_array.shape
        df.attrs['image_dtype'] = str(ds.pixel_array.dtype)
    #dataframe(df)
    #df=df.style.set_caption('資框')
    return df
  except InvalidDicomError:
    rndrCode("錯誤：無效的 DICOM 文件")
    #return None
  except Exception as e:
    rndrCode(f"錯誤：{str(e)}")
  return None
