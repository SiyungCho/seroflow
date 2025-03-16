"""
"""

from abc import abstractmethod
from ..utils.utils import check_directory, check_file, gather_files, remove_extension
from ..extract.extractor import Extractor, MultiExtractor

class FileExtractor(Extractor):
    """
    """
    def __init__(self, source, func, chunk_size, on_error, step_name="FileExtractor", **kwargs):
        """
        """
        super().__init__(step_name=step_name, func=func, chunk_size=chunk_size, on_error=on_error)
        if not check_file(source):
            raise FileNotFoundError("Error directory not found")
        
        self.source = source
        self.file_path = source
        self.file_name = remove_extension(source.split('/')[-1])
        self.kwargs = kwargs

    @abstractmethod
    def func(self, context):
        """
        """
        pass

    @abstractmethod
    def chunk_func(self, context, chunk_coordinates):
       """
       """
       pass

    @abstractmethod
    def get_max_row_count(self):
       """
       """
       pass

class MultiFileExtractor(MultiExtractor):
    """
    """
    def __init__(self, source, type, extension_type, chunk_size, on_error, step_name="MultiFileExtractor", **kwargs):
        """
        """
        super().__init__(step_name=step_name, type=type, chunk_size=chunk_size, on_error=on_error)
        if not check_directory(source): 
            raise FileNotFoundError("Error directory not found")

        self.source = source
        extension = self.identify_type(extension_type)
        self.file_paths, self.file_names = gather_files(self.source, extension)

        self.add_extractors(self.file_paths, kwargs)

    def identify_type(self, extension_type):
        """
        """
        if extension_type == 'csv':
            return ["csv"]
        elif extension_type == 'excel':
            return ["xlsx", "xls"]
        raise ValueError("Invalid file type")
