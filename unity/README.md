# Unity

The Project is designed to visualize a dataset of words in a 3D space using Unity's XR toolkit. Users can view words and see connections between similar words based on their clusters.

## Prerequisites

Before you begin, ensure you have the following:

- Unity installed (preferably the latest LTS version).
- Basic understanding of Unity’s interface and scripting.
- VR headset and controllers compatible with Unity.

## Project Setup

### Opening the Project in Unity

- Launch Unity Hub and click on `Add`.
- Select `Indw` folder and click `Add Project`.
- Open the project.
- all content written by our group is found under `/Assets/sripts`

### Setting up XR Interaction Toolkit (Normally this is already installed in the downloaded project)

#### Install XR Plugin Management

- Go to `Window` > `Package Manager`.
- Search for `XR Plugin Management` and install it.

#### Enable XR Plugin

- Go to `Edit` > `Project Settings` > `XR Plugin Management`.
- Enable the plugin for your specific VR headset (e.g., Oculus, OpenXR).

#### Install XR Interaction Toolkit

- Go to `Window` > `Package Manager`.
- Search for `XR Interaction Toolkit` and install it.

## Running the Project

- Play the scene in Unity and now you can see the clustered labels.
- Wear the VR headset if you want to get a better visual experience.

## Currently Disabled Features

Some features are disabled in the current version as they were not desired for the presentation. However the scripts are still available and can be reactivated by putting back a tick in the Unity inspector. Using the `Teleport Area Setup` requires to also reactivate the `Grid` as a basis for teleportation. Activating the `Spatial Panel Manipulator UI Example` script provides a Control Panel.

## Scripts

### `SpherePlacer.cs`

This script handles the interaction with the spheres representing words in VR, including highlighting and showing labels when a sphere is hovered over.

#### Basic Functionalities

##### Sphere Creation and Initialization

- Spheres are created based on the data from a text asset.
- Each sphere has its position and cluster information set.
- Spheres are assigned a unique color based on their cluster.

##### Label Creation and Initialization

- Labels are instantiated as child objects of the spheres.
- Labels display the name of the corresponding sphere.
- Labels are hidden by default and only shown when a sphere is interacted with.

##### Material Transparency

- Transparent materials are created for each cluster color.
- Materials are dynamically adjusted to be transparent when needed.

##### VR Interaction Setup

- The script is configured to work with VR controllers using ‘XRRayInteractor’ for interaction detection.
- Both left and right controllers can interact with the spheres.

##### Label Display and Timer Management

- Labels are shown when a sphere is pointed at or interacted with.
- Labels stay visible for a specified duration after interaction and then disappear.
- Timers for label visibility are managed using a coroutine.

##### Cluster-based Interaction

- When a sphere is interacted with, all spheres in the same cluster are highlighted.
- The labels for all spheres in the same cluster are shown when one sphere in the cluster is interacted with.

## Usage Guidelines for running `SpherePlacer.cs`

### Playing the Scene

- Select the `scripts` in the `Hierarchy`, check the `Sphere Placer (Script)` option and uncheck the `Label Placer (Script)` option in the `Inspector`.
- Ensure your VR headset is connected and configured.
- Play the scene in Unity Editor.

### Interacting with Spheres

- Use the VR controllers to point at and select spheres.
- Labels will appear when spheres are selected and remain visible for a short duration after pointing away.

### Customizing Data

- Update the `sample_data.txt` file with your data following the format: `word,x,y,z,cluster`.

### Customizing Appearance

- Adjust the `clusterColors` array in `SpherePlacer.cs` to change the colors associated with different clusters.
