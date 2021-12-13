import * as React from "react";
import { useState } from "react";
import axios from "axios";
import Dialog from "@mui/material/Dialog";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import { DialogContent, DialogActions } from "@mui/material";

export default function NewPortfolioDialog(props) {
  const [title, setTitle] = useState("");

  const createNewPortfolio = async () => {
    let data = JSON.stringify({
      username: props.username,
    });

  fetch(`http://127.0.0.1:8000/api/portfolio/${props.gameTitle}/${title}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: data
  })
  .then((res) => console.log(res.status));
};


  const handleSave = async () => {
    await createNewPortfolio();
    props.setDialogVisible();
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  return (
    <Dialog onClose={handleClose} open={props.open}>
      <DialogTitle>Create New Portfolio</DialogTitle>
      <DialogContent style={{ display: "contents" }}>
        <TextField
          id="outlined-basic"
          label="Title"
          variant="outlined"
          value={title}
          onChange={handleTitleChange}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
}
