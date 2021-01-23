import React, { useState, useCallback } from "react";
import utils from "../utils/utils";
import { useDropzone } from 'react-dropzone';
import List from "./List/List";
import ListItem from "./List/ListItem";
import Button from "./Button";
import staticLink from "../utils/static";
function FileUpload(props) {

  const initState = {
    fileStatus: "No files selected yet...",
    name: false
  }

  const [state, setState] = useState(initState)

  function handleChange(e) {
    setState({
      ...state,
      target: e.target,
      file: e.target.files[0],
      name: e.target.files[0].name,
      value: e.target.value
    })
  }

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      let formData = new FormData()
      formData.append('file', file, file.name);
      setState({ ...state, formData, name: file.name })
    })

  }, [])


  function onSubmit(e) {
    e.preventDefault()
    let formData = new FormData()
    try {
      formData.append('file', state.file, state.name);
      props.uploadCB(formData)
    } catch {
      utils.sendAlert(`Please select a file before uploading.`, "error")
    }
  }

  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="file-upload">
      <div className="u-pad-vert-sm">

        <h4 className="heading__4 heading__4--bold">Upload</h4>
      </div>
      <div className="u-pad-btm-sm">

        <h5 className="heading__5">{props.instructions}</h5>
      </div>
      <div id="fileDrag" {...getRootProps()} >

        <div className="file-upload__drag" onChange={handleChange}>
          <img src={`${staticLink}graphic__browse.svg`} alt="Browse Files" className="navbar__logo" />

          <form className="file-upload__form" encType="multipart/form-data" onSubmit={onSubmit}>
            <input type="file" name="map_layer" id="map_layer" className="form__file" onChange={handleChange} />
            <label htmlFor="map_layer" className="button__primary js-labelFile u-mgn-top-md" id="layerUploadLabel">

              Browse
            </label>
          </form>
          <h5 className="heading__5 u-mgn-top-sm">or drag a file here</h5>

        </div>

      </ div>
      <h5 className="heading__5 u-mgn-top-sm">Selected files:</h5>
      {state.name ?
        <List>
          <ListItem >
            <div className="u-pad-vert-sm">

              <p className="paragraph__1 paragraph__1--ko">
                {state.name}
              </p>
            </div>
          </ListItem>
        </List>
        :
        <div className="u-mgn-btm-sm u-mgn-top-sm">
          <p className="paragraph__2">{state.fileStatus}</p>
        </div>
      }
      <div className="file-upload__submit">
        {props.modalToggle ?
          <div className="u-mgn-right-sm">
            <Button buttonType="secondary" small={true} onClick={props.modalToggle}>Cancel</Button>
          </div>
          : null
        }
        <Button buttonType="primary" small={true} onClick={onSubmit}>Upload</Button>
      </div>
    </div>
  )

}

export default FileUpload