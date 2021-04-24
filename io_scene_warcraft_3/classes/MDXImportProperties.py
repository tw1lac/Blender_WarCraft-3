import bpy


class MDXImportProperties:
    def __init__(self):
        self.mdx_file_path = ''
        self.team_color = None
        self.bone_size = 1.0
        self.use_custom_fps = False
        self.fps = 30
        self.frame_time = 1.0

    def calculate_frame_time(self):
        if not self.use_custom_fps:
            self.fps = bpy.context.scene.render.fps
        self.frame_time = 1000 / self.fps
