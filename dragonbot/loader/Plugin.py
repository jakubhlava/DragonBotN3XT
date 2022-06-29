class Plugin:

    def __init__(self, name):
        self.name = name
        self.load_str = f"plugins.{name}.{name}"
        self.loaded = False
        self.version = None
