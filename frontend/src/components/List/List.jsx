import React from "react";

/*
  STYLED @ /sass/components/_list.scss
  STYLEGUIDE @ /style_guide#list
  
  PROPS
  __children__
  Description: The card component is NOT self closing. It is meant to be a parent to other JSX elements. 
  Type: JSX
  Values: JSX

*/ 

const List = props => {
  let listClass = "list"

  return (
    <ul className={listClass}>
      {props.children}
    </ul>
  )
}
export default List 