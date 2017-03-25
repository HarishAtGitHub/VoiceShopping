
class DataStore:

    def __init__(self, materials_file):
        # set materials
        with open(materials_file) as f:
            self.material_set = {line.strip() for line in f}
