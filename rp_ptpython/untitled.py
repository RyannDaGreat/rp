#Settings
path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/EVSign/Templates/template.png'
#path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Keurig/Inputs/IMG_8238.jpg'
path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/HandicapButton/Templates/handicap_button_template.png'
path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Poptarts/Inputs/IMG_8217.jpg'
path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Reeses/Inputs/IMG_8213.jpg'
path='/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/NoParkingSign/Templates/noparking_template.png'

template_path = '/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Poptarts/Templates/IMG_8217.jpg'
training_paths=['/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Poptarts/Templates/IMG_8217.jpg',
                '/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Poptarts/Inputs/IMG_8224.jpg',
                '/Users/Ryan/Desktop/CleanCode/Zebra/2019/Images/Poptarts/Inputs/IMG_8217.jpg']#Paths to an image where there is only ONE template


pinch_radius=5
minarea=1000
scale= .5
dilate=2
blur=1

image=load_image(path)
image=resize_image(image,scale)
di= lambda x,w=0: cv_imshow(full_range(x),wait=1000000 if w else 0)


def min_pinch(contour):
    #This is impemented wrong because adjacent verts...this is an intresting geometrry puzzle. The thickness of a contour. but not tonight.....
    d=(distance_matrix(as_points_array(contour),as_points_array(contour)))
    d=d+np.eye(*d.shape)*10000
    return np.min(d)
def pinch_test(contour,radius=4):
    o=cv_find_contours(cv_erode(as_byte_image(contour_to_image(contour,fill=True)),radius,circular=True))
    print(len(o))
    return 1==len(o)
def squeezyness(contour,):
    return cv_contour_area(contour)/(cv_contour_length(contour)/pi)**2

contours=cv_find_contours(cv_dilate(auto_canny(gauss_blur(image,blur)),dilate))
contours=[contour for contour in contours if contour.is_outer and not contour.is_solid_white and cv_contour_area(contour)>minarea]
contours=[circ_gauss_blur(as_complex_vector(evenly_split_path(x))) for x in contours]
ccopy=contours.copy()
i=image//4
i=cv_draw_contours(i,contours)
contours=[c for c in contours if pinch_test(c,pinch_radius)]
i=cv_draw_contours(i,contours,(255,0,0))

def descriptor(contour):
   return normalized(np.abs(np.fft.fft(circ_diff(as_complex_vector(contour)))))
def min_dist(contour):
    m=1000000
    for c in ccopy:
        if c is not contour:
            m=min(m,euclidean_distance(descriptor(c),descriptor(contour)))
    return m            
            
contours=sorted(contours,key=min_dist,reverse=True)

i=cv_draw_contours(i,contours[:6],(0,255,0),1)
i=cv_draw_contours(i,contours[:3],(0,255,64),2)
i=cv_draw_contours(i,contours[:2],(0,255,128),3)
i=cv_draw_contours(i,contours[:1],(0,255,255),4)
di(i,0)