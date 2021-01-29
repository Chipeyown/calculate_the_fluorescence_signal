from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
from skimage import io
import pandas as pd


##############################################圈出边界
def OnPress(event):
    if event.button == 1:
        border.append((event.xdata, event.ydata))
        if len(border) == 1:
            ax.scatter(border[0][0], border[0][1], color='white', s=2)
        if len(border) > 1:
            ax.plot([border[-2][0], border[-1][0]], [border[-2][1], border[-1][1]], color='white', linewidth=2)
        fig.canvas.draw()
    elif event.button == 3:
        if len(border) == 1:
            ax.scatter(border[0], color='orangered', s=2)
        else:
            ax.plot([border[-2][0], border[-1][0]], [border[-2][1], border[-1][1]], color='orangered')
        fig.canvas.draw()
        border.pop()


def OnMouseMotion(event):
    if event.button == 1:
        border.append((event.xdata, event.ydata))
        if len(border) > 1:
            ax.plot([border[-2][0], border[-1][0]], [border[-2][1], border[-1][1]], color='white')
        fig.canvas.draw()
##############################################圈出边界


##############################################获取区域内的所有的像素点
def Get_dots_in_border_region(border):
    dots = []  # dot in region
    polygon = Polygon(border)
    centroid = polygon.centroid  # centroid of region
    x = [e[0] for e in border]
    y = [e[1] for e in border]
    for i in range(int(min(x) + 1), int(max(x) + 1)):
        for j in range(int(min(y) + 1), int(max(y) + 1)):
            point = Point(i, j)
            if point.within(polygon):
                dots.append((j, i))
    return dots, centroid
##############################################获取区域内的所有的像素点


##############################################单个计算
pic = input('please input picture links:')
with open('.'.join(pic.split('.')[:-1]) + '.log', 'w') as f:
    f.write('Selection Records:\n')
    f.write('Select Region\tDots_Number\tMean_Value\tRegion_Center\n')
img = io.imread(pic)
image = io.imread(pic, as_gray=True)
Dots, all_dots = [], []
results = []  # record results
centroids = {}
i = 1
while True:
    border = []
    fig = plt.figure()
    fig.canvas.mpl_connect('motion_notify_event', OnMouseMotion)
    fig.canvas.mpl_connect('button_press_event', OnPress)
    ax = fig.add_subplot(111)
    ax.imshow(img)
    for key, value in centroids.items():
        ax.text(value[0], value[1], str(key), color='white')
    plt.show()
    try:
        dots, centroid = Get_dots_in_border_region(border)
    except TypeError:
        print('The selected point exceeds the picture boundary,please reselect again')
        continue
    except ValueError:
        print('No area is selected, all regions have been selected?')
        input3 = input('y=yes,n=no:')
        if input3 == 'y' or input3 == '':
            break
        else:
            continue
    img0 = img.copy()
    for dot in dots:
        img0[dot[0], dot[1]] = [255, 0, 255]
    print('for region %s, select or not:' % i, end='')
    plt.imshow(img0)
    for key, value in centroids.items():
        plt.text(value[0], value[1], str(key), color='white')
    plt.show()
    input1 = input()
    if input1 == '' or input1 == 'y':
        Dots.append(dots)
        all_dots += dots
        ss = 0  # sum value of C-in dot
        nn = 0  # C-in dot number
        for dot in dots:
            img[dot[0], dot[1]] = [210, 105, 30]
            nn += 1
            ss += image[dot[0], dot[1]]
        meanv = round(ss / nn, 3)
        print('Dots number in this region are %s' % nn)
        print('Mean dots value in this region are %s' % meanv)
        centroids[i] = [int(centroid.x), int(centroid.y)]
        results.append(['region' + str(i), nn, meanv])
        with open('.'.join(pic.split('.')[:-1]) + '.log', 'a+') as f:
            f.write('region' + str(i) + '\t' + str(nn) + '\t' + str(meanv) + '\t(' + str(int(centroid.x)) + ',' + str(
                int(centroid.y)) + ')\n')
            f.write('All dots in this region:' + str(dots)[1:-1] + '\n')
        i += 1

##############################################单个计算
##############################################最终统计
print('All regions have been selected')
print('Calculating final results,waiting...')
n1 = n2 = 0  # n1:cin dot number,n2:cout dot number
sum1 = sum2 = 0  # sum1:sum value of cin dot,sum2: sum value of cout dot
for i in range(image.shape[0]):
    for j in range(img.shape[1]):
        if (i, j) in all_dots:
            n1 += 1
            sum1 += image[i][j]
        else:
            n2 += 1
            sum2 += image[i][j]
mean1 = round(sum1 / n1, 3)
mean2 = round(sum2 / n2, 3)
results.append(['Cin', n1, mean1])
results.append(['Cout', n2, mean2])
df = pd.DataFrame(results)
df.rename(columns={0: 'Select Region', 1: 'Dots Number', 2: 'Mean Value'}, inplace=True)
df.to_excel('.'.join(pic.split('.')[:-1]) + '.xlsx', index=None)
io.imsave('.'.join(pic.split('.')[:-1]) + '-selected.tif', img)
print('Finished successfully')
##############################################最终统计
