import React, { Component } from "react";
import navInit from "../auth/navInit";
import authInit from "../auth/init";


class Landing extends Component {
  state = {
    isAuthenticated: false,
    thumbnail: ""
  }

  componentDidMount = () => {
    authInit(this)
  }

  render() {

    return (
      <div>
        {navInit(this, "navbar--clear")}

        <div className="container">
          <div className="index__center">

            <div className="index__content">
              <div className="index__heading--container">

                <h1 className="index__heading">Conservationist.io</h1>
              </div>
              <h6 className="index__beta">Beta</h6>
              <form id="searchIndex" action="" className="searchbar u-mgn-btm-medium">
                <input name="searchbar" type="text" className="searchbar__input searchbar__input--lg" placeholder="Search..." />
              </form>
              <div className="index__search" id="searchResults">

              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Landing