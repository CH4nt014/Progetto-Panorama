import cv2

# Import your picture
input_picture = cv2.imread("immaginePanoramica.png")

# Color it in gray
gray = cv2.cvtColor(input_picture, cv2.COLOR_BGR2GRAY)

# Create our mask by selecting the non-zero values of the picture
ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

# Select the contour
cont, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# if your mask is incurved or if you want better results,
# you may want to use cv2.CHAIN_APPROX_NONE instead of cv2.CHAIN_APPROX_SIMPLE,
# but the rectangle search will be longer

cv2.drawContours(gray, cont, -1, (255, 0, 0), 1)
cv2.imshow("Your picture with contour", gray)
cv2.waitKey(0)

# Get all the points of the contour
contour = cont[0].reshape(len(cont[0]), 2)

# we assume a rectangle with at least two points on the contour gives a 'good enough' result
# get all possible rectangles based on this hypothesis
rect = []

for i in range(len(contour)):
    x1, y1 = contour[i]
    for j in range(len(contour)):
        x2, y2 = contour[j]
        area = abs(y2 - y1) * abs(x2 - x1)
        rect.append(((x1, y1), (x2, y2), area))

# the first rect of all_rect has the biggest area, so it's the best solution if he fits in the picture
all_rect = sorted(rect, key=lambda x: x[2], reverse=True)

# we take the largest rectangle we've got, based on the value of the rectangle area
# only if the border of the rectangle is not in the black part

# if the list is not empty
if all_rect:

    best_rect_found = False
    index_rect = 0
    nb_rect = len(all_rect)

    # we check if the rectangle is  a good solution
    while not best_rect_found and index_rect < nb_rect:

        rect = all_rect[index_rect]
        (x1, y1) = rect[0]
        (x2, y2) = rect[1]

        valid_rect = True

        # we search a black area in the perimeter of the rectangle (vertical borders)
        x = min(x1, x2)
        while x < max(x1, x2) + 1 and valid_rect:
            if mask[y1, x] == 0 or mask[y2, x] == 0:
                # if we find a black pixel, that means a part of the rectangle is black
                # so we don't keep this rectangle
                valid_rect = False
            x += 1

        y = min(y1, y2)
        while y < max(y1, y2) + 1 and valid_rect:
            if mask[y, x1] == 0 or mask[y, x2] == 0:
                valid_rect = False
            y += 1

        if valid_rect:
            best_rect_found = True

        index_rect += 1

    if best_rect_found:

        cv2.rectangle(gray, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.imshow("Is that rectangle ok?", gray)
        cv2.waitKey(0)

        # Finally, we crop the picture and store it
        result = input_picture[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]

        cv2.imwrite("immaginePanoramicaProcessata2.png", result)
        cv2.imshow("Immagine panoramica processata", result)
        cv2.waitKey(0)
    else:
        print("No rectangle fitting into the area")

else:
    print("No rectangle found")