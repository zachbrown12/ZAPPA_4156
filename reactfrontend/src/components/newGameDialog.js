import * as React from 'react';
import { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';

export default function NewGameDialog(open, onCloseDialog) {
     // eslint-disable-next-line
    const [name, setName] = useState('');
     // eslint-disable-next-line
    const [startingBalance, setStartingBalance] = useState(null);
    // eslint-disable-next-line
    const [rules, setRules] = useState('');

    const handleClose = (name, startingBalance, rules) => {
        onCloseDialog(name, startingBalance, rules);
    }


    return(
        <Dialog onClose={handleClose} open={open}>
            <DialogTitle>Create New Game</DialogTitle>
            <TextField id="outlined-basic" label="Name" variant="outlined"/>
            <TextField id="outlined-basic" label="Starting Balance" variant="outlined"/>
            <TextField id="outlined-basic" label="Rules" variant="outlined"/>
        </Dialog>
    )
}
