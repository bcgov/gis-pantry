# Labels

This section describes the basics of creating basic labels for features on your map

Index <br>
* [Accessing Labels](#accessing-labels)
* [Label Text](#label-text)
* [Label Options](#label-options)
* [Label Bar](#label-bar)

[QGIS Labeling Documentation](https://docs.qgis.org/testing/en/docs/user_manual/working_with_vector/vector_properties.html#labels-properties)

## Accessing Labels
Labels can be enabled and configured from two locations: 
1. The label dialog in the styling window <br>
![label-options-styling-panel-gif](../images/label-options-styling-panel.gif)
2. The Layer Properties Labels tab <br>
![label-options-layer-properties-dialog-gif](../images/label-options-layer-properties-dialog.gif)

In both configuration dialogs the options for labeling are identical.

## Label Text
Label text is controlled by the value setting which can be set using a field or by using an expression. Fields can be set using the drop down dialog or an expression can be built using the expression editor.
![label-value-expression-gif](../images/label-value-expression.gif)

In the expression dialog, fields and values can be coerced into the desired output value. An 'output preview' of the result can be seen in the bottom left of the dialog.<br>
Expression examples: <br>
1. Concatenate two fields
    ```
    Field2 || Field3
    ```
2. The length of line features concatenated with units<br>
    ```
    round($length,1) || ' m'
    ```

## Label Options
Label options can be set using dropdown selections or radio buttons. Most options can also be set using fields or expressions. For example the size of a polygon label can be set to be dependent on the geometry area.

The options are broken down into groups:
- Text Options (font, style, size, colour, opacity)
- Formating (type case, spacing, orientaiton, blending, line wrapping, numerical formatting)
- Buffer(Control buffer mask size, colour, opacity, etc)
- Background (create and control a background for your label)
- Shadow (drop shadow effect control)
- Callouts (draw and control line style between feature to label)
- Placement (placement relative to feature, repeating and overun controls, geometry generation, data defined locations, label priority)
- Rendering (mulitpart control, duplication reduction, feature label limits, feature priority)

## Label Bar 
![label-bar-image](../images/labelBar.png)<br>
The label bar contains several tools to help you edit your labels. From left to right these tools are:
- Layer Labeling Options: Opens the layer styling panel
- Layer Diagram Options: Opens a dialog allowing the user to add diagrams as labels
- Highlight Pinned Labels and Diagrams: Highlights labels that fixed in place due to manual placement
- Pin / Unpin Label or Diagram: Pins a label or diagram label in place on click (or unpins with shift + mouse click)
- Show / Hide Labels or Diagrams: Allows turning on and off labels for currently active features
- Move Label: Allows moving of labels and diagrams
- Rotate Label: Rotate label or diagram
- Change Label Properties: Change the properties (font weight, buffer, font size, etc) of individual labels on a map
