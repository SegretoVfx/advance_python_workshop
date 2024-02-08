# workshop assignment

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [License](#license)
4. [Collaboration](#collaboration)
5. [Author](#author)

## Description
***
The project is to create a tool following the instruction of Alexander Richer TD
during an advanced python workshop taken for 8 weeks starting Jan 15th 2024.

The structure of the project shows 4 folders, each folder contains the 
assignments for each module of the workshop.

Workshop : https://www.alexanderrichtertd.com/

* **01_app** : Folder containing the tool I'll be working on during the workshop

* **02_style** : Folder containing the assignment on python style, usage and 
                 convention used for better readability of the code.
* **03_advanced** : Folder containing the solution of assignement for the course
* **04_ui** : Folder containing the solution of assignement for the course

This has been done for training purpose and no support will be given outside of 
the scope of the workshop.

## Installation
***
The tool present in the **01_app** folder is an animation path creation.

The animator can use the path to help the motion of a character, biped or 
quadruped. 
The root of the character will follow the path. 

Maya must be started using the _maya.bat_ file.

First, clone the repository into any location you want.

1. Open a CMD prompt where you want the repo to stand and type 
`git clone https://github.com/SegretoVfx/advance_python_workshop.git`
2. Simply double-click on the `maya.bat` file at the root of this repository.

**Maya** will open with all the needed `PATH` set correctly.


Once **Maya** is launched under the good environment,
you can launch the tool by typing into the *Maya script editor*.
You also can drag and drop this script to create a direct shelf button to the
world space tool.
```
import juls_anim_motion_path
juls_anim_motion_path.main()
```

A window will open up with all the instructions for using the tool.



## License
***
[MIT](https://choosealicense.com/licenses/mit/)

Copyright (c) 2024 Julien Segreto 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Collaboration
***
I don't know yet.

## Author
***
Julien Segreto
segretovfx@gmail.com


