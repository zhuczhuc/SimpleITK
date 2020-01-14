# -*- coding:utf-8 -*-
from __future__ import print_function
# %matplotlib inline
import matplotlib.pyplot as plt
import SimpleITK as sitk

image = sitk.Image(256, 128, 64, sitk.sitkInt16)
image_2D = sitk.Image(64, 64, sitk.sitkFloat32)
image_2D = sitk.Image([32, 32], sitk.sitkUInt32)
image_RGB = sitk.Image([128, 128], sitk.sitkVectorUInt8, 3)

help(image)

print(image.GetSize())
print(image.GetOrigin())
print(image.GetSpacing())
print(image.GetDirection())
print(image.GetNumberOfComponentsPerPixel())

# Note: The starting index of a SimpleITK Image is always 0. If the output of an
# ITK filter has non-zero starting index, then the index will be set to 0,
# and the origin adjusted accordingly.
# The size of the image's dimensions have explicit accessors:
print(image.GetWidth())
print(image.GetHeight())
print(image.GetDepth())

# Since the dimension and pixel type of a SimpleITK image is determined at run-time accessors are needed.
print(image.GetDimension())
print(image.GetPixelIDValue())
print(image.GetPixelIDTypeAsString())

# What is the depth of a 2D image?
print(image_2D.GetSize())
print(image_2D.GetDepth())

# What is the dimension and size of a Vector image?
print(image_RGB.GetDimension())
print(image_RGB.GetSize())
print(image_RGB.GetNumberOfComponentsPerPixel())

# For certain file types such as DICOM, additional information about the image is contained in the meta-data dictionary.
for key in image.GetMetaDataKeys():
    print("\"{0}\":\"{1}\"".format(key, image.GetMetaData(key)))

# There are the member functions GetPixel and SetPixel which provides an ITK-like interface for pixel access.
help(image.GetPixel)
print(image.GetPixel(0, 0, 0))
image.SetPixel(0, 0, 0, 1)
print(image.GetPixel(0, 0, 0))

print(image[0, 0, 0])
image[0, 0, 0] = 10
print(image[0, 0, 0])

# Conversion between numpy and SimpleITK
nda = sitk.GetArrayFromImage(image)
print(nda)
help(sitk.GetArrayFromImage)

# Get a view of the image data as a numpy array, useful for display
nda = sitk.GetArrayViewFromImage(image)

nda = sitk.GetArrayFromImage(image_RGB)
img = sitk.GetImageFromArray(nda)
img.GetSize()

help(sitk.GetImageFromArray)

img = sitk.GetImageFromArray(nda, isVector=True)  # zhuc ?
print(img)

# The order of index and dimensions need careful attention during conversion
# ITK's Image class does not have a bracket operator. It has a GetPixel which
# takes an ITK Index object as an argument, which is ordered as (x,y,z).
# This is the convention that SimpleITK's Image class uses for the GetPixel
# method and slicing operator as well. In numpy, an array is indexed in the
# opposite order (z,y,x). Also note that the access to channels is different.
# In SimpleITK you do not access the channel directly, rather the pixel value
# representing all channels for the specific pixel is returned and you then
# access the channel for that pixel. In the numpy array you are accessing the
# channel directly.
import numpy as np

multi_channel_3Dimage = sitk.Image([2,4,8], sitk.sitkVectorFloat32, 5)
x = multi_channel_3Dimage.GetWidth() - 1
y = multi_channel_3Dimage.GetHeight() - 1
z = multi_channel_3Dimage.GetDepth() - 1
multi_channel_3Dimage[x,y,z] = np.random.random(multi_channel_3Dimage.GetNumberOfComponentsPerPixel())

nda = sitk.GetArrayFromImage(multi_channel_3Dimage)

print("Image size: " + str(multi_channel_3Dimage.GetSize()))
print("Numpy array size: " + str(nda.shape))

# Notice the index order and channel access are different:
print("First channel value in image: " + str(multi_channel_3Dimage[x,y,z][0]))
print("First channel value in numpy array: " + str(nda[z,y,x,0]))

# Are we still dealing with Image, because I haven't seen one yet...
# While SimpleITK does not do visualization, it does contain a built in Show
# method. This function writes the image out to disk and than launches a program
# for visualization. By default it is configured to use ImageJ, because it is
# readily supports all the image types which SimpleITK has and load very quickly.
# However, it's easily customizable by setting environment variables.

# sitk.Show(image)

# y converting into a numpy array, matplotlib can be used for visualization for
# integration into the scientific python environment.
import matplotlib.pyplot as plt
z = 0
slice = sitk.GetArrayViewFromImage(image)[z,:,:]
plt.imshow(slice)
plt.show()
