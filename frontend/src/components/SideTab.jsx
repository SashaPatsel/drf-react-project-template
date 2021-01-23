import React from "react";

const SideTab = props => (
  <div {...props} className={`tab ${props.otherclasses} ${props.active == "true" ? "tab__active" : "tab__inactive"}`}>
    {props.children}
  </div>
)

export default SideTab