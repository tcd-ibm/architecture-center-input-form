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

    const [user, setUser] = useContext(AuthContext);

    const [data, setData] = useState([]);
    const [numberOfEntries, setNumberOfEntries] = useState();
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);

    useEffect(() => {
        const requestConfig = { 
            params: {
                page: page,
                per_page: pageSize
            },
            headers: { 
                'Content-Type': 'application/json', 
                'Accept': 'application/json', 
                'Authorization': `Bearer ${user.accessToken}` 
            } 
        };
        axios.get('/admin/users', requestConfig).then(res => {
            setData(res.data);
            setNumberOfEntries(parseInt(res.headers['x-total-count']));
        })
        .catch(err => {
            console.log(err);
        });
    }, [user, page, pageSize]);

    const handlePaginationChange = event => {
        setPage(event.page);
        setPageSize(event.pageSize);
    };

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
                        onChange={handlePaginationChange}
                        page={page}
                        pageSize={pageSize}
                        pageSizes={[10, 15, 25, 50 ]}
                        size='lg'
                        totalItems={numberOfEntries}
                    />
                </TableContainer>
            );
            }}
        </DataTable>
        </>
    );
}

export default ManageUsersPage;