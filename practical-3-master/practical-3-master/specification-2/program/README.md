CSC1034: Practical 2 - Specification 2
====================

When the program is ran a GUI will appear on screen. 

The program can be ran by either running the spec-2.py file in an IDE or by any other method, or by typing one of the 
following in the terminal

- pipenv run python -m specification-2.spec-2

or

- pipenv run python specification-2/spec-2.py

##Loading Images
- By default the program will load the images found in practical-3\resources\img .

- The user is able to choose a directory/folder as an input, from which all jpg, png and gif images will be collected.

- The user is also able to choose a selection of files as an input. These will be saved in a temporary directory.

##Saving Images

- By default when the save button is clicked, the images will be saved to the output folder found at 
practical-3\specification-2\output .

- The user is able to choose their own directory to save images to.

- Note - when saving any files with the same name as a file being saved will be overwritten by the new file.

## Options

Two options can be changed by the user:

- **Enable undo and redo** - This is enabled by default. When enabled, every change to the images will be recorded,
allowing the user to undo and redo these changes. When disabled, the history will be deleted, and no further history
will be recorded until this is enabled again

- **Apply to all images** - This is turned on by default. When enabled, any changes made will be applied to all images.
When disabled, any changes made will only be applied to the image currently being previewed.

## Features

- **Grayscale** - This converts the images to grayscale. There are two versions, grayscale and slow grayscale. Grayscale
converts the whole image to a grayscale image and then back to an RGB image. Slow grayscale goes through each pixel in 
each image and converts it to grayscale. This is a lot slower than the other method, but is there to show that it can 
be done in this method.

- **Convert to thumbnail** - This converts the images to a 128x128 thumbnail.

- **Rotate 90°** - This will rotate the images by 90° clockwise.

- **Apply colour change** - This can take up to 3 inputs found to the right. These inputs are a red, green, and blue
 value. These values are how much the relevant colour band will be multiplied by. For example, to increase the red
 colour band by 1.5x, then an input of 1.5 will be needed in the box for the R input.
 
 - **Apply brightness change** - This changes the brightness of images. The value for how much the brightness will be
 changed by. The input for this is a slider between 0.1 and 2. For example, if the slider is at 1.5 when the brightness
 changed button is pressed, then the brightness value of the images will be changed by 1.5x.
 
 - **Apply filter** - This applies a pre-determined filter to the images. The filter used can be set by the user by a
 drop down box. There are 10 filters available. Once one has been selected in the drop down box, when the user presses
 the apply filter button then the selected filter will be applied.
 
 - **Undo** - This will undo the last action done by the user. For example if the user increases the brightness by 1.5, 
 if they then press undo the images will go back to how they were before the brightness was increased. 
 
 - **Redo** - This will redo the last action that was undone by the user. For example if the user increases brightness
 by 1.5, then presses undo, and then presses redo, then the picture will be back to the state it was after the user
 increased the brightness. If something is undone, and then another action is taken, then the user is no longer able to
redo that undo, as this has been overwritten by the new action.

- **Reset images** - This will reset all the images to the state they were in before being modified. It does this by
reloading them form the input file. It could do this by saving a version of the images in memory before modifying them, 
but reloading them means that they do not need to be stored in memory, freeing up some memory. Because of this, if the
user selects their own individual files as an input, these files will be saved in a temporary directory. This will also
reset the history, meaning the user can not undo this action.

- **Choose input folder** - This allows the user to choose a folder which will be used as an input. All jpg, png and
gif files in this directory will be loaded. It will not collect images from directories within this folder. If there 
are a very large amount of images in this folder this may cause a memory issue if the 32 bit version of python is being
used, in which case there will be a message that will show up under the "Apply to images" box. This error will show up
until another action is taken. In the case of a memory error, no new files will be loaded and nothing will have changed.

- **Choose input files** - This allows the user to select a number of images to choose as an input. These files are put
into a list, and the files which are not jpg, png or gif are filtered out, and the remaining images are put in a
dictionary. These images are then saved to a temporary directory.

- **Choose output folder** - This allows the user to choose the directory that the images will be saved to when saved.

- **Save** - This will save the images to either the default directory or the output directory set by the user chosen
with the "Choose output folder" button.

- **Quit** - This will quit the application. Nothing will be automatically saved.

- **<<** - This button is found underneath the preview image. Pressing this will display the previous preview image. If
the currently displayed preview image is the first one (Preview Image (0)), then this will do nothing.

- **>>** - This button is found underneath the preview image. This button will display the next preview image. If the
preview image being displayed is the last one, then this button will do nothing.

- **Preview image** This will open a fullscreen preview of the current preview image in a new window. It should display
this with the systems default picture viewer.
