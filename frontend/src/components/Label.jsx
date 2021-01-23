import React from "react";

const Label = props => {
    let className =  "form__label" 
    if (props.ko) {
        className += " form__label--ko "
    }
    return (
        <div>
            <label className={className}>{props.text}</label>
        </div>
    )
}
export default Label