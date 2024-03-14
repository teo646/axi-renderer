from axiRenderer.objects.components import Object
from .river_surface import RiverSurface

class River(Object):
    def __init__(self, path, world):
        meshes = []
        river_surface = RiverSurface(path, world)

        meshes.append(river_surface.remove_dir())
        super().__init__(meshes)

