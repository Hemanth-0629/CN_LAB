import cv2
import numpy as np

query_image = cv2.imread('query_image.jpg')
ref_image1 = cv2.imread('ref_image1.jpg')
ref_image2 = cv2.imread('ref_image2.jpg')

query_image_gray = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
ref_image1_gray = cv2.cvtColor(ref_image1, cv2.COLOR_BGR2GRAY)
ref_image2_gray = cv2.cvtColor(ref_image2, cv2.COLOR_BGR2GRAY)

hist_query = cv2.calcHist([query_image_gray], [0], None, [256], [0, 256])
hist_ref1 = cv2.calcHist([ref_image1_gray], [0], None, [256], [0, 256])
hist_ref2 = cv2.calcHist([ref_image2_gray], [0], None, [256], [0, 256])

hist_query /= hist_query.sum()
hist_ref1 /= hist_ref1.sum()
hist_ref2 /= hist_ref2.sum()

bhattacharyya_distance1 = np.sqrt(np.sum(np.sqrt(np.multiply(hist_query, hist_ref1))))
bhattacharyya_distance2 = np.sqrt(np.sum(np.sqrt(np.multiply(hist_query, hist_ref2))))

print("Bhattacharyya Distance between query image and reference image 1:", bhattacharyya_distance1)
print("Bhattacharyya Distance between query image and reference image 2:", bhattacharyya_distance2)
