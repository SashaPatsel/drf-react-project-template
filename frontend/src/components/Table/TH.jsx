import React, { useState, useEffect } from "react";

export default function TH(props) {


  return (
    <th className="c-table__h">
      {props.children}
    </th>
  )
}
