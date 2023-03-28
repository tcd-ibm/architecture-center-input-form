import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router';
import { DataTable, TableContainer, TableToolbar, TableBatchActions, TableBatchAction, 
    TableToolbarContent, TableToolbarSearch, TableToolbarMenu, TableToolbarAction, Table, TableHead, 
    TableHeader, TableRow, TableSelectAll, TableBody, TableSelectRow, TableCell, Pagination, Button } from '@carbon/react';
import { TrashCan, UserRole } from '@carbon/icons-react';

import styles from './ManageUsersPage.module.scss';

import ModalBulkUserDeletion from '@/Components/ModalBulkUserDeletion';

import useAuth from '@/hooks/useAuth';

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
        },
        {
            header: 'Actions',
            key: 'actionsChangeRole'
        },
        {
            header: 'Actions',
            key: 'actionsDelete'
        },
    ];

    const navigate = useNavigate();

    const deletionModalRef = useRef();

    const { user } = useAuth();

    const [data, setData] = useState([]);
    const [numberOfEntries, setNumberOfEntries] = useState();
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);

    useEffect(() => {
        if(!user) {
            navigate('/login', { replace: true });
            return;
        }
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
            const data = res.data.map(user => ({ 
                ...user, 
                signupDate: new Date(user.created_at).toISOString().substring(0, 10),
                actionsChangeRole: <Button kind='ghost' renderIcon={UserRole}>Change role</Button>,
                actionsDelete: <Button kind='danger--ghost' renderIcon={TrashCan}>Delete</Button>
            }));
            setData(data);
            setNumberOfEntries(parseInt(res.headers['x-total-count']));
        })
        .catch(err => {
            console.log(err);
        });
    }, [navigate, user, page, pageSize]);

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
                                onClick={() => {
                                    deletionModalRef.current.open(selectedRows.map(row => row.id));
                                }}
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
                        </TableToolbarContent>
                    </TableToolbar>
                    
                    <Table {...getTableProps()}>
                        <TableHead>
                        <TableRow>
                            <TableSelectAll {...getSelectionProps()} />
                            {headers.map((header, i) => (
                                header.key === 'actionsChangeRole' ?
                                    <TableHeader key={i} {...getHeaderProps({ header })} colspan={2} className={styles.actionsHeaderCell}>
                                        {header.header}
                                    </TableHeader> :
                                header.key !== 'actionsDelete' &&
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
                                (cell.info.header === 'actionsChangeRole' || cell.info.header === 'actionsDelete') ?
                                <TableCell key={cell.id} className={styles.actionsCell}>{cell.value}</TableCell> :
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
        <ModalBulkUserDeletion users={data} onConfirm={selectedIds => console.log(selectedIds)} ref={deletionModalRef} />
        </>
    );
}

export default ManageUsersPage;