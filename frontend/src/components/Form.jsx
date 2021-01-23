import React from "react";

const Form = props => (
  <form {...props} className={`form ${props.otherclasses}`}>
    
      {props.children}
    
  </form>
)
export default Form