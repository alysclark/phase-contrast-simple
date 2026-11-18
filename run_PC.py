import numpy as np
import os
import re
import SimpleITK as sitk
import matplotlib
import matplotlib.pyplot as plt


segfile = 'path/to/segmentation'
pcfile = 'path/to/pcmag_and_phase'
voxel_size = 1.5625 # mm 
venc = 200.
RRint = 0.638 #
timeint = RRint/20.


old = True


### Reading in the segmentation of the vessels
seg_img = sitk.ReadImage(segfile)
#Reading in the exported phase contrast files
pc_img = sitk.ReadImage(pcfile)


#Convert segmentation of the vessels

array_seg = sitk.GetArrayFromImage(seg_img[:,:,0])
plt.imshow(array_seg)
plt.show()

flow_sum = np.zeros(int(np.max(seg_img)))
velocity= np.zeros((int(np.max(seg_img)),20)) #20 needs to be replaced with total from phase image



for i in range(0,20): #need to convert the value of 20 to get the correct 
    if old:
        array = sitk.GetArrayFromImage(pc_img[:,:,i])
    else:
        array = sitk.GetArrayFromImage(pc_img[:,:,:,i])
    if i==1:    
        plt.imshow(array)
        plt.show()
    for k in range(1,int(np.max(seg_img)+1)): #Running through different colour segmentations
        area = (voxel_size/10)**2 #area in cm2 #scale of mm2 to cm2
        flow_sum[k-1] = flow_sum[k-1] + np.sum(array[array_seg == k]*venc/4096.*area*timeint)#*frame_interval intensity -> cm/s * area  cm3/s 
        #plt.plot(i,np.sum(array[array_seg == k])*area/10.,'+')
        velocity[k-1,i]= np.mean(array[array_seg == k]*venc/4096.) #mm/s or cm/s #*area/10 
        #print(np.sum(array[array_seg == k])*area*frame_interval)
    
    
    
print(flow_sum) #forward volume in ml
flow_sum = flow_sum/RRint*60 #volume in cm3 over on heart beat -> cm3/s

print(flow_sum) #flow in ml/min

##print(velocity)
for k in range(1,int(np.max(seg_img)+1)):
    plt.plot(velocity[k-1,:],label=str(k))
    plt.legend()
    
plt.show()
