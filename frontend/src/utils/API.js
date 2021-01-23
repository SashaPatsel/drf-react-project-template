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
  templateFunction: (args) => axios.get(`/path/to/api`, config)
}