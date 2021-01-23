import React, { Component } from "react";
import Menu from "./Menu";

class Select extends Component {
  // Dismisses the Select when another element is clicked
  container = React.createRef();
  state = {
    active: false,
    title: "Select an option"
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
    if (this.container.current && !this.container.current.contains(event.target)) {
      this.setState({
        active: false,
      });
    }
  };

  render() {
    return (
      <div className="select" ref={this.container}>
        <button className={this.props.ko ? "select__btn select__btn--ko" : "select__btn"} onClick={this.open}>
          <div className="select__btn--title">
            {this.props.title ? this.props.title : this.state.title}
          </div>
          <div className="select__btn--icon">
            {this.state.active ?
              <i class="fas fa-angle-up"></i>
              :
              <i class="fas fa-angle-down"></i>
            }
          </div>
        </button>
        {this.state.active ?
          <div className="select__menu">
            <Menu
              options={this.props.options}
              ko={this.props.ko ? true : false}
            />
          </div>
          : null}
      </div>
    )
  }
}

export default Select
