import React, { useState, useEffect } from "react";

export default function TD(props) {


  return (
    <td className="c-table__d">
      {props.children}
    </td>
  )
}
