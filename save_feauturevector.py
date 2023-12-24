import sys
#import facenet
import faceinsight

if __name__ == '__main__':
#     args = sys.argv
#     if 2 <= len(args):
#         print(args[1], args[2])
# #        facenet.save_feature_vector(args[1], args[2])
#         faceinsight.save_feature_vector(args[1], args[2])
    faceinsight.save_feature_vector('images', 'facedb3')
