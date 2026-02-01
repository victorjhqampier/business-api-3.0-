class MapperCommon:
    @staticmethod
    def map(source, destination):
        for attr, value in source.__dict__.items():
            if hasattr(destination, attr):
                setattr(destination, attr, value)