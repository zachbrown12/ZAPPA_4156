import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useState } from "react";
import PortfoliosDialog from "./portfoliosDialog";

export default function GameTable(props) {
  let [portfoliosDialogVisible, setPortfoliosDialogVisible] = useState(false);
  let [selectedRowData, setSelectedRowData] = useState([]);

  const setVisible = () => {
    setPortfoliosDialogVisible(!portfoliosDialogVisible);
  };

  const columns = [
    { field: "title", headerName: "Title", width: 150 },
    {
      field: "starting_balance",
      headerName: "Starting Balance",
      width: 150,
    },
    { field: "winner", headerName: "Winner", width: 150 },
    { field: "created_on", headerName: "Start Date", width: 150 },
    { field: "rules", headerName: "Rules", width: 300 },
  ];

  const processGameData = (data) => {
    let resp = [];
    for (let d of data) {
      let r = {};
      r["id"] = d.uid;
      r["title"] = d.title;
      r["starting_balance"] = d.starting_balance;
      r["rules"] = d.rules;
      r["portfolios"] = d.portfolios;
      resp.push(r);
    }
    return resp;
  };

  const handleOnRowClick = (e) => {
    let data = e.row;
    setSelectedRowData(data);
    setPortfoliosDialogVisible(true);
  };

  return (
    <div style={{ display: "flex", height: "100%" }}>
      <div style={{ flexGrow: 1 }}>
        <DataGrid
          columns={columns}
          rows={processGameData(props.data)}
          onRowDoubleClick={handleOnRowClick}
        ></DataGrid>
        {portfoliosDialogVisible ? (
          <PortfoliosDialog
            open={portfoliosDialogVisible}
            setDialogVisible={setVisible}
            portfolios={selectedRowData.portfolios}
            gameTitle={selectedRowData.title}
          ></PortfoliosDialog>
        ) : (
          <></>
        )}
      </div>
    </div>
  );
}
