from skimage import io
from matplotlib import pyplot as plt

#######################################输入图片链接显示图像
pic = input('please input picture links:')
img = io.imread(pic)
if '.'.join(pic.split('.')[:-1]).endswith('-selected') == False:
    pic = '.'.join(pic.split('.')[:-1]) + '-selected.' + pic.split('.')[-1]
img = io.imread(pic)
f = open('.'.join(pic.split('.')[:-1]).replace('-selected', '') + '.log')
lines = f.readlines()
regions = [line for line in lines if line.startswith('region')]
plt.imshow(img)
for region in regions:
    regionid = region.split()[0].lstrip('region')
    center = region.rstrip(')\n').split('(')[1]
    plt.text(int(center.split(',')[0]), int(center.split(',')[1]), regionid, color='white')
f.close()
plt.show()
#######################################输入图片链接显示图像
