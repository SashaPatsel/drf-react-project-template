import React, { useState, useEffect } from "react";

export default function TableRow(props) {


  return (
    <tr className="c-table__row">
      {props.children}
    </tr>
  )
}
