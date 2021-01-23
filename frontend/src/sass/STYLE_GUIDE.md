# Conservationist.io Style Guide

## Sass
Sass is most simply explained as "syntactic sugar" for CSS. In fact, the styling used by Conservationist.io is plain CSS... but compiled by sass 

### Writing Sass
Conservationist.io uses an npm library called node-sass to copile Sass to CSS. All CSS is imported from  /frontend/src/App.css. So in order to see changes written in a .scss file reflected in the app, you need to have the compiling process running in the background. 

To get started, open a new command line prompt, navigate to /frontend and run `yarn sass` or `npm run sass`. This will start a new process that compiles all files referenced in /frontend/src/sass/main.scss to /frontend/App.css anytime one of those files is saved.

To start working in a new Sass file, make sure to import it to /frontend/src/sass/main.scss.

### Embedding
Sass allows you to embed classes to create structure in one's styling. Embedding also allows lets you avoid redundancies. 

Embeded classes are denoted by the `&` symbol

Here's an example of Sass's class embedding:

__In css, we'd have to do the following__
```css

.card__header--red {
  /* Styles the .card__header--red class */
}

.card__header--blue {
  /* Styles the .card__header--blue class */
}
```

__Whereas with Sass, we can embed class within a hierarchy__
```scss
.card {
  // Styles the .card class

  &__header {
    // Styles the .card__header class

    &--red {
      // Styles the .card__header--red class
    }

    &--blue {
      // Styles the .card__header--blue class
    }
  }

}
```

### Variables 
Sass allows you to set variables. The key benefit of this feature is that you can change a variables value, and every invocation of that variable will change accordingly across the app. 

Variables are declared and invoked using the `$` symbol.

The syntax is as follows:
```scss
// Variable declaration
$color-primary: #005596;

// Variable invocation
.some-class {
  background-color: $color-primary;
}

.another-class {
  border: 1px solid $color-primary;
}
```

### Mixins
Mixins address very similar needs to those addressed by variables. Rather than pointing to a single value though, mixins contain "chunks" of css code. 

Mixins are delcared by `@mixin`, and invoked by `@include`.

For example:
```scss
// Declaration
@mixin center-element {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
// Invocation
.some_class {
  color: white;
  border: 2px solid black;
  @include center-element; 
}
```

### Functions
Sass functions work very similarly to functions in programming languages.

```scss
// Declare a function with the @symbol
// Functions can take in arguments just like in other languages
@function pow($base, $exponent) {
  $result: 1;
  @for $_ from 1 through $exponent {
    $result: $result * $base;
  }
  @return $result;
}

.sidebar {
  float: left;
  // The margin will be dynamic based on the values provided in the function call.
  margin-left: pow(4, 3) * 1px;
}

```

## BEM
BEM is a css class-naming convention. Its an acronym that stands for Block, Element, Modifier. 

The convention is as follows: .block__element--modifier. 

Suppose we were designing a card component. In this case, the card will be the main "Block". As you can see below, the card contains three parts, or "Elements" (a heahder, a body, and a footer).

But suppose we have a site where in some cases we want a card header with a red background and in others we want one with a blue background. In such cases, we use "Modifiers". 

The JSX:
```html
<div className="card">
  <div className="card__header card__header--red">
  </div>
  <div className="card__body">
  </div>
  <div className="card__footer">
  </div>
</div>
```
In the example above, we created a card component with a header that has a red background. All cards will have the same dimensions, the same is true for every card's header. However, some cards will have a header with a red background, and others will have a header with a blue background. Depending on which case we need, we can use either of the modifier classes (&--) we rote below.

```scss
.card {
  width: 20rem;
  height: 20rem;

  &__header {
    padding: .5rem;
    width: 100%;
    height: 5rem;

    &--red {
      background-color: red;
    }

    &--blue {
      background-color: blue;
    }
  }
}

```

In the above example, we right styling for a card and its heading. 

## Responsiveness

### Responsive Mixin
Sass syntax makes some parts of responsive design a lot easier. The most comprehensive way to create a responsive design is to adjust an element's styling at each point it's design "breaks". 

However, if styling is done correctly, there will most often be no need to define different styling at different points. 

One more organized approach is to specify different styling for common screen sizes. In the code below, we define a mixin which takes in an argument:

```scss
// Declaration
@mixin responsive($breakpoint) {
    @if $breakpoint == phone {
      //em number calculated by dividing the amount of px by default font size (16px) 
      @media (max-width: 697px) { @content }; //600px 
    }
  
    @if $breakpoint == t-port {
      @media (max-width: 56.25em) { @content }; //900px
    }
  
    @if $breakpoint == t-land {
      @media (max-width: 85em) { @content }; 
    }
  
    @if $breakpoint == l-desk {
      @media (min-width: 112.5em) { @content }; //1800px
    }
}

// Invocation
html {
  @include responsive(l-desk) {
    font-size: 75%; //1rem = 12px 12/16 = 75%
  }

  @include responsive(t-land) { // width < 1200?
    font-size: 56.25%; //1rem = 9px 9/16 = 56.25%
  }

  @include responsive(t-port) { // width < 900?
    font-size: 50%; //1rem = 8px 8/16 = 50%
  }
}

// Invocation
.some-class {
  width: 35rem;

  @include responsive(t-land) {
    width: 30rem;
  }
}

```

Whenever we "include" a mixin in a css block, we pass an argument which corresponds to the screen size we want to style for. Within the include block, we write CSS as if we were styling any element/class, only it will apply strictly to that element at that screen size. 

In the code above, we are essentially calling a "function" named "responsive" and passing an argument for the screen size we want to apply styling for. 

### Normal Responsiveness
Responsiveness in CSS is accomplished through "media queries". Using `@media`, we define the screensize we want to style for.

```scss
.some-class {
  width: 50%;

  @media (max-width: 980px) {
    width: 80%;     
  }
}
```
*Note that media queries should be written in descending order of size. That is the only way to get them to apply sequentially. Otherwise, styling for larger screens will remain even when another media query has been written for the current screen size. 

## File Structure

### /abstracts
#### functions
Contains all functions to be used in the style library.

#### mixins
Contains all mixins to be used in the style library.

#### variables
Contains all variables to be used in the style library.

### /base
#### animations
Contains all animations to be used in the style library.

#### base
Contains all styling that affects all styling. For example, any styling to the body tag, or site-wite responsiveness would go here. 

#### typography
Contains styling for all typography. Includes headings, text, etc... 

#### utilities
Contains utility classes. For example, we might create the following class:
```scss
// small margin top
.mgn-top-sm {
  margin-top: 2rem;
}
```
Now any time we create an element that has a small margin above it, we can simply assign it this class in addition to any other classes. 

### /components
Files found in this folder contain styling for components found across the platform. Generally, each of these files should correspond to a React component.  

### /layout
Contains any layout related styling. Includes grids, maps, etc...

### /pages
Contains styling for individual pages. Each file should correspond to a unique page on the platform. 

### main.scss
The main.scss file is the "organizer" for all Sass code. Its job is to point to all the files that will be compiled to CSS. 

Every time a new file is created it should follow the following format: `_<name>.scss`

When importing a file to main.scssm follow this syntax: `@import "<folder>/<file>";`. Note you do __not__  need to include the `_` prefix in imports. 

