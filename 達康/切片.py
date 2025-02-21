from vtk import vtkImageReader2, vtkMatrix4x4, vtkImageReslice, vtkLookupTable, vtkImageMapToColors, vtkImageActor, vtkRenderer, vtkRenderWindow, vtkInteractorStyleImage, vtkInteractorStyleImage, vtkRenderWindowInteractor
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
reader = vtkImageReader2()
reader.SetFilePrefix(VTK_DATA_ROOT + "/Data/headsq/quarter")  #absPath/"newDCM"
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetDataScalarTypeToUnsignedShort()
reader.UpdateWholeExtent()

def vtkRndr():
  # Calculate the center of the volume
  reader.Update()
  xMin, xMax, yMin, yMax, zMin, zMax = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
  xSpacing, ySpacing, zSpacing = reader.GetOutput().GetSpacing()
  x0, y0, z0 = reader.GetOutput().GetOrigin()

  center = [x0 + xSpacing * 0.5 * (xMin + xMax), y0 + ySpacing * 0.5 * (yMin + yMax), z0 + zSpacing * 0.5 * (zMin + zMax)]

  # Matrices for axial, coronal, sagittal, oblique view orientations
  axial = vtkMatrix4x4()
  axial.DeepCopy((1, 0, 0, center[0],
                  0, 1, 0, center[1],
                  0, 0, 1, center[2],
                  0, 0, 0, 1))

  coronal = vtkMatrix4x4()
  coronal.DeepCopy((1, 0, 0, center[0],
                    0, 0, 1, center[1],
                    0,-1, 0, center[2],
                    0, 0, 0, 1))

  sagittal = vtkMatrix4x4()
  sagittal.DeepCopy((0, 0,-1, center[0],
                     1, 0, 0, center[1],
                     0,-1, 0, center[2],
                     0, 0, 0, 1))

  oblique = vtkMatrix4x4()
  oblique.DeepCopy((1, 0, 0, center[0],
                    0, 0.866025, -0.5, center[1],
                    0, 0.5, 0.866025, center[2],
                    0, 0, 0, 1))

  # Extract a slice in the desired orientation
  reslice = vtkImageReslice()
  reslice.SetInputConnection(reader.GetOutputPort())
  reslice.SetOutputDimensionality(2)
  reslice.SetResliceAxes(sagittal)
  reslice.SetInterpolationModeToLinear()

  # Create a greyscale lookup table
  table = vtkLookupTable()
  table.SetRange(0, 2000) # image intensity range
  table.SetValueRange(0.0, 1.0) # from black to white
  table.SetSaturationRange(0.0, 0.0) # no color saturation
  table.SetRampToLinear()
  table.Build()

  # Map the image through the lookup table
  color = vtkImageMapToColors()
  color.SetLookupTable(table)
  color.SetInputConnection(reslice.GetOutputPort())

  # Display the image
  actor = vtkImageActor()
  actor.GetMapper().SetInputConnection(color.GetOutputPort())

  renderer = vtkRenderer()
  renderer.AddActor(actor)

  window = vtkRenderWindow()
  window.AddRenderer(renderer)

  # Set up the interaction
  interactorStyle = vtkInteractorStyleImage()
  interactor = vtkRenderWindowInteractor()
  interactor.SetInteractorStyle(interactorStyle)
  window.SetInteractor(interactor)
  window.Render()

  # Create callbacks for slicing the image
  actions = {}
  actions["Slicing"] = 0

  def ButtonCallback(obj, event):
      if event == "LeftButtonPressEvent":
          actions["Slicing"] = 1
      else:
          actions["Slicing"] = 0

  def MouseMoveCallback(obj, event):
      (lastX, lastY) = interactor.GetLastEventPosition()
      (mouseX, mouseY) = interactor.GetEventPosition()
      if actions["Slicing"] == 1:
          deltaY = mouseY - lastY
          reslice.Update()
          sliceSpacing = reslice.GetOutput().GetSpacing()[2]
          matrix = reslice.GetResliceAxes()
          # move the center point that we are slicing through
          center = matrix.MultiplyPoint((0, 0, sliceSpacing*deltaY, 1))
          matrix.SetElement(0, 3, center[0])
          matrix.SetElement(1, 3, center[1])
          matrix.SetElement(2, 3, center[2])
          window.Render()
      else: interactorStyle.OnMouseMove()
  interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
  interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
  interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)

  interactor.Start()
