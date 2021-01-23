import React, {Component} from  "react";
import "./App.css";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Landing from "./pages/Landing";
import StyleGuide from "./pages/StyleGuide";
import StyleMax from "./pages/StyleMax";
import StyleSasha from "./pages/StyleSasha";
import ChangeDetection from "./apps/changedetection/ChangeDetection";
import ChangeDetectionMobile from "./apps/changedetection-mobile/ChangeDetectionMobile";
import Activate from "./auth/Activate";
import { ToastContainer } from 'react-toastify';
import PasswordResetReq from "./auth/PasswordResetReq";
import PasswordReset from "./auth/PasswordReset";
import Dash from "./apps/rrm/Dash";
import RRMMap from "./apps/rrm/RRMMap";
import { createBrowserHistory } from 'history';
const history = createBrowserHistory();

class App extends Component {
  render() {
    return (
      <div>
        <ToastContainer/>
        <Router history={history}>
          <Switch>
            {/* Root */}
            <Route exact path="/" component={Landing}/>
            
            {/* Authentication */}
            <Route path="/accounts/activate" component={Activate}/>
            <Route path="/accounts/password_reset_req" component={PasswordResetReq}/>
            <Route path="/accounts/password_reset" component={PasswordReset}/>

            {/* Account */}

            {/* Change Detection */}
            <Route path="/habitatpatrol" component={ChangeDetection}/>

            {/* Earthenticate */}
            <Route path="/earthenticate" component={ChangeDetectionMobile}/>

            {/* Refined Range Mapping */}
            <Route path="/rrm/dash" component={Dash}/>            
            <Route path="/rrm/map" component={RRMMap}/> 
            {/* Other */}
            <Route path="/style_guide" component={StyleGuide}/> 
            <Route path="/style_max" component={StyleMax}/> 
            <Route path="/style_sasha" component={StyleSasha}/> 

          </Switch>
        </Router>
      </div>
    )
  }
};

export default App;
