import * as React from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import { DialogContent, DialogActions } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import Button from "@mui/material/Button";

export default function HoldingsDialog(props) {
  const columns = [
    { field: "portfolio", headerName: "Portfolio", width: 400 },
    { field: "ticker", headerName: "Ticker", width: 100 },
    { field: "shares", headerName: "Shares", width: 100 },
  ];

  const processHoldingsData = (data) => {
    let resp = [];
    for (let d of data) {
      let r = {};
      r["id"] = d.uid;
      r["portfolio"] = d.portfolio.title;
      r["ticker"] = d.ticker;
      r["shares"] = d.shares;
      resp.push(r);
    }
    return resp;
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  return (
    <Dialog
      onClose={handleClose}
      open={props.open}
      maxWidth={"lg"}
      fullWidth={true}
      fullScreen={true}
    >
      <DialogTitle> Holdings for Portfolio {props.portfolioTitle}</DialogTitle>
      <DialogContent>
        <DataGrid
          columns={columns}
          rows={processHoldingsData(props.holdings)}
        ></DataGrid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
