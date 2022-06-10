# Progetto Panorama
 Creazione di un immagine panoramica unendo diverse foto

Image_Stitcher.py è uno script che permette di caricare diverse foto dalla cartella immagini e di unirle trovando innanzitutto delle feature comuni, poi di tagliare la foto panoramica creata prima trovando il rettangolo di grandezza massima che si adatta alla foto senza uscire dai bordi e senza avere buchi neri al suo interno

Image_cropper.py è uno script che taglia le foto panoramiche trovando il rettangolo massimo che si adatta meglio alla foto senza buchi neri. Questo script è stato implementato all'interno di Image_Stitcher.py.
