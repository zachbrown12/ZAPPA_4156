import * as React from "react";
import { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import axios from "axios";
import GameTable from "./gameTable";
import NewGameDialog from "./newGameDialog";
import { Navigate } from "react-router-dom";

export default function LandingPage(props) {
  const [newGameDialogVisible, setNewGameDialogVisible] = useState(false);
  let [gamesData, setGamesData] = useState([]);
  const setVisible = () => {
    setNewGameDialogVisible(!newGameDialogVisible);
  };

  const fetchGameData = async () => {
    axios
      .get("/api/games")
      .then((resp) => {
        console.log(resp.data);
        setGamesData(resp.data);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    (async () => {
      await fetchGameData();
    })();
  }, []);
  return (
    <div>
      {props.loggedIn ? (
        <div>
          <Button variant="contained" onClick={setVisible}>
            Create New Game
          </Button>
          <GameTable data={gamesData}></GameTable>
          {newGameDialogVisible ? (
            <NewGameDialog
              open={newGameDialogVisible}
              setDialogVisible={setVisible}
            ></NewGameDialog>
          ) : (
            <></>
          )}
        </div>
      ) : (
        <Navigate to="/login" />
      )}
    </div>
  );
}
