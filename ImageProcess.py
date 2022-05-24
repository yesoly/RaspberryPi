import numpy as np
import cv2

Color_Lower = (0,0,200)
Color_Upper = (180,255,255)

def check_RED(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    #Red HSV Range
    low_red=np.array([157,56,0])
    high_red=np.array([179,255,255])
        
    mask=cv2.inRange(hsv,low_red,high_red)
    blur=cv2.GaussianBlur(mask,(15,15),0)
    contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    status=0
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>20000:
            status=1
            cv2.drawContours(image,contour,-1,(0,0,255),3)
            cv2.putText(image,'RED STOP',(240,320), font, 2,(0,0,255),2,cv2.LINE_AA)     
    
    return (image,status)

def interest_region(image):
    height=image.shape[0]
    width=image.shape[1]
    region = np.array([[(100,height),(width-100,height),(width-130,height-140),(130,height-140)]])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,region,255)
    return mask

def average_slope_intercept(lines,image):
    left_fit=[]
    right_fit=[]
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            parameters=np.polyfit((x1,x2),(y1,y2),1)
            slope=parameters[0]
            intercept=parameters[1]
            if slope<0:
                right_fit.append((slope,intercept))
            else:
                left_fit.append((slope,intercept))                
    
    return len(left_fit), len(right_fit)

def draw_lines(lines,image):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if len(line)>0:                    
                x1,y1,x2,y2=line.reshape(4)
                cv2.line(line_image,(x1,y1),(x2,y2),[0,255,0],10)
    return line_image

def line_detect(image):
    blur=cv2.GaussianBlur(img, (7,7), 0) # 1. 가우시안블러
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # 2. RGB 색공간을 HSV 색공간으로 변환
    mask = cv2.inRange(hsv, Color_Lower, Color_Upper) # 3. 흰색에 해당하는 범위만 남기고 나머지는 검정색으로 
    canny=cv2.Canny(mask,50,150) # 4. Canny Edge detection (50, 150)은 임곗값 작을수록 세밀한 직선도 추출해낸다.
    region = interest_region(canny) # 5. 이미지 하단의 관심 부분(도로영역)만 짤라내서
    cut_img = cv2.bitwise_and(canny, region) # 6. 비트 연산자해서 도로만 남긴다
    lines= cv2.HoughLinesP(cut_img, 1, np.pi/180, 30, np.array([]), minLineLength=20, maxLineGap=5) # 7. Hough(하프) 연산으로 직선을 나타내는 점 추출
    left, right = average_slope_intercept(lines, image) 
    
    line_img = draw_lines(lines, img) # 점을 이용해서 직선의 방정식에 대입해 직선 그리는 함수
    img = cv2.addWeighted(img,1,line_img,1,0) # 기존 이미지랑 라인이랑 합침
 
    return left, right, img

