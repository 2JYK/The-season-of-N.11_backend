import cv2 # 이미지나 영상을 로드하고 거기서 편집해서 보여줌
import numpy as np

net = cv2.dnn.readNetFromTorch('nst/models/instance_norm/udnie.t7')

img = cv2.imread('nst/imgs/01.jpeg') # 이미지 경로를 지정해 읽음

# 이미지 전처리
# 이미지 형태 => 높이, 너비, 채널 이라는 변수에 저장
h, w, c = img.shape

# 사이즈 조절(int(가로세로 비율 유지)은 소수점이 나올 수 있어서 사용)
img = cv2.resize(img, dsize=(500, int(h / w * 500)))
print(img.shape)

# 전처리 : 이미지의 각 픽셀에서 빼주는 연산을 자동으로 처리
# blobFromImage 차원변형(목적: 컴퓨터가 알아들을 수 있는 형태로 변환)> img.shape 와 blob.shape로 비교해보세요.
MEAN_VALUE = [103.939, 116.779, 123.680]
blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
print(blob.shape)

# 결과 추론 : 전처리한 결과값을 Input으로 지정한다. 
net.setInput(blob)
output = net.forward()

# 후처리
output = output.squeeze().transpose((1, 2, 0)) # squeeze: 차원을 줄임 / transpose: 차원변형한 것을 다시 거꾸로 > 우리가 보기 쉬움
output += MEAN_VALUE # 뺀걸 다시 더해줌 

output = np.clip(output, 0, 255) # MEAN_VALUE 더해주면 이미지가 255를 초과하는 경우가 있음으로 이미지 제한
output = output.astype('uint8') # 정수형태로 바꿔주어 사람이 볼 수 있는 형태로 바뀜

cv2.imshow('output', output) # 이미지 출력 > 'output'이란 윈도우에 output을 출력
cv2.imshow('img', img) # 이미지 출력 > 'img'이란 윈도우에 img을 출력
cv2.waitKey(0) # 이미지를 띄어주고 0을 누르면 사라짐

