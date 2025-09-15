import BioImageHandler.BioImageHandler
import cv2 
import numpy as np
import matplotlib.pyplot as plt

class RastreadorNucleos(BioImageHandler):
    '''
        A partir de una bioimagen de un canal de fluorescencia de nucleos:
        - Detección y rotulo de los nucleos.
        - Obtención de un diccionario de tuplas (x,y) de sus coordenadas.
        - Determinación de su centroide.
        - Grafico comparativo de recuadros encerrando el núcleo y del centroide
        - Estadística de la fluorescencia de los nucleos en Unidades Arbitrarias de Fluorescencia.
    '''
    
    def __init__(self, rutaImagen, canalActual = None):
        super().__init__(rutaImagen) # Para herencia de BioImageHandler
        self.canalActual = canalActual
        self.imgActual = None
        self.imgProcesada = None
        self.num_nucleos = None
        self.imgRotulada = None
        self.centroides = None 
        self.coordenadasNucleos = None
        
    def procesarImagen(self, canal = 0, threshold = 0.5):
        '''
            Recibe un indice a un array de un array multidimensional de imagen. Por Default es 0.
            Si la imagen es un unico array,se devuelve la misma.
            Devuelve la imagen como tipo de bioio y la misma procesada a matriz binaria.
        '''
        
        img = leerBioImagen_bioformats()
        self.imgActual = img   
        
        forma_imagen = procesar_shape(img)
        
        if forma_imagen['canales'] > 1 : # Si no es una imagen 2D o 3D de un unico canal. 
            self.imgArrays = obtenerImagenesArray(img)
            img = self.imgArrays[canal]
            self.imgActual = img
            
        imgProcesada = convertirImgArray_AMAtriz(img)
        imgProcesada = normalizarImgMatriz(imgProcesada)
        imgProcesada = binarizarImgMatrizNorm(imgProcesada, threshold)
        self.imgProcesada = imgProcesada
        
        return img, imgProcesada
    
    def buscarNucleos(self, imgBinaria = None, tol_cerrada = 5, tol_abierta = 5):
        '''
            Toma una imagen binarizada de un canal de fluorescencia donde hay emisión desde nucleos y la procesa
            para rotular los grupos de pixeles correspondientes a cada nucleo. Realiza la siguientes operaciones:
            - Cierre morfológico : Une los huecos pequeños (tolerancia)
            - Apertura morfológica : elimina los objetos muy pequeños (Filtrado por tamaño)
            - Detectar componentes finales
        '''
        if imgBinaria is None:
            imgBinaria = self.imgProcesada
        
        # 1 - Cierre morfológico
        kernel_cerrado = np.ones((tol_cerrada, tol_cerrada), np.uint8)  # tamaño del kernel = tolerancia a ceros internos
        matriz_bin_cerrada = cv2.morphologyEx(imgBinaria, cv2.MORPH_CLOSE, kernel_cerrado)
        
        # 2 - Apertura morfológica 
        kernel_abierto = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tol_abierta, tol_abierta))
        mascara_filtrada = cv2.morphologyEx(matriz_bin_cerrada, cv2.MORPH_OPEN, kernel_abierto)
        
        # 3 - Detectar nucleos
        num_nucleos_filtrados, nucleos_filtrados = cv2.connectedComponents(mascara_filtrada, connectivity=8)
        self.num_nucleos = num_nucleos_filtrados - 1 # Se elimina el fondo
        self.imgRotulada = nucleos_filtrados
        
        return num_nucleos_filtrados, nucleos_filtrados
    
    def centroidesNucleos(self, num_nucleos = None, nucleos_filtrados = None):
        
        if num_nucleos is None:
            num_nucleos = self.num_nucleos
        if nucleos_filtrados is None:
            nucleos_filtrados = self.imgRotulada
        
        centroides = {}
        for nucleo in range(num_nucleos):
            coordenadas = np.column_stack(np.where(nucleos_filtrados == nucleo))
            centroide = coordenadas.mean(axis=0)
            centroides[f"nucleo_{nucleo}"] = (int(centroide[0]), int(centroide[1]))
        
        self.centroides = centroides
        
        return centroides
    
    def coordenadasNucleos(self, num_nucleos = None, nucleos_filtrados = None):
        
        if num_nucleos is None:
            num_nucleos = self.num_nucleos
        if nucleos_filtrados is None:
            nucleos_filtrados = self.imgRotulada
        
        coordenadasNucleos = {}
        for nucleo in range(num_nucleos):
            coordeandas = np.column_stack(np.where(nucleos_filtrados == nucleo))
            coordenadasNucleos[f"nucleo_{nucleo}"] = coordenadas.tolist()
        
        self.coordenadasNucleos = coordenadasNucleos
        
        return coordenadasNucleos
    
    def graficarNucleosRastreados(self, imgOriginal = None, coordenadasNucleos = None, coordenadasCentroides = None, titulo = None,
                                  centroideON = True, rectanguloON = True, rotulosON = True, colorRotulo = 'blue'):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        if imgOriginal is None:
            imgOriginal = self.imgActual
        if coordenadasCentroides is None:
            coordenadasCentroides = self.centroides
        if coordenadasNucleos is None:
            coordenadasNucleos = self.coordenadasNucleos
        if titulo is None:
            titulo = "Imagen original"

        # Subplot izquierdo: imagen original

        axes[0].imshow(imgOriginal, cmap='gray')
        axes[0].set_title(titulo)
        axes[0].axis('off')


        # Subplot derecho: con rectángulos y centroides

        axes[1].imshow(imgOriginal, cmap='gray')

        for nucleo in range(num_nucleos):
            coordenadas = np.column_stack(np.where(nucleos_filtrados == nucleo))
            min_fila, min_columna = coordenadas.min(axis=0)
            max_fila, max_columna = coordenadas.max(axis=0)

            # Dibujar rectángulo
            rectangulo = plt.Rectangle((min_columna - 1, min_fila - 1),
                                    max_columna - min_columna + 2, max_fila - min_fila + 2,
                                    edgecolor='red', facecolor='none', linewidth=1)
            if rectanguloON:
                axes[1].add_patch(rectangulo)


            # Dibujar centroide (más pequeño con markersize=4)
            centroide_fila, centroide_columna = centroides[f"obj_{nucleo}"]
            if centroideON:
                axes[1].plot(centroide_fila, centroide_columna, 'gx', markersize=2)


            # Etiqueta cerca del centroide
            if rotulosON:
                axes[1].text(centroide_columna + 20, centroide_fila + 1, f"nucleo_{nucleo}", color=colorRotulo, fontsize=8)

        axes[1].set_title("Nucleos detectados y delimitados")
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()
        