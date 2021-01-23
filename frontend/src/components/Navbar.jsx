import React, { Component } from "react";
import { toast } from 'react-toastify';
import staticLink from "../utils/static";
import { Icon, InlineDropdown, Menu } from "../components";
import { useState } from "react";

const useSprites = `<use xlink:href="${staticLink}sprite.svg#icon-grid1" xmlns="${staticLink}sprite.svg#icon-grid1" xmlns:svg="${staticLink}sprite.svg#icon-grid1" xmlns:xlink="${staticLink}sprite.svg#icon-grid1"></use>`


toast.configure({
  autoClose: 180
})

const Navbar = props => {
  const initState = {
  }

  const [state, setState] = useState(initState)

  return (
    <div className="nav">
      <div className="nav__brand">
        <h2 className="heading__2 heading__2--ko u-mgn-right-sm">Conservationist.io</h2>
        <h4 className="heading__4 heading__4--ko">Beta</h4>
      </div>

      <div className="nav__options">
        <InlineDropdown
  
          title={
            <p className="paragraph__1 paragraph__1--ko u-flex">
              <span className="u-mgn-right-sm">
                Products
                </span>
              <Icon icon="caret-down" size="sm" ko={true} />
            </p>

          }
        >
          <Menu
            dark={true}
            options={[
              {
                name: "Collaborative Mapper",
                link: "rrm/dash"
              },
              {
                name: "Habitat Patrol",
                link: "/habitatpatrol"
              },
              {
                name: "Earthenticate",
                link: "/earthenticate"
              }
            ]}
          />

        </InlineDropdown>
      </div>

      <div className="nav__config">
        {props.config}
      </div>
    </div>
  )
}


export default Navbar
