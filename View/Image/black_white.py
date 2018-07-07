import cv2, numpy

img = cv2.imread('Darkviolet.png', cv2.IMREAD_UNCHANGED)
for ridx, row in enumerate(img):
	for cidx, col in enumerate(row):
		if img[ridx, cidx, 3] != 0:
			img[ridx, cidx, :] = numpy.array([0, 0, 0, 255])
cv2.imwrite('Darkviolet_bw.png', img)