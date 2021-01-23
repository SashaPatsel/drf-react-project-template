import React, { Component } from "react";

class Tab extends Component {
  container = React.createRef();
  state = {
    open: false
  }

  componentDidMount() {
    document.addEventListener("mousedown", this.handleClickOutside);
  }
  componentWillUnmount() {
    document.removeEventListener("mousedown", this.handleClickOutside);
  }

  toggle = e => {
    this.setState({
      open: !this.state.open
    })
  }

  handleClickOutside = event => {
    if (this.container.current && !this.container.current.contains(event.target)) {
      this.setState({
        open: false,
      });
    }
  };

  render() {
    return (
      <div className="map__tab" ref={this.container} onClick={this.props.onClick}>
        <div className="map__icon-box " value="search" onClick={this.toggle}>
          {this.props.img}
        </div>  
        <div className={this.state.open ?(`map__tab-content ${this.props.otherclasses}`) : (`map__tab-content u-inactive ${this.props.otherclasses}`) }>
          {this.props.children}
        </div>
      </div>
    )
  }
}

export default Tab