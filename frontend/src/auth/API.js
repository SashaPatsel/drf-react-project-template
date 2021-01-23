import axios from "axios";

let config;
if (localStorage.getItem('token')) {
  config = {
    headers: {
      Authorization: `JWT ${localStorage.getItem('token')}`
    }
  }
} else {
  config = {}
}


export default {
  activate: function(data) {
    return axios.post("/api/accounts/activate", data)
  },
  emailReset: function(data) {
    return axios.post("/api/accounts/request_pass_reset", data)
  },
  checkResetToken: function(token) {
    return axios.get(`/api/accounts/pass_reset?token=${token}`)
  },
  getAccount: function() {
    
    return axios.get("/api/accounts/useraccount", config)
  },
  google: function(data) {
    // data = {
    //   client_id: 
    // }
  //   https://oauth2provider.com/auth?
  //  response_type=token&
  //  client_id=CLIENT_KEY&
  //  redirect_uri=CALLBACK_URI&
  //  scope=profile&
  //  scope=email
  // https://github.com/RealmTeam/django-rest-framework-social-oauth2
    return axios.post("/auth?response_type=token&client_id=224036121952-dc4om7dnkff6hca6gfnskfaphcgt0870.apps.googleusercontent.com&redirect_uri=localhost:3000")
  },
  logIn: function(data) {
    console.log("logIn", data)
    return axios.post("/token-auth/", data)
  },
  register: function(data) {
    return axios.post("/api/accounts/register", data)
  },
  resetPassword: function(data) {
    return axios.post("/api/accounts/pass_reset", data)
  }
}