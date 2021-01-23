import React from 'react';

export default function InputSlider({ ko, isVertical }, props) {
  // WIP COMPONENT

  // className definition for wrapper <div>
  const wrapperClassNameBase = 'input__range__wrapper';
  let wrapperVerticalStyle = isVertical
      ? `${wrapperClassNameBase}--isVertical`
      : `${wrapperClassNameBase}--isHorizontal`,
    wrapperClassName = `${wrapperClassNameBase} ${wrapperVerticalStyle}`;

  console.log(`wrapper className: ${wrapperClassName}`);

  // className definition for <input>
  const inputClassNameBase = 'input__range';
  let inputKoStyle = ko ? '' : '',
    inputVerticalStyle = isVertical
      ? `${inputClassNameBase}--isVertical`
      : `${inputClassNameBase}--isHorizontal`,
    inputClassName = `${inputClassNameBase} ${inputVerticalStyle} ${inputKoStyle}`;

  console.log(`input className: ${inputClassName}`);

  return (
    <div className={wrapperClassName}>
      <input {...props} className={inputClassName} type='range'></input>
    </div>
  );
}

// EXAMPLE SCSS FOR PROTOTYPE OF VERTICAL SLIDER (NEEDS TO UTILIZE PARENT DIV IN COMPONENT)
/* .input {
  &__range {
    &--disabled {
      &--ko {
      }
    }

    &--isVertical {
      transform-origin: 65px 65px;
      transform: rotate(-90deg);
    }

    &__wrapper {
      display: inline-block;

      &--isHorizontal {
        border: 1px solid red;
        max-height: 20px;
        max-width: 132px;
      }
      &--isVertical {
        border: 1px solid blue;
        height: 132px;
        width: 20px;
      }
    }
  }
} */
