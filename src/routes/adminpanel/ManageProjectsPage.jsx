//import { Heading } from '@carbon/react';
import { DataTable, TableContainer, TableToolbar, TableBatchActions, TableBatchAction, 
    TableToolbarContent, TableToolbarSearch, TableToolbarMenu, TableToolbarAction, Table, TableHead, 
    TableHeader, TableRow, TableSelectAll, TableBody, TableSelectRow, TableCell, Pagination } from '@carbon/react';
import { TrashCan, UserRole } from '@carbon/icons-react';

function ManageProjectsPage() {
    const headers = [
        {
            header: 'Project',
            key: 'project'
        },
        {
            header: 'Sponsor',
            key: 'sponsor'
        },
        {
            header: 'Date Created',
            key: 'dateCreated'
        },
        {
            header: 'Technology',
            key: 'technology'
        }
    ];

    const rows = [
        {
            id: '1',
            project: 'SCADA Interface Modernisation',
            sponsor: 'Kingspan',
            dateCreated: '2023-01-01',
            technology: 'Redhat Enterprise Linux'
        },
        {
            id: '2',
            project: 'Radio Access Networks',
            sponsor: 'Telco',
            dateCreated: '2023-02-12',
            technology: 'Orchestrator and Cloud Platform'
        },
        {
            id: '3',
            project: 'API Management Platform',
            sponsor: 'SAP',
            dateCreated: '2023-02-15',
            technology: 'Red Hat Integration'
        },
        {
            id: '4',
            project: 'Intelligent Automation Workflow',
            sponsor: 'Axa',
            dateCreated: '2023-02-23',
            technology: 'Red Hat Ansible Automation Platform'
        },
        {
            id: '5',
            project: 'Red Hat OpenShift Service',
            sponsor: 'Amazon',
            dateCreated: '2023-02-28',
            technology: 'Amazon Web Services Cloud'
        },
        {
            id: '6',
            project: 'Enabling Medical Imaging Diagnostics',
            sponsor: 'Edge',
            dateCreated: '2023-03-01',
            technology: 'Red Hat OpenShift GitOps'
        },
    ];

    return (
        <>
        <DataTable headers={headers} rows={rows} >
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
                title='Projects'
                description='List of all current projects'
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

export default ManageProjectsPage;