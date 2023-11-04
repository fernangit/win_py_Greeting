import sys
import facenet
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

#顔を検出して切り取る GPU使用
mtcnn = MTCNN(device='cuda:0', margin=10)

if __name__ == '__main__':
    ## args[1]:images inputpath
    ## args[2]:vector outputpath
    ## args[3]:input image
    args = sys.argv
    if 3 <= len(args):
        print(args[1], args[2])
#        facenet.save_feature_vector(args[1], args[2])
        detectname = facenet.compare_similarity(mtcnn(Image.open(args[3])), args[2])
        print('you are ', detectname)
    else:
        print('Arguments are too short')
