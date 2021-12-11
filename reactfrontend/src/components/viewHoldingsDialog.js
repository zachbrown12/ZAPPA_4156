import * as React from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import { DialogContent, DialogActions } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import Button from "@mui/material/Button";
import { useState } from "react";
import TradeHoldingsDialog from "./tradeHoldingsDialog";
import TradeOptionsDialog from "./tradeOptionsDialog";

export default function ViewHoldingsDialog(props) {
  const [buyHoldingDialogVisible, setBuyHoldingDialogVisible] = useState(false);
  const [sellHoldingDialogVisible, setSellHoldingDialogVisible] =
    useState(false);
  const [buyOptionDialogVisible, setBuyOptionDialogVisible] = useState(false);
  const [sellOptionDialogVisible, setSellOptionDialogVisible] = useState(false);
  const columns = [
    { field: "type", headerName: "Type", width: 100 },
    { field: "ticker", headerName: "Ticker", width: 100 },
    { field: "shares", headerName: "Shares", width: 100 },
    { field: "contract", headerName: "Contract", width: 150 },
    { field: "quantity", headerName: "Quantity", width: 100 },
  ];

  const processHoldingsData = (holdings, options) => {
    let resp = [];
    for (let d of holdings) {
      let r = {};
      r["id"] = d.uid;
      r["type"] = "Stock";
      r["ticker"] = d.ticker;
      r["shares"] = d.shares;
      r["contract"] = "N/A";
      r["quantity"] = "N/A";
      resp.push(r);
    }
    for (let d of options) {
      let r = {};
      r["id"] = d.uid;
      r["type"] = "Option";
      r["ticker"] = "N/A";
      r["shares"] = "N/A";
      r["contract"] = d.contract;
      r["quantity"] = d.quantity;
      resp.push(r);
    }
    return resp;
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  const setBuyHoldingVisible = () => {
    setBuyHoldingDialogVisible(!buyHoldingDialogVisible);
  };

  const setSellHoldingVisible = () => {
    setSellHoldingDialogVisible(!sellHoldingDialogVisible);
  };

  const setBuyOptionVisible = () => {
    setBuyOptionDialogVisible(!buyOptionDialogVisible);
  };

  const setSellOptionVisible = () => {
    setSellOptionDialogVisible(!sellOptionDialogVisible);
  };

  return (
    <div>
      <Dialog
        onClose={handleClose}
        open={props.open}
        maxWidth={"lg"}
        fullWidth={true}
        fullScreen={true}
      >
        <DialogTitle>Holdings for Portfolio {props.portfolioTitle}</DialogTitle>
        <DialogContent>
          <DataGrid
            columns={columns}
            rows={processHoldingsData(props.holdings, props.options)}
          ></DataGrid>
        </DialogContent>
        <DialogActions>
          <Button variant="contained" onClick={setBuyHoldingVisible}>
            Buy Holding
          </Button>
          <Button variant="contained" onClick={setSellHoldingVisible}>
            Sell Holding
          </Button>
          <Button variant="contained" onClick={setBuyOptionVisible}>
            Buy Option
          </Button>
          <Button variant="contained" onClick={setSellOptionVisible}>
            Sell Option
          </Button>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
      {buyHoldingDialogVisible ? (
        <TradeHoldingsDialog
          open={buyHoldingDialogVisible}
          setDialogVisible={setBuyHoldingVisible}
          type={"Buy"}
          gameTitle={props.gameTitle}
          portfolioTitle={props.portfolioTitle}
        ></TradeHoldingsDialog>
      ) : (
        <></>
      )}
      {sellHoldingDialogVisible ? (
        <TradeHoldingsDialog
          open={sellHoldingDialogVisible}
          setDialogVisible={setSellHoldingVisible}
          type={"Sell"}
          gameTitle={props.gameTitle}
          portfolioTitle={props.portfolioTitle}
        ></TradeHoldingsDialog>
      ) : (
        <></>
      )}
      {buyOptionDialogVisible ? (
        <TradeOptionsDialog
          open={buyOptionDialogVisible}
          setDialogVisible={setBuyOptionVisible}
          type={"Buy"}
          gameTitle={props.gameTitle}
          portfolioTitle={props.portfolioTitle}
        ></TradeOptionsDialog>
      ) : (
        <></>
      )}
      {sellOptionDialogVisible ? (
        <TradeOptionsDialog
          open={sellOptionDialogVisible}
          setDialogVisible={setSellOptionVisible}
          type={"Sell"}
          gameTitle={props.gameTitle}
          portfolioTitle={props.portfolioTitle}
        ></TradeOptionsDialog>
      ) : (
        <></>
      )}
    </div>
  );
}
