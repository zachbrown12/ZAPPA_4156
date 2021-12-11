import * as React from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import { DialogContent, DialogActions } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import Button from "@mui/material/Button";
import ViewHoldingsDialog from "./viewHoldingsDialog";
import { useState } from "react";
import axios from "axios";
import NewPortfolioDialog from "./newPortfolioDialog";

export default function PortfoliosDialog(props) {
  let [holdingsDialogVisible, setHoldingsDialogVisible] = useState(false);
  let [selectedRowData, setSelectedRowData] = useState({
    holdings: [],
    options: [],
  });
  let [selectedPortfolioTitle, setSelectedPortfolioTitle] = useState("");
  let [createNewPortfolioVisible, setCreateNewPortfolioVisible] =
    useState(false);

  const columns = [
    { field: "game_rank", headerName: "Ranking", width: 100 },
    { field: "title", headerName: "Portfolio Title", width: 400 },
    { field: "owner", headerName: "Owner", width: 300 },
    { field: "total_value", headerName: "Total Value", width: 200 },
    { field: "cash_balance", headerName: "Cash Balance", width: 200 },
  ];

  const processPortfolioData = (data) => {
    let resp = [];
    for (let d of data) {
      let r = {};
      r["id"] = d.uid;
      r["game_rank"] = d.game_rank;
      r["title"] = d.title;
      r["owner"] = d.owner.username;
      r["total_value"] = d.total_value;
      r["cash_balance"] = d.cash_balance;
      resp.push(r);
    }
    return resp;
  };

  const handleClose = () => {
    props.setDialogVisible();
  };

  const getPortfolio = async (portfolioName) => {
    axios
      .get(`/api/portfolio/${props.gameTitle}/${portfolioName}`)
      .then((res) => {
        console.log(res.data);
        setSelectedRowData(res.data);
      })
      .catch((err) => console.log(err.response.data));
  };

  const handleOnRowClick = async (e) => {
    await getPortfolio(e.row.title);
    setSelectedPortfolioTitle(e.row.title);
    setHoldingsDialogVisible(true);
  };

  const createNewPortfolio = () => {
    setCreateNewPortfolioVisible(true);
  };

  const changeCreateNewPortfolioVisible = () => {
    setCreateNewPortfolioVisible(!createNewPortfolioVisible);
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
        <DialogTitle> Portfolios for Game {props.gameTitle}</DialogTitle>
        <DialogContent>
          <DataGrid
            columns={columns}
            rows={processPortfolioData(props.portfolios)}
            onRowDoubleClick={handleOnRowClick}
          ></DataGrid>
        </DialogContent>
        <DialogActions>
          <Button onClick={createNewPortfolio}>Create New Portfolio</Button>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
      {holdingsDialogVisible ? (
        <ViewHoldingsDialog
          open={holdingsDialogVisible}
          setDialogVisible={setHoldingsDialogVisible}
          holdings={selectedRowData.holdings}
          options={selectedRowData.options}
          portfolioTitle={selectedPortfolioTitle}
          gameTitle={props.gameTitle}
        ></ViewHoldingsDialog>
      ) : (
        <></>
      )}
      {createNewPortfolioVisible ? (
        <NewPortfolioDialog
          open={createNewPortfolioVisible}
          username={props.username}
          setDialogVisible={changeCreateNewPortfolioVisible}
          gameTitle={props.gameTitle}
        ></NewPortfolioDialog>
      ) : (
        <></>
      )}
    </div>
  );
}
