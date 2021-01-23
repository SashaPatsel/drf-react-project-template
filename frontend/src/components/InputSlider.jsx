import React from 'react';

export default function InputSlider({ ko, props }) {
  const baseStyle = 'input__slider';
  let koStyle = ko ? `${baseStyle}--ko` : '',
    disabledStyle = props.disabled && !ko ? `${baseStyle}--disabled` : '',
    disabledKoStyle = ko && props.disabled ? `${baseStyle}--ko--disabled` : '',
    className = `${baseStyle} ${koStyle} ${disabledStyle} ${disabledKoStyle}`;

  // console.log(`props:`, props);
  // console.log(`input className: ${className}`);

  return <input {...props} className={className} type='range'></input>;
}
