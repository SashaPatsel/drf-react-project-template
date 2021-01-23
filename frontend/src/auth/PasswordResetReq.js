import React, { Component } from "react";
import Form from "../components/Form";
import Auth from "./API";
import { toast } from 'react-toastify';
import utils from "../utils/utils";
import { Redirect } from "react-router-dom";

toast.configure({
  autoClose: 180000
})

class PasswordResetReq extends Component {
  state = {
    finished: false
  }

  handleChange = e => this.setState({ [e.target.name]: e.target.value });

  requestEmail = e => {
    e.preventDefault()
    const req = {
      email: this.state.email
    }
    Auth.emailReset(req)
    .then((res, err) => {
      if (err) {
        return err
      }
      utils.sendAlert("An email has been sent to the provided address. Follow the instructions within to reset your password.", "success")
    })
    .catch(err => {
      utils.sendAlert("There is no account associated with that email address. Please try again.", "error")
    })
  }

  render() {
    if (this.state.finished) {
      return <Redirect to='/' />
    }
    return (
      <div className="password__form-page">
        <div className="password__reset">

          <h1>Forgot your password?</h1>
          <p>Enter your email address below, and we'll email instructions for setting a new one.</p>

          <Form onSubmit={this.requestEmail}>
            <label htmlFor="id_email" className="form__label">Email</label>
            <input onChange={this.handleChange} className="form__input" type="email" name="email" maxLength="254" required id="id_email" />
            <input className="btn-alt u-mgn-top-sm" type="submit" value="Send me a link" />
          </Form>
        </div>
      </div>
    )
  }
}

export default PasswordResetReq
