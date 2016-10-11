import pylab
import imageio
filename = 'DataR/1R.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')

fig = pylab.figure()

myseq1 = None;
myseq2 = None;
for num in range(1, 5):
    image = vid.get_data(num)
    fig1 = pylab.figure(1)
    if myseq1 is None:
        myseq1 = pylab.imshow(image)
    else:
        myseq1.set_data(image)
    fig1.suptitle('image #{}'.format(num), fontsize=20)

    fig2 = pylab.figure(2)
    if myseq2 is None:
        myseq2 = pylab.imshow(image)
    else:
        myseq2.set_data(image)
    fig2.suptitle('image #{}'.format(num + 1), fontsize=20)
    pylab.pause(1)
    pylab.draw()
print "hello";


