import * as React from 'react';
import { DataGrid }from '@mui/x-data-grid';

export default function GameTable() {
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

    const rows = [
        {
            'id': "id1", // TODO: this will have to be uid
            'title': 'Test Game',
            'starting_balance': 1234.23,
            'winner': null,
            'created_on': '12-06-2021',
            'rules': 'All is fair in love and war',
        }
    ]

    return (
        <DataGrid
            columns={columns}
            rows={rows}
        >
        </DataGrid>
    )
}
