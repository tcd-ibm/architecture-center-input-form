import { useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { DataTable, TableContainer, TableToolbar, TableBatchActions, TableBatchAction, 
    TableToolbarContent, TableToolbarSearch, TableToolbarMenu, TableToolbarAction, Table, TableHead, 
    TableHeader, TableRow, TableSelectAll, TableBody, TableSelectRow, TableCell, Pagination } from '@carbon/react';
import { TrashCan, UserRole } from '@carbon/icons-react';

import AuthContext from '@/context/AuthContext';

function ManageUsersPage() {
    const headers = [
        {
            header: 'Email',
            key: 'email'
        },
        {
            header: 'Username',
            key: 'username'
        },
        {
            header: 'Signup date',
            key: 'signupDate'
        },
        {
            header: 'Role',
            key: 'role'
        }
    ];

    // const rows = [
    //     {
    //         id: '1',
    //         email: 'admin@admin.com',
    //         username: 'admin',
    //         signupDate: '2023-01-01',
    //         role: 'Admin'
    //     },
    //     {
    //         id: '2',
    //         email: 'abc@abc.com',
    //         username: 'abc',
    //         signupDate: '2023-02-02',
    //         role: 'Moderator'
    //     },
    //     {
    //         id: '3',
    //         email: 'abcd@abcd.com',
    //         username: 'abcd',
    //         signupDate: '2023-02-10',
    //         role: 'User'
    //     },
    //     {
    //         id: '4',
    //         email: 'example@example.com',
    //         username: 'example',
    //         signupDate: '2023-02-11',
    //         role: 'User'
    //     },
    //     {
    //         id: '5',
    //         email: 'qwerty@qwerty.com',
    //         username: 'qwerty',
    //         signupDate: '2023-02-22',
    //         role: 'User'
    //     },
    //     {
    //         id: '6',
    //         email: 'zxcvb@zxcvb.com',
    //         username: 'zxcvb',
    //         signupDate: '2023-02-25',
    //         role: 'User'
    //     },
    // ];

    const [user, setUser] = useContext(AuthContext);

    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/admin/users', { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } }).then(res => {
            console.log(res.data);
            setData(res.data);
        })
        .catch(err => {
            console.log(err);
        });
    }, [user]);

    return (
        <>
        <DataTable headers={headers} rows={data} >
            {({
                rows,
                headers,
                getHeaderProps,
                getRowProps,
                getSelectionProps,
                getToolbarProps,
                getBatchActionProps,
                onInputChange,
                selectedRows,
                getTableProps,
                getTableContainerProps,
            }) => {
            const batchActionProps = getBatchActionProps();

            return (
                <TableContainer
                title='Users'
                description='List of all currently registered users'
                {...getTableContainerProps()}>

                    <TableToolbar {...getToolbarProps()}>
                        <TableBatchActions {...batchActionProps}>
                            <TableBatchAction
                                tabIndex={batchActionProps.shouldShowBatchActions ? 0 : -1}
                                renderIcon={TrashCan}
                                >
                                Delete
                            </TableBatchAction>
                            <TableBatchAction
                                tabIndex={batchActionProps.shouldShowBatchActions ? 0 : -1}
                                renderIcon={UserRole}
                                >
                                Change user role
                            </TableBatchAction>
                        </TableBatchActions>
                        <TableToolbarContent aria-hidden={batchActionProps.shouldShowBatchActions}>
                            <TableToolbarSearch
                                tabIndex={batchActionProps.shouldShowBatchActions ? -1 : 0}
                                onChange={onInputChange}
                                persistent
                            />
                            <TableToolbarMenu
                                tabIndex={batchActionProps.shouldShowBatchActions ? -1 : 0}>
                                <TableToolbarAction onClick={() => alert('Alert 1')}>
                                Action 1
                                </TableToolbarAction>
                                <TableToolbarAction onClick={() => alert('Alert 2')}>
                                Action 2
                                </TableToolbarAction>
                                <TableToolbarAction onClick={() => alert('Alert 3')}>
                                Action 3
                                </TableToolbarAction>
                            </TableToolbarMenu>
                        </TableToolbarContent>
                    </TableToolbar>
                    
                    <Table {...getTableProps()}>
                        <TableHead>
                        <TableRow>
                            <TableSelectAll {...getSelectionProps()} />
                            {headers.map((header, i) => (
                            <TableHeader key={i} {...getHeaderProps({ header })}>
                                {header.header}
                            </TableHeader>
                            ))}
                        </TableRow>
                        </TableHead>
                        <TableBody>
                        {rows.map((row, i) => (
                            <TableRow key={i} {...getRowProps({ row })}>
                            <TableSelectRow {...getSelectionProps({ row })} />
                            {row.cells.map((cell) => (
                                <TableCell key={cell.id}>{cell.value}</TableCell>
                            ))}
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                    <Pagination 
                        backwardText='Previous page'
                        forwardText='Next page'
                        itemsPerPageText='Items per page:'
                        onChange={function noRefCheck(){}}
                        page={1}
                        pageSize={10}
                        pageSizes={[
                          10,
                          15,
                          25,
                          50
                        ]}
                        size='lg'
                        totalItems={103}
                    />
                </TableContainer>
            );
            }}
        </DataTable>
        </>
    );
}

export default ManageUsersPage;