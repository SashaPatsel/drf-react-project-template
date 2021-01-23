import React from "react";
import Range from 'rc-slider';
import 'rc-slider/assets/index.css';

const Slider = props => (
  <div className="rc-slider__group">
    <div className="rc-slider__label">
      <Range
        min={props.min}
        max={props.max}
        defaultValue={props.defaultValue}
        onChange={props.onChange}
        onBeforeChange={props.onBeforeChange}
      />
      <div className="rc-slider__val">{props.val}</div>
    </div>
  </div>
)

export default Slider