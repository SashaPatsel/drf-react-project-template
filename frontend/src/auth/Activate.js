import React, { Component } from "react";
import Navbar from "../components/Navbar";
import API from "./API"
import { Redirect } from "react-router-dom";
import utils from "../utils/utils";

class Activate extends Component {
  state = {
    finished: false
  }

  componentDidMount = () => {
    const search = window.location.search.substring(1);
    const queryObj = utils.queryParamsToObj(search)
    const { uid, token } = queryObj
    const req = { uid, token }
    console.log("req", req)
    const activate = this
    API.activate(req)
      .then(function (res) {
        const password = localStorage.getItem("tempPWord")
        const req = {
          username: res.data.username,
          password: password
        }
        API.logIn(req)
          .then(res2 => {
            localStorage.removeItem("tempPWord")
            const token = res2.data.token
            localStorage.setItem("token", token)
            activate.setState({
              finished: true
            })
          })
      })
      .catch(function (err) {
      })
  }

  render() {
    if (this.state.finished) {
      window.location.href= "/"
    }
    return (
      <div>
        <Navbar
          navTheme="navbar--clear"
          isAuthenticated={false}
          thumbnail=""
        />

      </div>
    )
  }
}

export default Activate