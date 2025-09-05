import cv2

image = cv2.imread("Primer_Gauss.png")
blured_image = cv2.GaussianBlur(image, (7, 7), sigmaX=0)
     
cv2.imshow("Original", image)
cv2.imshow("Blured", blured_image)
     
cv2.waitKey(0) 
cv2.destroyAllWindows()