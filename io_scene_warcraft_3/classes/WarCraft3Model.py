
class WarCraft3Model:
    def __init__(self):
        self.file = ''
        self.version = 800
        self.name = None
        self.meshes = []
        self.materials = []
        self.textures = []
        self.nodes = []
        self.sequences = []
        self.geoset_animations = []
        self.pivot_points = []

    def normalize_meshes_names(self):
        for mesh in self.meshes:
            mesh.name = self.name
