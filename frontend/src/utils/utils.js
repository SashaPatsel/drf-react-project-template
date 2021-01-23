import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default {
  sendAlert: (msg, type) => {
    return toast(msg, {
        position: toast.POSITION.TOP_CENTER,
        className: "alert-toast",
        progressClassName: `alert-toast__${type}`,
        autoClose: false
      });
    
  },
  queryParamsToObj: url => {
    // URL should be `window.location.search.substring(1)`
    return JSON.parse('{"' + decodeURI(url).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}')
  }
}