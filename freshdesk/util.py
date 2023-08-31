import gzip
import pathlib
import shutil


def ensure_directory(dir_path: pathlib.Path) -> pathlib.Path:
    """ Ensures directory. Checks if exists and creates it if necessary.

    Args:
        dir_path: Path to the directory.

    returns: pathlib.Path The path to the created or existing directory
    """
    path = pathlib.Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def output_data_to_file(data: str or bytes, filepath: pathlib.Path, compressed: bool = True):
    """ Outputs given data to a csv file and compressed the file if requested

    Args:
        data: Data to be streamed to a file
        filepath: Destination file path
        compressed: The file will or not be gziped
    """

    if compressed:
        filepath = filepath if str(filepath).endswith('.gz') else str(filepath) + '.gz'

    ensure_directory(pathlib.Path(filepath).parent)
    filepath_tmp = str(filepath) + '.tmp'

    write_mode = 'wt'
    if isinstance(data, (bytes, bytearray)):
        write_mode = 'wb'

    if compressed:
        with gzip.open(str(filepath_tmp), write_mode) as tmp_output_file:
            tmp_output_file.write(data)
    else:
        with open(str(filepath_tmp), write_mode) as tmp_output_file:
            tmp_output_file.write(data)

    shutil.move(str(filepath_tmp), str(filepath))
