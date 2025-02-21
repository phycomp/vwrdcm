from pydicom.errors import InvalidDicomError
from stUtil import rndrCode

def  rtrvDS(ds):
  try:
    # 打印基本文件資訊
    rndrCode("=== DICOM 文件基本資訊 ===")
    #rndrCode(f"文件名稱: {file_path}")
    # 顯示所有 DICOM 標籤和對應的值
    DS資訊=f"""SOP Class UID: {ds.SOPClassUID}
    "SOP Instance UID: {ds.SOPInstanceUID}"""
    for elem in ds:
        # 獲取標籤名稱
        if elem.name != '':
            tag_name = elem.name
        else:
            tag_name = "Unknown"

        # 獲取標籤值
        if elem.VR == "SQ":
            value = f"Sequence with {len(elem.value)} item(s)"
        else:
            value = elem.value

        # 打印標籤資訊
        DS資訊+=f"""標籤: ({elem.tag})"
"名稱: {tag_name}"
"VR (Value Representation): {elem.VR}"
"值: {value}\n"""

    rndrCode(DS資訊)
    # 顯示圖像相關資訊（如果有的話）
    if hasattr(ds, 'pixel_array'):
      rndrCode("\n=== 圖像資訊 ===")
      rndrCode(f"圖像尺寸: {ds.pixel_array.shape}")
      rndrCode(f"圖像類型: {ds.pixel_array.dtype}")
  except InvalidDicomError:
    rndrCode("錯誤：無效的 DICOM 文件")
  except Exception as e:
    rndrCode(f"錯誤：{str(e)}")
