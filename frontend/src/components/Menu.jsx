import React, { Component } from "react";
import { Link } from "react-router-dom";

/* 
  STYLED @ /sass/components/menu.scss
  STYLEGUIDE @ /style_guide#menu
  
  PROPS
  __textColor__ 
  Description: Determines the color of the text for menu options. White by default 
  Type: String
  Values: "yellow"

*/

class Menu extends Component {

  state = {
    menuClasses: "menu",
    optionClasses: "menu__option"
  }

  componentDidMount() {
    let optionClasses = "menu__option"
    let menuClasses = "menu"
    if (this.props.dark) {
      menuClasses += " menu--dark"
    }
    this.setState({ menuClasses, optionClasses })
  }


  render() {
    return (
      <div className={this.state.menuClasses}>
        {this.props.options.map((option, i) => (
          <div className={this.state.optionClasses} key={i} onClick={option.onClick ? option.onClick : () => {}}>
            {option.link ?
              <Link to={option.link}>
                <p className="paragraph__2 paragraph__2--ko">
                  {option.name}
                </p>
              </Link>
              :
              <div>
                <p className="paragraph__2 paragraph__2--ko">
                  {option.name}
                </p>
              </div>
            }
          </div>
        ))}
      </div>
    )
  }
}

export default Menu