import React, { useState, useEffect } from "react";

export default function RadioButton(props) {
  let buttonClass = "radio__button"
  let labelClass = "radio__label"
  if (props.ko) {
    buttonClass += " radio__button--ko"
    labelClass += " radio__label--ko"
  }

  return (
    <div className="radio__btn-group">
      <input type="radio" className="radio__input" id={props.name} name="size" defaultChecked={props.defaultChecked} />
      <label htmlFor={props.name} className={labelClass}>
        <span className={buttonClass} onClick={props.onClick} ></span>
      </label>
    </div>
  )
}