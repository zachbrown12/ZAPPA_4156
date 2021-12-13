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
    console.log("Fetching game data");
    axios
      .get("/api/games/")
      .then((resp) => {
        console.log(resp.data);
        setGamesData(resp.data);
        fetchGameData()
      })
      .catch((err) => console.log(err.response.data));

  };

  const logOutUser = () => {
    props.setUsername("");
    props.setLoggedIn(false);
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
          <h1 style={{ margin: "20px" }}>Zappa Trade Simulation</h1>
          <div style={{ margin: "20px", height: "50px" }}>
            <Button variant="contained" onClick={setVisible}>
              Create New Game
            </Button>
            <Button variant="contained" onClick={logOutUser}>
              Logout User {props.username}
            </Button>
          </div>
          <GameTable data={gamesData} username={props.username}></GameTable>
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
