class Scenery:
    def __init__(self, path_img_floor_layer, path_img_bottom_layer, path_img_upper_layer, path_csv_bottom_layer, path_csv_upper_layer):
        # Armazena o caminho das imagens
        self.img_floor_layer = path_img_floor_layer
        self.img_bottom_layer = path_img_bottom_layer
        self.img_upper_layer = path_img_upper_layer

        # Armazena o caminho da imagem correspondente em .csv
        self.csv_bottom_layer = path_csv_bottom_layer
        self.csv_upper_layer = path_csv_upper_layer

    
