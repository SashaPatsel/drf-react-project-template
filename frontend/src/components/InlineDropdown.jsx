import React, { Component } from "react";


class InlineDropdown extends Component {
  // Dismisses the Inlinedropdown when another element is clicked
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
    if (this.container.current && !this.container.current.contains(event.target)) {
      this.setState({
        active: false,
      });
    }
  };

  render() {
    return (
      <div className="inline-dropdown" ref={this.container}>
        <button className="inline-dropdown__btn" onClick={this.open}>
          {this.props.title}
        </button>
        <div className="inline-dropdown__content">
          {this.state.active ? this.props.children : null}
        </div>
      </div>
    )
  }
}

export default InlineDropdown
