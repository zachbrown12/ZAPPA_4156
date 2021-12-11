import * as React from "react";
import { useState } from "react";
import axios from "axios";
import Dialog from "@mui/material/Dialog";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import { DialogContent, DialogActions, Checkbox } from "@mui/material";

export default function TradeDialog(props) {
  const [ticker, setTicker] = useState("");
  const [shares, setShares] = useState(0);
  const [exercise, setExcercise] = useState(false);
  const securityType = props.securityType;

  const trade = async () => {
    let data = {};
    if (securityType === "stock") {
      data = {
        portfolioTitle: props.portfolioTitle,
        gameTitle: props.gameTitle,
        securityType: securityType,
        ticker: ticker,
        exercise: exercise,
      };
      if (props.type === "Sell") {
        data.shares = -parseInt(shares);
      } else {
        data.shares = parseInt(shares);
      }
    } else {
      data = {
        portfolioTitle: props.portfolioTitle,
        gameTitle: props.gameTitle,
        securityType: securityType,
        contract: ticker,
      };
      if (props.type === "Sell") {
        data.quantity = -parseInt(shares);
      } else {
        data.quantity = parseInt(shares);
      }
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

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  const handleSharesChange = (e) => {
    setShares(e.target.value);
  };

  const handleExerciseChange = (e) => {
    setExcercise(e.target.checked);
  };

  return (
    <Dialog onClose={handleClose} open={props.open}>
      <DialogTitle>
        {props.type} Stock for Portfolio {props.portfolioTitle} in Game{" "}
        {props.gameTitle}
      </DialogTitle>
      <DialogContent>
        <TextField
          id="outlined-basic"
          label={props.tickLabel}
          variant="outlined"
          value={ticker}
          onChange={handleTickerChange}
        />
        <TextField
          id="outlined-basic"
          label={props.sharesLabel}
          variant="outlined"
          value={shares}
          onChange={handleSharesChange}
        />
        {securityType === "Stock" ? (
          <Checkbox
            checked={exercise}
            onChange={handleExerciseChange}
            label="Exercise"
          />
        ) : (
          <></>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleTrade}>{props.type}</Button>
      </DialogActions>
    </Dialog>
  );
}
