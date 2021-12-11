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

    axios
      .post(`/api/portfolio/${props.gameTitle}/${title}/`, data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res) => console.log(res.status))
      .catch((err) => console.log(err.response.data)); // TODO: Add better error
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
