from streamlit import session_state, sidebar
from cv2 import imshow as cvImshow, waitKey as cvWaitkey, destroyAllWindows

def cvVwr():
  slices=session_state['slices']
  noSlices=len(slices)
  slceNdx = sidebar.slider('Slice', 0, noSlices-1, int(noSlices/2))
  slce=slices[slceNdx]
  dcmSample=slce.pixel_array*128
  #cv2.imshow(,)
  cvImshow('sample image dicom', dcmSample)
  cvWaitkey(0)
  destroyAllWindows()
  cvWaitkey(1)


  #from dcmbdc.ImageSlicing import vtkRndr
  #vtkRndr()
