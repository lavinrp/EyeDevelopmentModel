from epithelium_backend.Epithelium import Epithelium
import pickle


def import_epithelium(file_path: str) -> Epithelium:
    """
    Loads an epithelium from a file. If an epithelium cannot be successfully loaded None is returned.
    :param file_path: Path to epithelium save file.
    """

    try:
        with open(file_path, "rb") as input_file:
            epithelium = pickle.load(input_file)
    except Exception:
        return None

    if isinstance(epithelium, Epithelium):
        return epithelium
    return None


def export_epithelium(epithelium: Epithelium, file_path: str) -> None:
    """
    Saves an epithelium to a file
    :param epithelium: The epithelium to save.
    :param file_path: The path to the file where the epithelium will be saved.
    :return:
    """

    with open(file_path, "wb") as out_file:
        pickle.dump(epithelium, out_file, protocol=pickle.HIGHEST_PROTOCOL)

def import_simulation_settings():
    print("Todo: import settings to somewhere")

def export_simulation_settings():
    print("Todo: export settings to somewhere")

