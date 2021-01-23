import React, { Component } from "react";
import API from "../auth/API";
import { Link } from "react-router-dom";
import Button from "./Button";
import Form from "./Form";
import Input from "./Input";
import Dropdown from "./Dropdown";
import { toast } from 'react-toastify';
import utils from "../utils/utils";
import utilsAPI from "../utils/API";
import staticLink from "../utils/static";
import {
  Modal,
  ModalBody
} from "reactstrap";
import { useState } from "react";

let notifications = []
let unreadNotifications = 0

const useSprites = `<use xlink:href="${staticLink}sprite.svg#icon-grid1" xmlns="${staticLink}sprite.svg#icon-grid1" xmlns:svg="${staticLink}sprite.svg#icon-grid1" xmlns:xlink="${staticLink}sprite.svg#icon-grid1"></use>`

// FOR TWO-TIER DEPLOYMENT
const tools = [
  {
    name: "Refined Range Mapping",
    link: "/rrm/dash"
  },
  {
    name: "ESA Doc Search",
    link: "https://esadocs.defenders-cci.org/"
  },
  {
    name: "Habitat Patrol",
    link: "/habitatpatrol"
  },
  {
    name: "Earthenticate",
    link: "/earthenticate"
  }
]

const acct = [
  {
    name: "User Guide",
    link: ""
  },
  {
    name: "Profile",
    link: ""
  },
  {
    name: "Settings",
    link: ""
  }
]

toast.configure({
  autoClose: 180
})

const Navbar = props => {
  const initState = {
    isAuthenticated: false,
    loginModalShow: false,
    signupModalShow: false,
    feedbackModalShow: false,
    account: {},
    feedback: "",
    fbName: ""
  }

  const [state, setState] = useState(initState)

 const componentDidMount = () => {

    setState({
      isAuthenticated: props.isAuthenticated
    })
  }
  
 const handleChange = e => setState({ [e.target.name]: e.target.value });
  
 const toggleLoginModal = () => {
    const status = state.loginModalShow;
    setState({
      loginModalShow: !status
    })
  }
  
 const toggleSignupModal = () => {
    const status = state.signupModalShow;
    setState({
      signupModalShow: !status
    })
  }
 const toggleFeedbackModal = () => {
    const status = state.feedbackModalShow;
    setState({
      feedbackModalShow: !status
    })
  }
  
  
 const submitFeedback = e => {
    e.preventDefault();
    toggleFeedbackModal()
    const { feedback, fbName } = state
    const req = { feedback, fbName }
    console.log("req", req)
    utilsAPI.submitFeedback(req)
    .then(res => {
      utils.sendAlert("Feedback submitted.", "success")
    })
  }
 const logIn = e => {
    e.preventDefault();
    const { liUsername, liPassword } = state
    const req = {
      username: liUsername,
      password: liPassword
    }
    API.logIn(req)
      .then(res => {
        const token = res.data.token
        localStorage.setItem("token", token)
        window.location.href = "/"
      }).catch(err => {
        console.log("err", err)
        toggleLoginModal()
        utils.sendAlert("Invalid username or password", "error")
      })
  }

  const signUp = e => {
    const app = this
    e.preventDefault();
    const data = {
      first_name: state.firstName,
      last_name: state.lastName,
      username: state.suUsername,
      email: state.email,
      password: state.suPassword,
      password2: state.suPasswordConfirm
    }
    API.register(data)
      .then(function (res, err) {
        if (err) {
          return err
        }
        app.toggleSignupModal()
        utils.sendAlert("Your request to sign up was successfully submitted. Please check the email at the address you entered to complete the sign up process.", "success")
        localStorage.setItem("tempPWord", app.state.suPassword)
      })
      .catch(err => {
        app.toggleSignupModal()
        utils.sendAlert("We were unable to process your request. Please make sure all fields are correct. It is also possible the submitted username or email is already taken.", "error")
      })
  }

 const google = () => {
    API.google({})
      .then(res => {
      })
  }

 const readNotifications = () => {
    utilsAPI.readNotifications(props.account.id)
    .then(res => {
      unreadNotifications = 0
      setState({feedback: ""})
    })
    .catch(err => {

    })
  }


    if (props.account && notifications.length === 0) {
      utilsAPI.getNotifications(props.account.id)
      .then(res => {
        unreadNotifications = 0
        notifications = res.data
        for (let i = 0 ; i < notifications.length ; i++) {
          if (!notifications[i].seen) {
            unreadNotifications ++
          }
        }
      })
    }
    return (
      <div>
        <nav className={props.navTheme}>
      
          <a href="/">
            <div className="navbar-brand navbar__logo--link">
              <img src={`${staticLink}logo.png`} alt="logo" className="navbar__logo" />
            </div>
          </a>
          
          <div className="navbar__right">
        
            <a href="/">
              <div className="navbar-brand navbar__logo--btm">
                <img src={`${staticLink}logo.png`} alt="logo" className="navbar__logo" />
              </div>
            </a>
            
            <div className="navbar__feedback" onClick={toggleFeedbackModal}>
              <i className="fas fa-comment-dots"></i>
            </div>

            <Dropdown
              items={tools}
              otherclasses="u-mgn-right-sm"
              img={<svg className="navbar__icon" dangerouslySetInnerHTML={{ __html: useSprites }}>
              </svg>}
            />
            {
              props.isAuthenticated || state.isAuthenticated ?
                <div className="u-center-flex">
                  <Dropdown
                    items={notifications}
                    otherclasses="u-mgn-right-sm"
                    img={<i className="fas fa-bell navbar__notifications"></i>}
                    notifications={true}
                    unreadNotifications={unreadNotifications}
                    secondaryClick={readNotifications}
                  />
                  <Dropdown
                    items={acct}
                    otherclasses="u-mgn-right-sm"
                    img={<img src={props.thumbnail || state.thumbnail} alt="profile thumbnail" className="navbar__thumbnail" id="profileDropBtn" />}
                    acct={true}
                  />
                </div> :
                <div className="btn-group">
                  <Button onClick={toggleLoginModal}>Log In</Button>
                  <Button onClick={toggleSignupModal}>Sign Up</Button>
                </div>
            }
          </div>
        </nav>

        {/* FEEDBACK */}
        <Modal isOpen={state.feedbackModalShow} toggle={toggleFeedbackModal}>
          <ModalBody className="d-flex justify-content-around align-items-center container modal__feedback">
              <p className="u-flex-start-self p-reg u-mgn-right-sm">
                Please use the textbox to the right to provide any feedback that comes to mind. You can use to report any bugs/inconvenicences you encountered, or to recommend any features you'd like to see added.
              </p>
              <Form onSubmit={submitFeedback}>
                <textarea name="feedback" id="" cols="25" rows="10" className="u-border-default form__textarea u-black" defaultValue="" onChange={e => handleChange(e)} ></textarea>
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black u-mgn-btm-sm"
                  label="Name (optional)"
                  type="text"
                  name="fbName"
                  onChange={handleChange}
                />
                <Button type="submit">Submit Feedback</Button>
              </Form>
          </ModalBody>
        </Modal>

        {/* Log In */}
        <Modal isOpen={state.loginModalShow} toggle={toggleLoginModal}>
          <ModalBody className="index__background--login d-flex justify-content-around align-items-center">
            <Form onSubmit={logIn}>
              <div className="form__group">
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Username"
                  type="text"
                  name="liUsername"
                  placeholder="Username"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Password"
                  type="password"
                  name="liPassword"
                  placeholder="Password"
                  onChange={handleChange}
                />
                <Link to="/accounts/password_reset_req" className="password__link">Forgot password or username?</Link>
              </div>
              <Button type="submit">Log In</Button>
            </Form>
            <h3 className="auth__or black-text-shadow">OR</h3>
            <a href="/login/google-oauth2/">
              <Button className="auth__btn">
                <img className="auth__google" src={`${staticLink}google-logo.png`} alt="Google logo" />
              </Button>
            </a>
          </ModalBody>
        </Modal>

        {/* Sign Up */}
        <Modal isOpen={state.signupModalShow} toggle={toggleSignupModal}>
          <ModalBody className="index__background--signup d-flex justify-content-around align-items-center">
            <Form onSubmit={signUp}>
              <div className="form__group">
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="First Name"
                  type="text"
                  name="firstName"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Last Name"
                  type="text"
                  name="lastName"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Username"
                  type="text"
                  name="suUsername"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Email"
                  type="email"
                  name="email"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Password"
                  type="password"
                  name="suPassword"
                  onChange={handleChange}
                />
                <Input
                  labelColor="u-white black-text-shadow"
                  otherclasses="u-black"
                  label="Confirm Password"
                  type="password"
                  name="suPasswordConfirm"
                  onChange={handleChange}
                />

              </div>
              <Button type="submit">Sign Up</Button>
            </Form>
            <h3 className="auth__or black-text-shadow">OR</h3>
            {/* <a href="/login/google-oauth2/"> */}
            <Button onClick={google} className="auth__btn">
              <img className="auth__google" src={`${staticLink}google-logo.png`} alt="Google logo" />
            </Button>
            {/* </a> */}
          </ModalBody>
        </Modal>
      </div>
    )
}


export default Navbar
