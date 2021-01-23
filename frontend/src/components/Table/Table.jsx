import React, { useState, useEffect } from "react";

export default function Table(props) {


  return (
    <table className="c-table">
      {props.children}
    </table>
  )
}
