from abc import ABCMeta, abstractclassmethod
import importlib
import cv2 as cv

###顔認証モデルの継承クラス

class face(metaclass=ABCMeta):
    @abstractclassmethod
    def import_lib(self):
        pass

    @abstractclassmethod
    def get_facedb(self):
        pass

    @abstractclassmethod
    def recognize_face(self, frame):
        pass

class facenet_model(face):
    def import_lib(self):
        self.model = importlib.import_module('facenet')

    def get_facedb(self):
        return 'facedb2'
    
    def recognize_face(self, frame):
        max_sim, detect_name, fv = self.model.recognize_face(frame, 'facedb2')

        return max_sim, detect_name, fv

class insightface_model(face):
    def import_lib(self):
        self.model = importlib.import_module('faceinsight')

    def get_facedb(self):
        return 'facedb3'
    
    def recognize_face(self, frame):
        max_sim, detect_name, fv = self.model.recognize_face(frame, 'facedb3')
  
        return max_sim, detect_name, fv

if __name__ == '__main__':
    #カメラの設定　デバイスIDは0
    cap = cv.VideoCapture(0)
    #画面キャプチャ
    hasFrame, frame = cap.read()

    face_recog_model = facenet_model()
    face_recog_model.import_lib()
    print(face_recog_model.recognize_face(frame))

    face_recog_model = insightface_model()
    face_recog_model.import_lib()
    print(face_recog_model.recognize_face(frame))    