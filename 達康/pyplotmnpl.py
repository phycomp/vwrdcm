def plotSlice(vol, slice_ix=0):
  fig, ax = subplots()
  axis('off')
  print(vol)
  selected_slice = vol[slice_ix, :]
  #selected_slice = vol[slice_ix, :, :]
  ax.imshow(selected_slice, origin='lower', cmap='gray')
  return fig
  #filename = get_testdata_files("CT_small.dcm")[0]
  #ds = pydicom.dcmread(filename)

def run():
  from streamlit import pyplot, sidebar
  from pydicom import read_file
  from streamlit import file_uploader
  from matplotlib.pyplot import subplots, axis, cm, imshow, gcf
  MENUs=['Slice', '3DreConstruction', 'UploadDCM', 'Annot', 'vtkRndr', 'opencv']  #'Metadata', 
  menu = sidebar.radio('Output', MENUs, index=0)
  if menu==MENUs[0]:
    from dcmbdc.sliceSeq import slceSqnc
    slceSqnc()
  elif menu==MENUs[1]:
    from dcmbdc.sliceSeq import reCnstrctn3D
    from streamlit import session_state
    reCnstrctn3D()  #slices
  elif menu==MENUs[2]:
    flUpld=file_uploader('Please Upload dcm')
    if flUpld:
      'Uploaded completed'
  elif menu==MENUs[3]:
    from dcmbdc.annot import Annot
    Annot()
  elif menu==MENUs[4]:
    'vtkRndr'
    from vedo import load as vdLoad, show as vdShow
    from pathlib import Path
    absPath=Path(__file__).parent
    absPath=absPath/'Head_NeckCTA_20170917_ID'#'newDCM'
    dcmVLM = vdLoad(str(absPath)) #returns a vtkVolume object
    vdShow(dcmVLM, bg='white')
  elif menu==MENUs[5]:
    'opencv'
    from dcmbdc.cvMnpl import cvVwr
    cvVwr()
  elif menu==MENUs[5]:
    'iframe'
    from streamlit import iframe
    iframe('')

  #elif menu==MENUs[1]:
  #  from dcmbdc.sliceSeq import rtrvMetadata
  #  rtrvMetadata()
def DCMmnpl():
  from pathlib import Path
  import matplotlib.pyplot as plt
  import pydicom
  from pydicom.data import get_testdata_files
  session_state['sliceNdx']=sliceNdx
  absPath=Path(__file__).parent
  dcm=read_file(absPath/'1_1_1_1.dcm')
  imshow(dcm.pixel_array, cmap=cm.bone) 
  #print(  dcm.__dict__)
  #fig = plotSlice(dcm)
  fig=gcf()
  pyplot(fig)
