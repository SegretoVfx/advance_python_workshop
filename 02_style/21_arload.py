import datetime
import os

import libFunc
import libLog
from Qt import QtCompat
from arUtil import ArUtil

TITLE = "load"
LOG = libLog.init(script=TITLE)


class ArLoad(ArUtil):
    def __init__(self):
        super(ArLoad, self).__init__()
        
        path_ui = f"{os.path.dirname(__file__)}/ui/{TITLE}.ui"

        self.wg_load = QtCompat.loadUi(path_ui)
        
        scene_cur_item_txt = self.wg_load.lstScene.currentItem().text()
        
        self.load_dir = self.data["project"]["PATH"][scene_cur_item_txt]
        self.file_name = self.wg_load.lstSet.currentItem().text()
        
        self.load_file = f"{self.load_dir}/{self.file_name}"
        
        scene_cur_item_data = self.data["rules"]["SCENES"][scene_cur_item_txt]
        self.scene_steps = len(scene_cur_item_data.split("/"))
        
        software_format = {
            y: x.upper() for x, y in self.data["software"]["EXTENSION"].items()
        }
        self.software_keys = list(software_format.keys())
        
        self.wg_load.lstStatus.clear()
        self.wg_load.lstScene.clear()
        self.wg_load.lstSet.clear()
        self.clear_meta()
        self.resize_widget(self.wg_load)
        self.wg_load.show()
        
        LOG.info("START : ArLoad")
    
    def is_path_exists(self):
        """Set status message in case of file path doesn't exist.

        Returns:
            False : if path doesn't exist
        """
        if not os.path.exists(self.load_file):
            self.set_status(
                f"FAILED LOADING : Path doesn't exists: {self.load_file}",
                msg_type=3,
            )
            return False
    
    def add_menu_item_folder(self):
        """Add a menu folder using 'start' module with no file.  
        """
        import arSaveAs
        
        arSaveAs.start(new_file=False)
    
    def sort_menu(self, list_widget, reverse=False):
        """Sort the input list, with option to reverse the sorting.

        Args:
            list_widget (dictionary): list of all the widgets.
            reverse (bool, optional): Reverse sorting option. Defaults to False.

        Returns:
            list : sorted list
        """
        file_list = []
        for index in range(list_widget.count()):
            file_list.append(list_widget.item(index).text())
        list_widget.clear()
        list_widget.addItems(sorted(file_list, reverse=reverse))
        return list_widget
    
    def change_list_scene(self):
        """ Does something I don't know what.
        """
        tmp_content = libFunc.get_file_list(self.load_dir)
        
        if self.scene_steps < 5:
            self.wg_load.lstAsset.hide()
        else:
            self.wg_load.lstAsset.itemSelectionChanged.connect(
                self.change_lstAsset
            )
            self.wg_load.lstAsset.show()
        self.wg_load.lstSet.clear()
        
        if tmp_content:
            self.wg_load.lstSet.addItems(sorted(tmp_content))
            self.wg_load.lstSet.setCurrentRow(0)
    
    def change_list_set(self):
        """Does something I don't know what.
        """
        set_cur_item_txt = self.wg_load.lstSet.currentItem().text()
        new_path = f"{self.load_dir}/{set_cur_item_txt}"
        tmp_content = libFunc.get_file_list(new_path)
        
        if self.scene_steps < 5:
            self.wg_load.lstTask.clear()
            if tmp_content:
                self.wg_load.lstTask.addItems(sorted(tmp_content))
                self.wg_load.lstTask.setCurrentRow(0)
        else:
            self.wg_load.lstAsset.clear()
            if tmp_content:
                self.wg_load.lstAsset.addItems(sorted(tmp_content))
                self.wg_load.lstAsset.setCurrentRow(0)
    
    def change_list_asset(self):
        """Does something I don't know what.
        """
        lst_set_item_txt = self.wg_load.lstSet.currentItem().text()
        lst_asset_item_txt = self.wg_load.lstAsset.currentItem().text()
        
        new_path = f"{self.load_dir}/{lst_set_item_txt}/{lst_asset_item_txt}"
        
        tmp_content = libFunc.get_file_list(new_path)
        self.wg_load.lstTask.clear()
        
        if tmp_content:
            self.wg_load.lstTask.addItems(sorted(tmp_content))
            self.wg_load.lstTask.setCurrentRow(0)
    
    def fill_meta(self):
        """Fill the metadata with generated file info.
        label : Title
        label : Date
        label : File size
        """
        file_timestamp = os.path.getmtime(self.load_file)
        file_date_raw = datetime.datetime.fromtimestamp(file_timestamp)
        file_date = str(file_date_raw).split(".")[0]
        
        file_size_raw = os.path.getsize(self.load_file)
        file_size_mb = file_size_raw / (1024 * 1024.0)
        file_sie = f"{file_size_mb:.2f} MB"
        
        self.wgPreview.lblTitle.setText(self.file_name)
        self.wgPreview.lblDate.setText(file_date)
        self.wgPreview.lblSize.setText(file_sie)
    
    def clear_meta(self):
        """Clear the metadata.
        label : Title
        label : Date
        label : User
        """
        self.wgPreview.lblTitle.setText("")
        self.wgPreview.lblDate.setText("")
        self.wgPreview.lblUser.setText("")


def execute_ar_load():
    """
    instantiate the class ArLoad and set the global variable MAIN_WIDGET.
    """
    global MAIN_WIDGET
    MAIN_WIDGET = ArLoad()
