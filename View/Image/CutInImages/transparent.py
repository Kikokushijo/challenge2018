import cv2, numpy, sys

def trans1():
	img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
	img = img // 2
	for ridx, row in enumerate(img):
		for cidx, col in enumerate(row):
			if img[ridx, cidx, 3] != 0:
				img[ridx, cidx, 3] = 235
	cv2.imwrite(sys.argv[1][:-4] + '_trans1.png', img)

def trans2():
	img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
	for ridx, row in enumerate(img):
		for cidx, col in enumerate(row):
			if img[ridx, cidx, 3] != 0:
				img[ridx, cidx, 3] = 235
	cv2.imwrite(sys.argv[1][:-4] + '_trans2.png', img)

if __name__ == '__main__':
	
	assert len(sys.argv) >= 3

	if sys.argv[2] == '1':
		trans1()
	elif sys.argv[2] == '2':
		trans2()
	elif sys.argv[2] == 'all':
		trans1()
		trans2()

