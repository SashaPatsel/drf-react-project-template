import React, { useState, useEffect } from "react";
import { Icon } from "../components";

export default function ModalClose(props) {


  return (
    <div className="modal__close" onClick={props.cb}>
      <Icon icon="close" ko={true} size="sm" />
    </div>
  )
}