import React from "react";
/*
  STYLED @ /sass/components/_card.scss
  STYLEGUIDE @ /style_guide#card
  
  PROPS
  __children__
  Description: The card component is NOT self closing. It is meant to be a parent to other JSX elements. 
  Type: JSX
  Values: JSX

  __position__
  Description: Determines whether or not the card will have a stripe, and where it will be placed within the card. 
  Type: String
  Values: top, bottom, null
*/ 

const CardStripe = props => {
  let positionClass
  if (props.position === "top") {
    positionClass = "card__stripe--top"
  } else if (props.position === "bottom") {
    positionClass = "card__stripe--bottom"
  }
  return (
    <div className={`card__stripe ${positionClass}`}>
      {props.children}
    </div>
  )
}
export default CardStripe 