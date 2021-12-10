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
  let [gamesData, setGamesData] = useState([]);
  const setVisible = () => {
      setNewGameDialogVisible(!newGameDialogVisible);
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
        await fetchGameData();
      })();
  }, []);
  return (
    <div>
      <Button variant="contained" onClick={setVisible}>Create New Game</Button>
      <GameTable data={gamesData}></GameTable>
      {newGameDialogVisible ? <NewGameDialog open={newGameDialogVisible} setDialogVisible={setVisible}></NewGameDialog>: <></>}
    </div>

  );
}
