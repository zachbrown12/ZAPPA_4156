import * as React from 'react';
import { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import axios from "axios";
import GameTable from './gameTable';
import NewGameDialog from './newGameDialog';

export default function LandingPage() {
    // TODO: Create newGameDialog component
  // Allows a user to specify the name of a game
  // eslint-disable-next-line
  const [newGameDialogVisible, setNewGameDialogVisible] = useState(false);
  // eslint-disable-next-line
  const [gameName, setGameName] = useState("DummyGameName");
  // eslint-disable-next-line
  const [gameRules, setGameRules] = useState(null);
  // eslint-disable-next-line
  const [gameStartingBalance, setGameStartingBalance] = useState(null);
  // eslint-disable-next-line
  let [gamesData, setGamesData] = useState([]);
  const setVisible = () => {
      setNewGameDialogVisible(true);
  }

  // eslint-disable-next-line
  const createNewGame = async () => {
    let data = {
        rules: "Test",
        startingBalance: "All's fair in love and war"
    }
    axios
        .post(`/api/game/${gameName}`, data)
        .then((res) => console.log(res.data))
        .catch((err) => console.log(err)); // TODO: Add better error
  }

  const handleDialogClose = (name, rules, balance) => {
      setGameName(name);
      setGameRules(rules);
      setGameStartingBalance(balance);
  }

  // eslint-disable-next-line
  const fetchGameData = async () => {
    axios
    .get('/api/games')
    .then((resp) => {
        console.log(resp.data)
        setGamesData(resp.data);
    }).catch((err) => console.log(err));
  }

  useEffect(() => {
      (async () => {
        await createNewGame();
        await fetchGameData();
      })();
  }, []);
  return (
    <div>
      <Button variant="contained" onClick={setVisible}>Create New Game</Button>
      <GameTable data={gamesData}></GameTable>
      {newGameDialogVisible ? <NewGameDialog open={newGameDialogVisible} onCloseDialog={handleDialogClose}></NewGameDialog>: <></>}
    </div>

  );
}
