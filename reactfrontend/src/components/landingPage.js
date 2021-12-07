import * as React from 'react';
import { useState } from 'react';
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
  const [gameName, setGameName] = useState("Dummy Game Name");
  // eslint-disable-next-line
  const [gameRules, setGameRules] = useState(null);
  // eslint-disable-next-line
  const [gameStartingBalance, setGameStartingBalance] = useState(null);
  // eslint-disable-next-line
  const [gamesData, setGamesData] = useState([]);
  const setVisible = () => {
      setNewGameDialogVisible(true);
  }

  // eslint-disable-next-line
  const createNewGame = () => {
    axios
        .post(`/api/game/${gameName}`)
        .then((res) => console.log(res.data))
        .catch((err) => console.log(err)); // TODO: Add better error
  }

  const handleDialogClose = (name, rules, balance) => {
      setGameName(name);
      setGameRules(rules);
      setGameStartingBalance(balance);
  }

  // eslint-disable-next-line
  const fetchGameData = () => {
      axios
        .get('/api/games')
        .then((res) => setGamesData(res.data))
        .catch((err) => console.log(err));
  }
  return (
    <div>
      <Button variant="contained" onClick={setVisible}>Create New Game</Button>
      <GameTable></GameTable>
      {newGameDialogVisible ? <NewGameDialog open={newGameDialogVisible} onCloseDialog={handleDialogClose}></NewGameDialog>: <></>}
    </div>

  );
}
