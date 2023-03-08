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
            header: 'Date Added',
            key: 'dateAdded'
        },
        {
            header: 'Technologies',
            key: 'technologies'
        }
    ];

    const rows = [
        {
            id: '1',
            project: 'SCADA Interface Modernisation',
            sponsor: 'Kingspan',
            dateAdded: '2023-01-01',
            technologies: 'ACM, AMQ, Ansible, API, OpenShift'
        },
        {
            id: '2',
            project: 'Radio Access Networks',
            sponsor: 'Telco',
            dateAdded: '2023-02-12',
            technologies: 'ACM, AMQ, OpenShift, Quay, RHEL'
        },
        {
            id: '3',
            project: 'API Management Platform',
            sponsor: 'SAP',
            dateAdded: '2023-02-15',
            technologies: 'RHEL, OpenShift'
        },
        {
            id: '4',
            project: 'Intelligent Automation Workflow',
            sponsor: 'Axa',
            dateAdded: '2023-02-23',
            technologies: 'OpenShift, Ansible'
        },
        {
            id: '5',
            project: 'Red Hat OpenShift Service',
            sponsor: 'Amazon',
            dateAdded: '2023-02-28',
            technologies: 'ROSA, OpenShift'
        },
        {
            id: '6',
            project: 'Enabling Medical Imaging Diagnostics',
            sponsor: 'Edge',
            dateAdded: '2023-03-02',
            technologies: 'OpenShift, AMQ, ACM, RHEL'
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