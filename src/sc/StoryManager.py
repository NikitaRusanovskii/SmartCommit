class StoryManager:
    def __init__(self, StoryFilePath: str,
                 mode: str,
                 encoding: str):
        self.path = StoryFilePath
        self.mode = mode
        self.encoding = encoding
        self.file = None
        self._contextIsActive = False

    def __enter__(self):
        self.file = open(self.path, self.mode, encoding=self.encoding)
        self._contextIsActive = True
        return self.file

    def upload(self, data: str = None):
        if self._contextIsActive:
            if self.file:
                if self.mode == 'a':
                    self.file.write(data)
                else:
                    raise RuntimeError(("Upload operation is allowed"
                                        "only in append ('a') mode"))
            else:
                raise RuntimeError("File is not opened")
        else:
            raise RuntimeError("Context manager is not active")

    def download(self) -> str:
        if self._contextIsActive:
            if self.file:
                return self.file.read()
            else:
                raise RuntimeError("File is not opened")
        else:
            raise RuntimeError("Context manager is not active")

    def clear(self):
        if self._contextIsActive:
            if self.file:
                return self.file.truncate(0)
            else:
                raise RuntimeError("File is not opened")
        else:
            raise RuntimeError("Context manager is not active")

    def __exit__(self, exc_type, exc, traceback):
        if self.file:
            self.file.close()
        self._contextIsActive = False
