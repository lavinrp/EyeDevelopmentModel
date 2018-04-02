from epithelium_backend.Epithelium import Epithelium
from quick_change import FurrowEventList
import pickle
import wx
from wx.core import TextCtrl


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


def import_simulation_settings(file_path: str) -> dict:
    """Loads simulation options and specialization options from a file
    :param file_path: Path to simulation save file.
    :return: a dictionary with values for updating the simulation options.
    The key is the label text of the StaticText in the simulation options scroll window.
    The value of the dict is the new value to be entered into the TextCtrl.

    No information about the furrow event list is returned. These values are set within the function.
    """
    try:
        with open(file_path, "rb") as input_file:
            # get inputs
            input = pickle.load(input_file)
            simulation_options_dict = input[0]
            imported_furrow_event_list = input[1]

            # update furrow event list
            for furrow_event in FurrowEventList.furrow_event_list:
                for imported_event in imported_furrow_event_list:
                    furrow_keys = set(furrow_event.field_types.keys())
                    imported_keys = set(imported_event.field_types.keys())
                    if furrow_keys == imported_keys:
                        for key, val in imported_event.field_types.items():
                            furrow_event.field_types[key] = val
                        break

            # return the simulation options for the caller to update
            return simulation_options_dict

    except Exception:
        return None


def export_simulation_settings(simulation_scroll_children: list, furrow_event_list: list, file_path: str):
    """
    Saves all simulation options and specialization options to a file.
    :param simulation_scroll_children: A list containing the the StaticText and TextCtrl widgets from the
    simulation settings scroll window.
    :param furrow_event_list: The furrow events to have options saved.
    :param file_path: Path to the save file.
    """
    simulation_options = dict()
    for i in range(len(simulation_scroll_children)):
        if isinstance(simulation_scroll_children[i], wx.StaticText):
            child = simulation_scroll_children[i]  # type: wx.StaticText
            text_ctrl = simulation_scroll_children[i + 1]  # type: TextCtrl
            simulation_options[child.GetLabelText()] = text_ctrl.GetValue()

    output = (simulation_options, furrow_event_list)

    with open(file_path, "wb") as out_file:
        pickle.dump(output, out_file, protocol=pickle.HIGHEST_PROTOCOL)

