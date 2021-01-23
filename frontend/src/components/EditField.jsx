import React, { useState, useEffect } from "react";
import Input from "../components/Input";
import ReactTooltip from 'react-tooltip';
import { icon } from "leaflet";

export default function EditField(props) {

  const initState = {
    isEditing: false,
    [props.name]: props.inputValue,
    inputValue: props.inputValue,
    message: "Edit",
    inputName: props.name
  }

  const [state, setState] = useState(initState)

  let classes = "edit-field"
  let type = ""
  let pFont = "paragraph__2"
  let iconFont = "icon"
  if (props.textType === "primary") {
    classes += " edit-field__primary"
    type = "edit-field__primary"
  } else if (props.textType === "secondary") {
    classes += " edit-field__secondary"
    type = "edit-field__secondary"
  } else if (props.textType === "text") {
    classes += " edit-field__text"
    type = "edit-field__text"
  }

  if (props.ko) {
    let secondaryClass = classes.split(" ")
    secondaryClass = secondaryClass[1]
    let modifierClass = secondaryClass + "--ko"
    modifierClass = " " + modifierClass
    classes += modifierClass
    pFont += " paragraph__2--ko"
    iconFont += "--ko"
  }

  if (props.small) {
    const smallClass = " " + type + "--sm"
    classes += smallClass
  }

  function changeEditStatus(arg) {
    const { isEditing } = state

    if (isEditing) {
      setState({ ...state, isEditing: !isEditing, message: "Edit" })
    } else {
      setState({ ...state, isEditing: !isEditing, message: "Save", inputValue: state[props.name] })
    }
    if (arg === "save") {
      props.updateValueCB({inputValue: state.inputValue, updatedValue: state[props.name], elementName: state.inputName})
    }
  }

  function handleChange(e) {
    setState({ ...state, [e.target.name]: e.target.value })
  }

  return (
    <div className="edit-field">
      {state.isEditing ?
        <div className="edit-field__input">
          <Input value={state[props.name]} ko={props.ko ? true : false} name={props.name} onChange={handleChange} small={true}/>
        </div>
        :
        props.children
      }
      <a data-tip data-for={`editField-${props.name}`}>

        {state.isEditing ?
          // <span className="icon--ko icon2-icon2__check icon--md" onClick={() => changeEditStatus("save")}></span>
          <p className={`${pFont} u-hover-color-yellow`} onClick={() => changeEditStatus("save")}>DONE</p>
          :
          <span className={`${iconFont} icon-icon__edit icon--md`} onClick={() => changeEditStatus("change")}></span>
        }
      </a>
      <ReactTooltip id={`editField-${props.name}`} type='light'>
        <span className="u-color-blue">{state.message}</span>
      </ReactTooltip>
    </div>
  )
}
