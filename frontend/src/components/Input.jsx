import React from "react";

const Input = (props) => {
  let className =  "form__input" 
  if (props.ko) {
      className += " form__input--ko "
  }

  if (props.small) {
    className += " form__input--sm "
  }
  return (
  <div>
    <input className={className} {...props}/>
  </div>
) }
export default Input