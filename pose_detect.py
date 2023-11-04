import cv2
import time
import numpy as np

MODE = "MPI"

if MODE == "COCO":
    protoFile = "pose/coco/pose_deploy_linevec.prototxt"
    weightsFile = "pose/coco/pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

elif MODE == "MPI" :
    protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]


inWidth = 368
inHeight = 368
threshold = 0.1
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def set_openpose_device(device):
    if device == "cpu":
        net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
        print("Using CPU device")
    elif device == "gpu":
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")

def getpoints(hasFrame, frame):
    # Empty list to store the detected keypoints
    points = []
    t = time.time()
    frameCopy = np.copy(frame)
    if not hasFrame:
        return points

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                              (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 3, lineType=cv2.LINE_AA)
            cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    cv2.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv2.LINE_AA)
    # cv2.putText(frame, "OpenPose using OpenCV", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 50, 0), 2, lineType=cv2.LINE_AA)
    # cv2.imshow('Output-Keypoints', frameCopy)
    #debug
    # cv2.namedWindow("Output-Skeleton", cv2.WINDOW_NORMAL)
    # resized_frame = cv2.resize(frame, ((int)(frame.shape[1]), (int)(frame.shape[0])))
    # cv2.imshow('Output-Skeleton', resized_frame)
    # cv2.moveWindow('Output-Skeleton', 100, 100)

    return points

def crop_frame(p, frame):
#    print('p:', p)
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    #顔の中心算出
    fcx = int((p[0][0] + p[1][0]) / 2)
    fcy = int((p[0][1] + p[1][1]) / 2)
#    print('fcx:', fcx, 'fcy:', fcy)
    #顔のサイズ算出
    fwid = abs(p[0][0] - p[1][0])
    fhig = abs(p[0][1] - p[1][1])
#    print('fwid:', fwid, 'fhig:', fhig)
    #[縦上:縦下, 横左:横右]
    sy = fcy - fhig
    if sy < 0:
        sy = 0
    ey = fcy + fhig
    if ey > frame_height:
        ey = frame_height
    sx = fcx - fhig
    if sx < 0:
        sx = 0
    ex = fcx + fhig
    if ex > frame_width:
        ex = frame_width
#    print('sx:', sx, 'sy:', sy, 'ex:', ex, 'ey:', ey)
    #画像切り出し
    cropped_frame = frame[sy : ey, sx : ex]
    #debug
#    cv2.imwrite('cropped_frame.jpg', cropped_frame)

    return cropped_frame

