Lightweight Python application for the creation of items for tabletop role playing games.

When you first launch the project, it will open with a blank workflow.
Along the bottom edge, the application will display your currently active project.
You can create new items via the file menu, pressing Control N, or the New Item button located in the bottom left.
New items by default load with an incrementing name, and no items may share the same name.
To edit an existing item, double click on the item in the scrollbox to make it your active item, then you may change the name and description as you wish, and can save changes by pressing the save button located below the description.
To delete items, select them in the scrollbox and press delete (not backspace).
To save your current project, you can either use the file menu option or press control s. This will overwrite the existing project on your drive.
To save as a new file, you can use the file menu option or control shift s. This will open a dialog box for you to save the project.
To load your most recent project, you can use the file menu option or press control shift o. If you dont have a recent project or it cannot find it, it will prompt you to select your file.
To open any project, you can use the file menu option or press control o. This will open a dialog box so you may navigate to and select the file.
On quit, either by the hotkey control escape, the file menu or by pressing the x, it will prompt you to ensure you do not quit without making a save if desired.

Items are saved into a json file, which can then be edited outside of the application if desired. As long as you maintain the 'name' and 'description' field structure, it should be able to be reloaded.

A config file is created in the Config Files sub directory. This will be used to store more in the future, but at the moment it only stores the path to your most recent project.

