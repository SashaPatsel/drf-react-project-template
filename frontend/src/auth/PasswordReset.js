import React, { Component } from "react";
import Form from "../components/Form";
import Auth from "./API";
import { toast } from 'react-toastify';
import utils from "../utils/utils";
import { Redirect } from "react-router-dom";

toast.configure({
  autoClose: 180000
})

class PasswordReset extends Component {
  state = {
    invalidToken: false,
    finished: false
  }

  componentDidMount = () => {
    let href = window.location.href
    href = href.split("token=")
    href = href[1].split("&username=")
    const token = href[0]
    const username = href[1]
    this.setState({username})
    Auth.checkResetToken(token)
    .then((res, err) => {
      if (err) {
        return err
      }
    })
    .catch(err => {
      utils.sendAlert("Your password reset token was invalid. You will be redirected to the home page shortly.", "error")
      setTimeout(() => {
        this.setState({
          invalidToken: true
        })
      }, 10000);
    })
  }

  handleChange = e => this.setState({ [e.target.name]: e.target.value });

  resetPassword = e => {
    e.preventDefault()
    const app = this
    if (this.state.password === this.state.passwordConfirm) {
      const req = {
        password: this.state.password,
        username: this.state.username
      }
      Auth.resetPassword(req)
      .then(resp => {
        Auth.logIn(req)
        .then(res => {
          const token = res.data.token
          localStorage.setItem("token", token)
          utils.sendAlert("Password reset.", "success")
          setTimeout(() => {
            app.setState({
              finished: true
            })
          }, 5000);
        })
      })
    } else {
      utils.sendAlert("Passwords do not match.", "error")
    }
  }

  render() {
    if (this.state.invalidToken || this.state.finished) {
      return <Redirect to='/' />
    }
    return(
      <div className="password__form-page">
        <div className="password__reset">            
            <h1>Set a new password!</h1>
            <Form onSubmit={this.resetPassword}>
                <label htmlFor="id_new_password1" className="form__label">New password</label>
                <input onChange={this.handleChange} type="password" className="form__input" name="password" required id="id_new_password1"/>
                <label htmlFor="id_new_password2" className="form__label">New password</label>
                <input onChange={this.handleChange} type="password" className="form__input" name="passwordConfirm" required id="id_new_password2"/>
                <input className="btn-alt u-mgn-top-sm" type="submit" value="Change password"/>
            </Form>
        </div>
      </div>
    )
  }
}

export default PasswordReset