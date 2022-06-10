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
    # cv2.imshow(img)
    cv2.waitKey(0)

# inizializza l'oggetto imageStitcher ed effettuo l'unione delle immagini
imageStitcher = cv2.Stitcher_create()
error, stitched_img = imageStitcher.stitch(images)

# Se non c'è errore OpenCV ha unito le immagini con successo
if not error:

    # salva l'immagine panoramica creata sul disco e la mostro
    cv2.imwrite("immaginePanoramica.png", stitched_img)
    cv2.imshow("Immagine Panoramica", stitched_img)
    cv2.waitKey(0)

    # converte l'immagine unita in scala di grigi e crea una soglia in modo che tutti i pixel
    # maggiori di zero siano impostati a 255 (quelli in primo piano) mentre gli altri rimangono a 0
    # (background)
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    # mostra l'effetto ottenuto
    cv2.drawContours(gray, cont, -1, (255, 0, 0), 1)
    cv2.imshow("Immagine con i contorni", gray)
    cv2.waitKey(0)

    # trova tutti i punti del contorno
    contour = cont[0].reshape(len(cont[0]), 2)

    # assumiamo che un rettangolo con almeno due punti sul contorno dia dei risultati abbastanza buoni
    # prendiamo tutti i possibili rettangoli che si basano su questa ipotesi
    rect = []

    # aggiungo i rettangoli alla lista
    for i in range(len(contour)):
        x1, y1 = contour[i]
        for j in range(len(contour)):
            x2, y2 = contour[j]
            area = abs(y2 - y1) * abs(x2 - x1)
            rect.append(((x1, y1), (x2, y2), area))

    # il primo rettangolo di tutti i rettangoli ha l'area più grande,
    # perciò è la migliore soluzione se fitta bene nell'immagine
    all_rect = sorted(rect, key=lambda x: x[2], reverse=True)

    # prende il rettangolo più grande trovato, basato sul valore dell'area del rettangolo
    # solo se i bordi del rettangolo non si trovano fuori dall'immagine, nella parte nera

    # se la lista non è vuota
    if all_rect:

        best_rect_found = False
        index_rect = 0
        nb_rect = len(all_rect)

        # controlla se il rettangolo è una buona soluzione
        while not best_rect_found and index_rect < nb_rect:

            rect = all_rect[index_rect]
            (x1, y1) = rect[0]
            (x2, y2) = rect[1]

            valid_rect = True

            # cerca un'area nera nel perimetro del rettangolo
            x = min(x1, x2)
            while x < max(x1, x2) + 1 and valid_rect:
                # se trova dei pixel neri, allora parte del rettangolo è nera
                # perciò elimina questo rettangolo
                if mask[y1, x] == 0 or mask[y2, x] == 0: valid_rect = False
                x += 1

            y = min(y1, y2)
            while y < max(y1, y2) + 1 and valid_rect:
                if mask[y, x1] == 0 or mask[y, x2] == 0:
                    valid_rect = False
                y += 1

            if valid_rect: best_rect_found = True
            index_rect += 1

        if best_rect_found:
            cv2.rectangle(gray, (x1, y1), (x2, y2), (255, 0, 0), 1)
            cv2.imshow("Is that rectangle ok?", gray)
            cv2.waitKey(0)

            # croppa l'immagine e la salva
            result = stitched_img[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]

            cv2.imwrite("immaginePanoramicaProcessata.png", result)
            cv2.imshow("Immagine panoramica processata", result)
            cv2.waitKey(0)
        else:
            print("Nessun rettangolo si adatta bene all'immagine")

    else:
        print("Nessun rettangolo trovato")

# notifica se la creazione dell'immagine panoramica fallisce a causa di pochi keypoint
else:
    print("L'immagine non può essere unita!\nPochi keypoint trovati")
