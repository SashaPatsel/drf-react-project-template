import React, { useState, useEffect } from "react";

export default function TableHead(props) {


  return (
    <thead className="c-table__head">
      {props.children}
    </thead>
  )
}
