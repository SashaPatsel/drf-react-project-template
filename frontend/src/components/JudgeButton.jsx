import React from "react";

const JudgeButton = props => {  
  let type;
  if (props.type === "like") {
    type = "judgebutton__like"
  } else if (props.type === "dislike") {
    type = "judgebutton__dislike"
  }
  else if (props.type === "caution") {
    type = "judgebutton__caution"
  }
  return (
    <button {...props} className={`judgebutton ${type} ${props.otherclasses}`}>
      {(() => {
        if (props.type === "like") {
          return (
            <i className="fas fa-thumbs-up judgebutton__btn"></i>
          )
        } else if (props.type === "dislike") {
          return (
            <i className="fas fa-thumbs-down judgebutton__btn"></i>
          )
        }
        else if (props.type === "caution") {
            return (
              <span role="img" aria-label="shrug" className="judgebutton__shrug">🤷</span>
              )
        }
      })()}
    </button>
  )
}

export default JudgeButton