import React, { useState, useEffect } from 'react';

export default function InlineDropdown({ props, style, debug, initState }) {
  /* 
  InlineDropdown is a generic component that is a dropdown selector element for 
  the frontend. It is called "inline" because the dropdown component is a
  <span></span> element and can be inserted into text without triggering a /n.
  The "props" props takes an argument that is an array of single element dictionary.
  The key in the dictionary is the label of a dropdown selector element and the
  value is an arrow function to be triggered when the selector element is selected.
  E.G. "props" props for an inline dropdown menu with two items, "none", and "log" function,
  that sets the Raster state attribute `valuationFunction` to a new value upon each
  selection.
  const inlineDropdownProps = [
    {
      none: () => {
        raster.setState({ ...raster.state, valuationFunction: 'none' });
      },
    },
    {
      '(log fn.)': () => {
        raster.setState({ ...raster.state, valuationFunction: 'log' });
      },
    },
  ];
  The "style" props takes an argument that is a dictionary containing ref var names
  as the keys and SCSS classes as the values.
  E.G. "style" props
  const inlineDropdownStyle = {
    dropdownContent: 'hab-pla dropdown-content',
    dropdownContentHidden: 'hab-pla dropdown-content hidden',
  };
  */

  const inlineDropdownCompStateInit = {
    isVisible: false,
  };
  const [inlineDropdownCompState, setInlineDropdownCompState] = useState(
    inlineDropdownCompStateInit
  );
  const [selectedOption, setSelectedOption] = useState({});
  const [selectedIndex, setSelectedIndex] = useState(initState);

  useEffect(() => {
    setSelectedOption(props[selectedIndex]);
  }, [selectedIndex]);

  let dropdownContentClassName;
  inlineDropdownCompState.isVisible
    ? (dropdownContentClassName = style.dropdownContent)
    : (dropdownContentClassName = style.dropdownContentHidden);

  const dropdownContentElements = props.map((dropdownContentElement, index) => {
    let elementKey = Object.keys(dropdownContentElement)[0];
    return (
      <div
        className={style.dropdownContentItem}
        key={index}
        onClick={() => {
          dropdownContentElement[elementKey](index);
          setSelectedIndex(index);
          debug.function();
        }}>
        {elementKey}
      </div>
    );
  });

  return (
    <span
      className={style.dropdown}
      onClick={() => {
        setInlineDropdownCompState({
          ...inlineDropdownCompState,
          isVisible: !inlineDropdownCompState.isVisible,
        });
      }}>
      {Object.keys(selectedOption)[0]}
      <span className={dropdownContentClassName}>
        {dropdownContentElements}
      </span>
    </span>
  );
}

// Closes itself on select
// Executes action from props
// Changes the title