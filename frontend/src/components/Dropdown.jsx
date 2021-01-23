import React, { Component } from "react";

class Dropdown extends Component {
  // Dismisses the dropdown when another element is clicked
  container = React.createRef();
  state = {
    active: false
  }

  componentDidMount() {
    document.addEventListener("mousedown", this.handleClickOutside);
  }
  componentWillUnmount() {
    document.removeEventListener("mousedown", this.handleClickOutside);
  }

  open = e => {
    this.setState({
      active: !this.state.active
    })
  }


  handleClickOutside = event => {
    if (this.container.current && !this.container.current.contains(event.target) && this.props.globalDismiss) {
      this.setState({
        active: false,
      });
    }
  };

  render() {
    return (
      <div className="dropdown">
        <button className="dropdown__btn" onClick={this.open}>
          <div className={this.state.active ? "dropdown__btn--title u-font-bold" : "dropdown__btn--title"}>
            {this.props.title}
          </div>
          <div className="dropdown__btn--icon">
            {this.state.active ?
              <span className="icon--ko icon2-icon2-caret__up icon--sm"></span>
              :
              <span className="icon--ko icon2-icon2-caret__down icon--sm"></span>
            }
          </div>
        </button>
        <div className="dropdown__content">
          {this.state.active ? this.props.children : null}
        </div>
      </div>
    )
  }
}

export default Dropdown
