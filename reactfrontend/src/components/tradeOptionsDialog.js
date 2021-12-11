import * as React from "react";
import { useState } from "react";
import axios from "axios";
import Dialog from "@mui/material/Dialog";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import { DialogContent, DialogActions } from "@mui/material";

export default function TradeHoldingsDialog(props) {
  const [contract, setContract] = useState("");
  const [quantity, setQuantity] = useState(0);
  const securityType = "option";

  const trade = async () => {
    let data = {
      portfolioTitle: props.portfolioTitle,
      gameTitle: props.gameTitle,
      securityType: securityType,
      contract: contract,
    };
    if (props.type === "Sell") {
      data.quantity = -parseInt(quantity);
    } else {
      data.quantity = parseInt(quantity);
    }
    data = JSON.stringify(data);
    axios
      .post(`/api/portfolio/trade`, data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res) => console.log(res.status))
      .catch((err) => console.log(err.response.data)); // TODO: Add better error
  };

  const handleTrade = async () => {
    await trade();
    props.setDialogVisible();
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  const handleContractChange = (e) => {
    setContract(e.target.value);
  };

  const handleQuantityChange = (e) => {
    setQuantity(e.target.value);
  };

  return (
    <Dialog onClose={handleClose} open={props.open}>
      <DialogTitle>
        {props.type} Option for Portfolio {props.portfolioTitle} in Game{" "}
        {props.gameTitle}
      </DialogTitle>
      <DialogContent>
        <TextField
          id="outlined-basic"
          label="Contract"
          variant="outlined"
          value={contract}
          onChange={handleContractChange}
        />
        <TextField
          id="outlined-basic"
          label="Quantity"
          variant="outlined"
          value={quantity}
          onChange={handleQuantityChange}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleTrade}>{props.type}</Button>
      </DialogActions>
    </Dialog>
  );
}
