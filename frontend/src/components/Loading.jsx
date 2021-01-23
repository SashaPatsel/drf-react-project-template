import React, { useState, useCallback } from "react";
import staticLink from "../utils/static";

export default function Loading(props) {

  const initState = {
    imgClass: "loading__img"
  }

  const [state, setState] = useState(initState)

  useState(() => {
    let {imgClass} = state 
    if (props.size === "lg") {
      imgClass += " loading__img--lg"
    } else if (props.size === "sm") {
      imgClass += " loading__img--sm"
    } else {
      imgClass += " loading__img--md"
    }

    setState({...state, imgClass})
  })

  return (
    <div className="loading">
      <img src={`${staticLink}Rolling-1s-200px.svg`} alt="" className={state.imgClass}/>
    </div>
  )
}