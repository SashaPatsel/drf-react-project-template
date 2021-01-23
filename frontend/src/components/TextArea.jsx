import React from "react";

const TextArea = props => {
    let className = "form__textarea"
    if (props.ko) {
        className += " form__textarea--ko "
    }
    return (
        <div className="u-pos-relative" >
            <div className={className} {...props} contentEditable onInput={props.onChange}>
                {props.children}
            </div>
            <button onClick={props.onSubmit} className="form__textarea-submit">
                <span className="icon--md icon-icon__send"></span>
            </button >
        </div>
    )
}
export default TextArea