import * as React from "react";
import { useState } from "react";
import Dialog from "@mui/material/Dialog";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import { DialogContent, DialogActions } from "@mui/material";

export default function NewGameDialog(props) {
  const [name, setName] = useState("");
  const [startingBalance, setStartingBalance] = useState("");
  const [rules, setRules] = useState("");

  const createNewGame = async () => {
    let data = JSON.stringify({
      startingBalance: startingBalance,
      rules: rules,
    });

    fetch(`http://127.0.0.1:8000/api/game/${name}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: data
      })
      .then((res) => console.log(res.status));
  };
    

  const handleSave = async () => {
    await createNewGame();
    props.setDialogVisible();
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleStartingBalanceChange = (e) => {
    setStartingBalance(e.target.value);
  };

  const handleRulesChange = (e) => {
    setRules(e.target.value);
  };

  return (
    <Dialog onClose={handleClose} open={props.open}>
      <DialogTitle>Create New Game</DialogTitle>
      <DialogContent style={{ display: "contents" }}>
        <TextField
          id="outlined-basic"
          label="Name"
          variant="outlined"
          value={name}
          onChange={handleNameChange}
        />
        <TextField
          id="outlined-basic"
          label="Starting Balance"
          variant="outlined"
          value={startingBalance}
          onChange={handleStartingBalanceChange}
        />
        <TextField
          id="outlined-basic"
          label="Rules"
          variant="outlined"
          value={rules}
          onChange={handleRulesChange}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
}
