import React, { Component } from "react";
import Autosuggest from 'react-autosuggest';

class Autocomplete extends Component {

  state = {
    value: '',
    suggestions: []
  };

  getSuggestions = value => {
    const inputValue = value.trim().toLowerCase();
    const inputLength = inputValue.length;

    return inputLength === 0 ? [] : this.props.data.filter(i =>
      i.toLowerCase().slice(0, inputLength) === inputValue
    );
  };

  getSuggestionValue = suggestion => suggestion;

  renderSuggestion = suggestion => (
    <div >
      {suggestion}
    </div>
  );

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
    if (this.props.onChange) {
      this.props.onChange(event)
    }
  };

  // Autosuggest will call this function every time you need to update suggestions.
  // You already implemented this logic above, so just use it.
  onSuggestionsFetchRequested = ({ value }) => {
    this.setState({
      suggestions: this.getSuggestions(value)
    });
  };

  // Autosuggest will call this function every time you need to clear suggestions.
  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  render() {
    const { value, suggestions } = this.state;

    // Autosuggest will pass through all these props to the input.
    const inputProps = {
      placeholder: this.props.placeholder,
      value,
      onChange: this.onChange,
      id: this.props.htmlID
    };

    return (
      <div style={{ position: "relative" }} className={this.props.otherclasses}>
        <Autosuggest
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          inputProps={inputProps}
        />
        <button type="submit" className="autocomplete__button">
          <i className="fas fa-search autocomplete__icon"></i>
        </button>
      </div>
    );
  }
}

export default Autocomplete