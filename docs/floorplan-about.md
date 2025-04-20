# Floorplan Application Requirements

## Overview
This desktop application is designed to help home or apartment owners start with an image of a floorplan and then place furniture on it. The goal is to provide a sense of layout for a room or rooms based on the sizes of the room and the furniture selected.

## Target Audience
- Home or apartment owners

## User Roles
- This is a single-user application.

## Room Shapes
- Support both rectangular and irregular room shapes.
- Users can draw a simple rectangle over the floorplan and set the width and length of the room.
- For irregular room shapes, users can draw a polygon using individual line segments and enter the length of each segment. Not all segments need to have a size set.

## Furniture Properties
- Focus on dimensions of the furniture. The image will provide a sense of other properties.

## Grid Customization
- The grid should show 1-foot increments by default.
- Provide an option to enable inch increments.
- Display the grid on top of the floorplan and furniture in a light, non-distracting color.

## File Size Limits
- Do not support image sizes larger than 10MB.

## Help and Documentation
- Include tooltips on buttons to guide users.
- Detailed help and documentation within the application are not required.

## Advanced Features
- Save the floorplan as an FLPX file or as an image of the current view.
- Allow users to label each room on the floorplan.

## Room Labeling
- Use a default, simple-to-read font for room labels.
- Room labels should appear on top of the furniture in the room.
- Font and size of the room label cannot be changed.

## Furniture Rotation
- Provide simple options (buttons) to rotate furniture in 45-degree increments.
- Include options to flip furniture horizontally and vertically.
- Offer an advanced dialog to enter specific rotation degrees.

## Grid Units
- Support only feet and inches for grid measurements.

## Key Features
- Upload an image of a floorplan in 2D.
- Adjust the uploaded image (e.g., crop, zoom, remove background) to focus on the floorplan itself.
- Add room dimensions to the floorplan by drawing lines on the boundaries of the room and entering the size of each edge.
- Automatically create a scale for the room based on the entered dimensions, ensuring furniture is scaled correctly.
- Upload images of furniture and set their dimensions to match the scale of the floorplan.
- Maintain a list of added furniture images for easy selection and property adjustments (e.g., dimensions).
- Crop furniture images for aesthetic purposes without altering their dimensions.
- Rearrange and rotate furniture on the floorplan.
- Reset the floorplan or furniture images to their initial state or delete them to start over.
- Show/hide a grid on top of each room to measure it in common units (feet and inches).
- Support undo/redo actions for changes made to the floorplan or furniture.
- Allow up to 100 actions to be undone.
- Do not save undo/redo history between sessions.
- Save the floorplan as a ZIP file with an FLPX extension, including all images and positioning details, to allow reopening and editing.
- Open FLPX files to restore the floorplan and furniture to their previous state.

## Collaboration
- Save a floorplan with all associated images into a file that can be shared and opened by other users of the application.
- Save the current view of the floorplan as an image.

## Integration
- Insert images from the filesystem.
- Support common image formats for floorplans and furniture (e.g., JPEG, PNG, SVG, WEBP).
- No additional integrations are required at this time.

## Design Preferences
- The user interface should focus on clarity, ease of use, and simplicity.

## Localization
- The application will initially support English only.

## Performance
- Rooms will be displayed on a screen and can be resized to lower quality to improve performance.

## Deployment
- The application will be delivered as a Python file that can be run on desktop machines.

## User Workflow
1. Upload a floorplan image.
2. Select and adjust the floorplan image (crop, zoom, remove background).
3. Add room dimensions by drawing lines on the boundaries of the room and entering the size of each edge.
4. Automatically calculate the scale for the room based on the entered dimensions.
5. Upload furniture images and add them to the floorplan.
6. Maintain a list of added furniture images for selection and property adjustments (e.g., dimensions).
7. Move and rotate furniture on the floorplan.
8. Save the floorplan as a ZIP file (FLPX extension) with all images and positioning details.
9. Open FLPX files to restore the floorplan and furniture to their previous state.

## Error Handling
- Gracefully handle errors (e.g., notify the user if an image cannot be loaded and allow retry).
- Prevent invalid input for dimensions.
- Highlight overlapping furniture with a red boundary until the overlap is resolved.

## Accessibility
- Follow standard best practices for accessibility.
- Support keyboard navigation.

## Versioning
- Automatic versioning is not required. Users can save different versions of floorplans as needed.

## Testing
- Add unit tests for each new feature.
- Run unit tests regularly to ensure continued functionality as features are added.

## Monetization
- This is a free application for personal use only.

## Startup Behavior
- Open with a blank canvas.
- Provide options to add a floorplan image or open an existing project.

## Error Logging
- Error logging is not required at this time.

## User Preferences
- Store the latest user preferences (e.g., grid settings) in the FLPX file.

## Image Editing Tools
- Cropping should support rectangular crops with freeform adjustments of both height and width.
- Zooming should be controlled by buttons that increase or decrease by 5% increments.
- Background removal should be automatic:
  - For floorplans, focus on keeping the walls of the room and removing objects inside the rooms.
  - For furniture, remove the background of the image to allow overlapping and proper rendering.

## Room and Furniture Interaction
- Furniture should snap to the inch grid.
- Furniture should display a red boundary if it overlaps between rooms.

## Performance Optimizations
- The application should feel responsive and not hang when dragging furniture around.

## Keyboard Shortcuts
- `Ctrl+Z`: Undo.
- `Ctrl+S`: Save the FLPX file.
- `Ctrl+O`: Open an FLPX file.
- Arrow keys: Move selected furniture left, right, up, or down by 1-inch increments.
- `Ctrl+Arrow keys`: Move selected furniture left, right, up, or down by 1-foot increments.
- `Alt+F`: Open the File menu.
- `Alt+O`: Activate the button on the canvas to upload a floorplan.

## Visual Feedback
- The furniture being interacted with should display a bounding box that does not conflict in color with the grid.

## Export Options
- Allow toggling the grid on/off when saving the floorplan as an image.
- Room labels should be included in the exported image.
- Legends and scales are not required in the exported image.

## Resizing Support
- The application window should allow resizing.
- All content within the window, including the floorplan and furniture, should resize dynamically to fit the new window size.