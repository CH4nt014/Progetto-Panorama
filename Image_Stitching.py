import numpy as np
import cv2
import glob
import imutils

# prende il percorso delle immagini di imput e inizializza la lista di immagini
image_paths = glob.glob("immagini/*.jpg")
images = []

# loop sul percorso delle immagini, carica ogni immagine e le aggiunge alla lista per la panoramica
for image in image_paths:
    img = cv2.imread(image)
    images.append(img)
    # cv2_imshow(img)
    # cv2.imshow(img)
    cv2.waitKey(0)

# inizializza l'oggetto imageStitcher ed effettuo l'unione delle immagini
imageStitcher = cv2.Stitcher_create()
error, stitched_img = imageStitcher.stitch(images)

# Se non c'è errore OpneCV ha unito le immagini con successo
if not error:

    # salva l'immagine panoramica creata sul disco e la mostro
    cv2.imwrite("stitchedOutput.png", stitched_img)
    # print("Stitched Img")
    # cv2_imshow(stitched_img)
    cv2.imshow("Stitched Img", stitched_img)
    cv2.waitKey(0)

    # crea un bordo di 10 pixel che circonda l'immagine unita
    stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

    # converte l'immagine unita in scala di grigi e crea una soglia in modo che tutti i pixel
    # maggiori di zero siano impostati a 255 (quelli in primo piano) mentre gli altri rimangono a 0
    # (background)
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    # mostra l'effetto ottenuto
    # print("Threshold Image")
    # cv2_imshow(thresh_img)
    cv2.imshow("Threshold Image", thresh_img)
    cv2.waitKey(0)

    # trova tutti i bordi esterni nell'immagine di soglia, quindi trova
    # il contorno "più grande" che sarà il contorno dell'immagine unita
    contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    ROI = max(contours, key=cv2.contourArea)

    # alloca memoria per la maschera che conterrà il riquadro di delimitazione rettangolare dell'area
    # dell'immagine unita
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(ROI)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    # crea due copie della maschera: la prima serve da regione rettangolare minima
    # la seconda serve per contare quanti pixel devono essere rimossi per ottenere il rettangolo minimo
    minRectangle = mask.copy()
    sub = mask.copy()

    # contniua a ciclare fin quando non ci saranno più pixel diversi da 0
    while cv2.countNonZero(sub) > 0:
        # erode la maschera rettangolare minima e sottrae l'immagine con soglia dalla maschera
        # in modo da poter conttare se ci sono pixel diversi da zero rimasti
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, thresh_img)

    # trova i contorni nella maschera ed estrae il rettangolo del selezione con coordinate (x, y)
    contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    ROI = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(ROI)

    # mostra l'effetto ottenuto
    # print("minRectangle Image")
    # cv2_imshow(minRectangle)
    cv2.imshow("minRectangle Image", minRectangle)
    cv2.waitKey(0)

    # usa la boundig box per estrarre l'immagine finale
    stitched_img = stitched_img[y:y + h, x:x + w]

    # salva l'immagine finale sul disco
    cv2.imwrite("stitchedOutputProcessed.png", stitched_img)

    # mostra l'immagine finale
    # print("Stitched Image Processed")
    # cv2_imshow(stitched_img)
    cv2.imshow("Stitched Image Processed", stitched_img)
    cv2.waitKey(0)


# notifica se la creazione dell'immagine panoramica fallisce a causa di pochi keypoint
else:
    print("Images could not be stitched!")
    print("Likely not enough keypoints being detected!")
