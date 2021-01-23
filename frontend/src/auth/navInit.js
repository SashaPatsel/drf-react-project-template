import React from "react";
import Navbar from "../components/Navbar";

export default (app, theme) => {
 return ( 
   app.state.isAuthenticated ?
      <Navbar
        navTheme={theme}
        isAuthenticated={true}
        thumbnail={app.state.thumbnail}
        account={app.state.account}
      /> :
      <Navbar
        navTheme={theme}
        isAuthenticated={false}
        thumbnail=""
      />
  )
}