# FilterBox Component

The FilterBox is a React component that allows users to create filters based on certain conditions. It provides a drop-down list for selecting columns, conditions, and a text box for entering the desired value.

## Usage

```jsx
<FilterBox columns={columns} onRemoveFilter={onRemoveFilter} index={index} updateFilter={updateFilter} />
```

## Props

| Prop            | Type     | Description                                                                                                   |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| columns         | string[] | An array of column names to be displayed in the column selection dropdown.                                    |
| onRemoveFilter  | function | A function that will be called when the remove filter button is clicked.                                      |
| index           | number   | The index of the current filter box. Used for identification purposes when multiple filter boxes are present.|
| updateFilter    | function | A function that updates the filter based on the selected column, condition, and value entered by the user.    |

## States

| State           | Type     | Description                                                                                                   |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| selectedColumn  | string   | The currently selected column in the column selection dropdown.                                               |
| condition       | string   | The currently selected condition in the condition selection dropdown.                                         |
| value           | string   | The value entered by the user in the text box.                                                                |

## Functions

### setSelectedColumn

This function updates the `selectedColumn` state with the value selected by the user in the column selection dropdown.

### setCondition

This function updates the `condition` state with the value selected by the user in the condition selection dropdown.

### setValue

This function updates the `value` state with the value entered by the user in the text box.

## Styles

The component uses Tailwind CSS for styling. The main container has a padding of 4, a white background, rounded corners, and a medium shadow. Inside, the content is divided into rows and columns with a gap of 4. The text is gray and the borders of the dropdowns and text box are gray.