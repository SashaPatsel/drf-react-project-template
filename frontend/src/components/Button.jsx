import React from "react";

const Button = props => {
  let classes = "button"
  let type = ""
  if (props.buttonType === "primary") {
    classes += " button__primary"
    type = "button__primary"
    if (props.size === "small") {
      classes += " button__primary--sm"
    } 
    if (props.size === "large") {
      classes += " button__primary--lg"
    }
  } else if (props.buttonType === "secondary") {
    classes += " button__secondary"
    type = "button__secondary"
    if (props.size === "small") {
      classes += " button__secondary--sm"
    } 
    if (props.size === "large") {
      classes += " button__secondary--lg"
    }
  } else if (props.buttonType === "text") {
    classes += " button__text"
    type = "button__text"
  }


  if (props.ko) {
    let secondaryClass = classes.split(" ")
    secondaryClass = secondaryClass[1]
    let modifierClass = secondaryClass + "--ko"
    modifierClass = " " + modifierClass
    classes += modifierClass
  }

  if (props.small) {
    const smallClass = " " + type + "--sm"
    classes += smallClass 
  }

  return (
    // ko : boolean      
    // type: string (primary, secondary, text)      
    <a href={props.href}>
      <button {...props} className={classes}>
        {props.children}
      </button>
    </a>
  )
}
export default Button 