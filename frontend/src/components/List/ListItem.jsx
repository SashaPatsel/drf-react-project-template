import React from "react";

/*
  STYLED @ /sass/components/_list.scss
  STYLEGUIDE @ /style_guide#list
  
  PROPS

  __thumbnail__
  Description: Determines the image that will be rendered in the thumbnail space of a list item. If no argument is passed, no image is used. 
  Type: String
  Values: Path to an image

  __thumbnailRounded__
  Description: Determines whether the thumnail will be a circular image or a square. Only valid if props.thumbnail is true. 
  Type: Boolean
  Values: T/F

  __ko__
  Description: Determines the color of the list item. If true, the list will have a white/light background. 
  Type: Boolean
  Values: T/F

  __children__
  Description: The card component is NOT self closing. It is meant to be a parent to other JSX elements. 
  Type: JSX
  Values: JSX
*/ 

const ListItem = props => {
  let imageStyle
  let elementStyle = "list__item"

  if (props.thumbnailRounded) {
    imageStyle = "round"
  } else {
    imageStyle = "square"
  }

  if (props.ko) {
    elementStyle += " list__item--ko"
  }

  return (
    <li className={elementStyle}>
      {props.thumbnail ?
      <div className="list__item-thumbnail">
        <img alt="listThumbnail" src={props.thumbnail} className={`list__item-img list__item-img--${imageStyle}`} />
      </div>
      : null
      }
      <div className="list__item-body">
        {props.children}
      </div>
    </li>
  )
}
export default ListItem 