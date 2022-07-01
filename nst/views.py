from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import cv2 
import numpy as np
    
def magic(filestr, style):
    npimg = np.fromstring(filestr, np.uint8)
    input_img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    style = cv2.dnn.readNetFromTorch(f'nst/models/{style}')
    
    h, w, c = input_img.shape
    input_img = cv2.resize(input_img, dsize=(500, int(h / w * 500)))
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(input_img, mean=MEAN_VALUE)
    style.setInput(blob)
    output = style.forward()
    output = output.squeeze().transpose((1, 2, 0)) 
    output += MEAN_VALUE 
    output = np.clip(output, 0, 255) 
    output = output.astype('uint8')
    
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%s')
    return cv2.imwrite(f'nst/output/{time}.jpeg', output) 


class NstView(APIView):
    def post(self, request): 
        user = request.user
        output_img = magic(
                filestr=request.FILES['input'].read(),
                style=request.data.get('style', '') 
            )

        return Response({"output": output_img}, status=status.HTTP_200_OK)