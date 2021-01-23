import Auth from "./API";

export default async (app) => {
  await Auth.getAccount()
    .then(res => {
      let isAuthenticated = true
      if (res.data.anonymous) {
        isAuthenticated = false
      }
        app.setState({
          isAuthenticated,
          thumbnail: res.data.photo,
          account: res.data
        })
    })
    .catch(err => {
      console.log("ERROR", err)
    })
}
