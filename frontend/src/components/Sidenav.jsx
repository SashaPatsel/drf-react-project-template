import React, { useState, useEffect } from "react";
/* 
  STYLED @ /sass/components/menu.scss
  STYLEGUIDE @ /style_guide#menu
  
  PROPS
  __arrow__ 
  Description: If true, an arrow is displayed on the dropdown button to show its current open status 
  Type: Boolean
  Values: T/F


*/
export default function Sidenav(props) {
  // Dismisses the dropdown when another element is clicked
  const container = React.createRef();
  const initState = {
    active: props.isOpen,
    style: {},
  }

  const [state, setState] = useState(initState)
  
  useEffect(() => {
    if (props.fullHeight) {
      const style = { height: "100vh" }
      setState({...state, style})
    }
    if (props.ko) {

    }
  }, []);

  function open(e) {
    setState({
      ...state,
      active: !state.active
    })
    if (props.onToggle) {
      props.onToggle()
    }
  }

  return (
    <div className={state.active ? "sidenav sidenav__active" : "sidenav"} style={state.style} >
      <button className={props.ko ? "sidenav__btn--ko" : "sidenav__btn"} onClick={open}>
        <div className={state.active ? "sidenav__btn--title u-font-bold" : "sidenav__btn--title"}>
          {props.title}
        </div>
        {props.arrow ?
          <div className={state.active ? "sidenav__btn--icon--left" : "sidenav__btn--icon--right"}>
            {state.active ?
              <span className="icon2-icon2-caret__up icon--sm"></span>
              :
              <span className="icon2-icon2-caret__up icon--sm"></span>
            }
          </div>

          : null}
      </button>
      <div className="sidenav__content">
        {state.active ? props.children : null}
      </div>
    </div>
  )

}
