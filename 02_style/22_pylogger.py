# STYLE ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# ************************************************************************************


def find_caller_stack_frame(self):
    """
    Find the stack frame of the caller

    Returns:
        rv (str, int, str) : File name, line number, Function name
    """
    cur_frame = currentframe()

    # if IronPython isn't run with '-X:Frames' : currentframe() returns None.
    if cur_frame is not None:
        cur_frame = cur_frame.f_back

    while hasattr(cur_frame, "f_code"):

        frame_code = cur_frame.f_code
        file_name = os.path.normcase(frame_code.co_filename)

        if file_name == _srcfile:
            cur_frame = cur_frame.f_back
            continue

        return frame_code.co_filename, cur_frame.f_lineno, frame_code.co_name

    return "(unknown file)", 0, "(unknown function)"
