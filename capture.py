# 웹캠으로 사진찍기 (video_cam_take_pic.py)
import cv2

cap = cv2.VideoCapture(0)  # 0번 카메라 연결

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, frame = cap.read()  # 카메라 프레임 읽기
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 트랙바 함수 정의
def on_threshold(pos):
    _, dst = cv2.threshold(frame_gray, pos, 255, cv2.THRESH_BINARY)
    cv2.imshow('dst', dst)

cv2.namedWindow('dst')
cv2.createTrackbar('Threshold', 'dst', 0, 255, on_threshold)  # 임계값 범위 0~255
cv2.setTrackbarPos('Threshold', 'dst', 128)  # 임계값 초기값 128
b = cv2.getTrackbarPos('Threshold', 'dst')


while True:
    if cv2.waitKey(1) & 0xFF == ord('q'): #q면 종료
        print("YOU PRESS 'q")
        break
    ret, frame = cap.read()  # 카메라 프레임 읽기
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("VideoFrame", frame_gray)
    b = cv2.getTrackbarPos('Threshold', 'dst')
    ret, img_binary = cv2.threshold(frame_gray, b, 255, cv2.THRESH_BINARY)
    cv2.imshow("VideoFrame", img_binary)  # 이진 화면 출력

    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        pts = contours[i]
        if (90000 < cv2.contourArea(pts) < 150000):
            epsilon = 0.025 * cv2.arcLength(pts, True)
            approx = cv2.approxPolyDP(pts, epsilon, True)
            # cv2.drawContours(src, [approx], 0, (0, 0, 255), 3)

            if not cv2.isContourConvex(approx):
                continue

            if len(approx) == 4:
                cv2.drawContours(frame_gray, [approx], 0, (0, 0, 255), 3)
                cv2.imshow("src", frame_gray)


        if (90000 < cv2.contourArea(pts) < 130000):
            j = 0
            # for c in contours:
            # get the bounding rect
            x, y, w, h = cv2.boundingRect(pts)
            # to save the images
            cv2.imwrite('img_{}.jpg'.format(j), frame[y:y + h, x:x + w])
            # j += 1

cap.release()
cv2.destroyAllWindows()
