import * as React from 'react';
import { DataGrid }from '@mui/x-data-grid';

export default function GameTable(props) {
    const columns = [
        { field: 'title', headerName: 'Title', width: 150},
        {
          field: 'starting_balance',
          headerName: 'Starting Balance',
          width: 150,
        },
        { field: 'winner', headerName: 'Winner', width: 150},
        { field: 'created_on', headerName: 'Start Date', width: 150},
        { field: 'rules', headerName: 'Rules', width: 300},
    ];

    const processGameData = (data) => {
        let resp = []
        for (let d of data) {
            let r = {}
            r["id"] = d.uid
            r["title"] = d.title
            r["starting_balance"] = d.starting_balance
            r["rules"] = d.rules
            r["portfolios"] = d.portfolios
            resp.push(r)
        }
        return resp
    }

    return (
        <DataGrid
            columns={columns}
            rows={processGameData(props.data)}
        >
        </DataGrid>
    )
}
