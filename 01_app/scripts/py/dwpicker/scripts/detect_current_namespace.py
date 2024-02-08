import dwpicker
from .picker import detect_picker_namespace


picker = dwpicker.current()
if picker:
    namespace = detect_picker_namespace(picker.shapes)
