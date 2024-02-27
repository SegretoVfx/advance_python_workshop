# ADVANCED
# ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# **************************************************************************

"""
CUBE CLASS

1. CREATE a class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate,
   scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely
formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3
    floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""


class Object:
    def __init__(self, name):
        self.name = name
        self._translate = [0.0, 0.0, 0.0]
        self._rotate = [0.0, 0.0, 0.0]
        self._scale = [1.0, 1.0, 1.0]
        self._color = [0.0, 0.0, 0.0]

    def translate(self, tx=0.0, ty=0.0, tz=0.0):
        self._translate = tx, ty, tz
        self.print_status("translate")

    def rotate(self, rx=0.0, ry=0.0, rz=0.0):
        self._rotate = [rx, ry, rz]
        self.print_status("rotate")

    def scale(self, sx=1.0, sy=1.0, sz=1.0):
        self._scale = [sx, sy, sz]
        self.print_status("scale")

    def color(self, r=0.0, g=0.0, b=0.0):
        self._color = [r, g, b]
        self.print_status("color")

    def print_status(self, ttype=None):
        if ttype == "translate":
            print(
                f"{self.name} translate values :  \n"
                f"translate x = {self._translate[0]}, \n"
                f"translate y = {self._translate[1]}, \n"
                f"translate z =  {self._translate[2]} \n\n"
            )
        elif ttype == "rotate":
            print(
                f"{self.name} rotate values :  \n"
                f"rotate x = {self._rotate[0]}, \n"
                f"rotate y = {self._rotate[1]}, \n"
                f"rotate z =  {self._rotate[2]} \n\n"
            )
        elif ttype == "scale":
            print(
                f"{self.name} scale values :  \n"
                f"scale x = {self._scale[0]}, \n"
                f"scale y = {self._scale[1]}, \n"
                f"scale z =  {self._scale[2]} \n\n"
            )
        elif ttype == "color":
            print(
                f"{self.name} color values : \n"
                f"red = {self._color[0]}, \n"
                f"green = {self._color[1]}, \n"
                f"blue =  {self._color[2]} \n\n"
            )
        else:
            print(
                f"{self.name} translate values :  \n"
                f"translate x = {self._translate[0]}, \n"
                f"translate y = {self._translate[1]}, \n"
                f"translate z =  {self._translate[2]} \n\n"
                f"{self.name} rotate values :  \n"
                f"rotate x = {self._rotate[0]},\n"
                f"rotate y = {self._rotate[1]}, \n"
                f"rotate z =  {self._rotate[2]} \n\n"
                f"{self.name} scale values :  \n"
                f"scale x = {self._scale[0]}, \n"
                f"scale y = {self._scale[1]}, \n"
                f"scale z =  {self._scale[2]} \n\n"
                f"{self.name} color values : \n"
                f"red = {self._color[0]}, \n"
                f"green = {self._color[1]}, \n"
                f"blue =  {self._color[2]} \n\n"
            )

    def update_transform(self, ttype, value):
        match ttype:
            case "translate":
                self.translate(value[0], value[1], value[2])

            case "rotate":
                self.rotate(value[0], value[1], value[2])

            case "scale":
                self.scale(value[0], value[1], value[2])

            case "color":
                self.color(value[0], value[1], value[2])


class Cube(Object):
    def __init__(self, name):
        super(Cube, self).__init__(name)


cube_1 = Cube("cube_1")
cube_1.update_transform("translate", [4, 4, 4])
cube_1.update_transform("scale", [0.9, 0.4, 0.4])
cube_1.print_status()

cube_2 = Cube("cube_2")
cube_2.update_transform("rotate", [7, 8, 4])
cube_2.update_transform("color", [1, 0.7, 0.4])
cube_2.print_status()

cube_3 = Cube("cube_3")
cube_3.update_transform("translate", [1, 1, 2])
cube_3.update_transform("rotate", [0, 45, 45])
cube_3.update_transform("scale", [2, 2, 2])
cube_3.print_status()
