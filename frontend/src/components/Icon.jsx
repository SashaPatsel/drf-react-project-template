import React, { useState, useCallback } from "react";
import staticLink from "../utils/static";

export default function Icon(props) {

  const initState = {
    iconColor: "icon",
    iconShape: "icon-icon__",
    iconSize: "icon--md"
  }

  const [state, setState] = useState(initState)

  useState(() => {
    let { iconColor, iconShape, iconSize } = state

    if (props.size === "sm") {
      iconSize = "icon--sm"
    } else if (props.size === "lg") {
      iconSize = "icon--lg"
    } 

    if (props.icon === "caret-down" || props.icon === "caret-up" || props.icon === "close" || props.icon === "check" ) {
      iconShape = "icon2-icon2__"
    } 
    iconShape += props.icon

    if (props.ko) {
      iconColor += "--ko"
    }

    setState({...state, iconColor, iconShape, iconSize})
  })

  return (
    <div {...props}>
      <span className={`${state.iconColor} ${state.iconShape} ${state.iconSize}`}></span>
    </div>
  )
}