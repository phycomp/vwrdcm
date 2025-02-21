from pydicom import dcmread
from matplotlib.pyplot import subplot, imshow, gcf, cm
from numpy import zeros
from glob import glob
from streamlit import sidebar, pyplot, session_state, dataframe
from pathlib import Path
from pandas import DataFrame
#from matplotlib.pyplot import subplots, axis, cm, imshow, gcf

def slceSqnc():
  DCMs = []
  print('Parent',Path(__file__).parent)
  absPath=Path(__file__).parent/'Head_NeckCTA_20170917_ID'#charset_files palettes''#'newDCM'
  
  for fname in absPath.glob('*.dcm'):#, recursive=False):
    print(fname)
    DCMs.append(dcmread(fname))

  slices, skipcount=[], 0
  for dcm in DCMs:
      if hasattr(dcm, 'SliceLocation'):
          slices.append(dcm)
          print(dcm.SliceLocation)
      else: skipcount +=  1

  print("skipped, no SliceLocation: {}".format(skipcount))
  #slices.sort(key = lambda x: int(x.InstanceNumber))
  slices = sorted(slices, key=lambda dcm: dcm.SliceLocation)

  # pixel aspects, assuming all slices are the same
  session_state['slices']=slices

  noSlices=len(slices)
  print('noSlices', noSlices)
  sliceNdx = sidebar.slider('Slice', 0, noSlices-1, int(noSlices/2))
  session_state['sliceNdx']=sliceNdx
  #sliceNdx=session_state['sliceNdx']
  if sliceNdx:
    dcm=DCMs[sliceNdx]
    #dcm.SOP
    #rtrvMetadata(dcm)
    #()
    imshow(dcm.pixel_array, cmap=cm.bone) 
    #print(  dcm.__dict__)
    #fig = plotSlice(dcm)
    fig=gcf()
    pyplot(fig)
  session_state['slices']=slices
def rtrvMetadata(dcm):
  from pandas import DataFrame
  from streamlit import write as stWrite, code as stCode#, echo
  from streamlit.components.v1 import html
  ptntName = dcm.PatientName
  ptntFullname = ptntName.family_name + ptntName.given_name
  dcmInfo=f"""SOP Class........: {dcm.SOPClassUID} ({dcm.SOPClassUID.name})
Patient's Name...: {ptntFullname}
Patient ID.......: {dcm.PatientID}
Modality.........: {dcm.Modality}
Study Date.......: {dcm.StudyDate}
Image size.......: {dcm.Rows} x {dcm.Columns}
Pixel Spacing....: {dcm.PixelSpacing}
Slice location...: {dcm.get('SliceLocation', '(missing)')}"""
  #from json import dumps
  stWrite(dcm.to_json_dict())
  #dcmDF=DataFrame.from_dict(dcm.to_json_dict())
  #dcmDF
  #stWrite()#dumps())
  #stWrite(  dcm.to_json())
  #stCode(dcmInfo)
  #from streamlit import session_state, dataframe, sidebar
  #from pandas import DataFrame
  #slices=session_state['slices']
  #noSlices=len(slices)
  #sliceNdx = sidebar.slider('Slice', 0, noSlices-1, int(noSlices/2))
  #sliceNdx=session_state['sliceNdx']
  #session_state['sliceNdx']=sliceNdx
  #dcm=slices[sliceNdx]
  #dcmDfrm=DataFrame(dcm)#.from_dict(dcm)#.__dict__
  #dcmDfrm
def reCnstrctn3D():
  from matplotlib.pyplot import subplot, imshow, gcf
  from numpy import zeros, arange, ones
  from streamlit import pyplot, sidebar, session_state, write as stWrite
  slices=session_state['slices']
  noSlices=len(slices)
  sliceNdx = sidebar.slider('Slice', 0, noSlices-1, int(noSlices/2))
  img_shape = list(slices[sliceNdx].pixel_array.shape) # create 3D array
  img_shape.append(len(slices))
  stWrite(img_shape)
  img3D = zeros(img_shape)

  # fill 3D array with the images from the files
  for ndx, slc in enumerate(slices):
    img2d = slc.pixel_array
    print(img2d.shape)
    #arr = zeros((100, 3))
    #arr[:,0:2] = arange(100*2).reshape(-1,2)
    #arr[40,2]=6
    #imgSHP=img2d.shape
    #img3D = ones((imgSHP[0], imgSHP[1]+1))
    #img3D[:, :, 1:] = img2d
    try: img3D[:, :, ndx] = img2d
    except: print(f'shape mismatched:{ndx}')
  #stWrite(img3D.shape)
  ps = slices[sliceNdx].PixelSpacing
  ss = slices[sliceNdx].SliceThickness
  axAspect = ps[1]/ps[0]
  sagAspect = ps[1]/ss
  corAspect = ss/ps[0]

  #imshow(a[:,:,z], aspect=dy/dx) # pixel size (dx, dy)
  axial = subplot(2, 2, 1)
  stWrite('img_shape', img_shape[2]//2)
  imshow(img3D[:, :, sliceNdx])  #img_shape[2]//2]
  axial.set_aspect(axAspect)

  sgttl = subplot(2, 2, 2)
  imshow(img3D[:, sliceNdx, :]) #img_shape[1]//2
  sgttl.set_aspect(sagAspect)

  crnl = subplot(2, 2, 3)
  imshow(img3D[sliceNdx, :, :].T)   #img_shape[0]//2
  crnl.set_aspect(corAspect)
  fig=gcf()
  pyplot(fig)
