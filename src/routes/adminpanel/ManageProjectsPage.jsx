//import { Heading } from '@carbon/react';
import { DataTable, TableContainer, TableToolbar, TableBatchActions, TableBatchAction, 
    TableToolbarContent, TableToolbarSearch, TableToolbarMenu, TableToolbarAction, Table, TableHead, 
    TableHeader, TableRow, TableSelectAll, TableBody, TableSelectRow, TableCell, Pagination, Modal } from '@carbon/react';
import { TrashCan, Edit } from '@carbon/icons-react';
import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

import { useNavigate } from 'react-router';
import useAuth from '@/hooks/useAuth';

function ManageProjectsPage() {

    const [projects, setProjects] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);
    const [numberOfEntries, setNumberOfEntries] = useState();
    const navigate = useNavigate();

    const { user } = useAuth();

    /*useEffect(() => {
        axios.get('/projects').then(res => {
            setProjects(res.data);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);*/

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
        axios.get('/admin/projects', requestConfig).then(res => {
            const projects = res.data;
            setProjects(projects);
            setNumberOfEntries(parseInt(res.headers['x-total-count']));
        })
        .catch(err => {
            console.log(err);
        });
    }, [navigate, user, page, pageSize]);


    const headers = [
        {
            header: 'Project',
            key: 'title'
        },
        {
            header: 'ID',
            key: 'id'
        },
        {
            header: 'Date Added',
            key: 'date'
        },
        {
            header: 'Description',
            key: 'description'
        },
        {
            header: 'Tags',
            key: 'tags'
        },
        {
            header: 'Visit Count',
            key: 'visit_count'
        }
    ];


    function handleCell(cell) {
        if (cell.info.header ==='date') {
            return cell.value.slice(0,10);
        } 
        if (cell.info.header ==='tags') {
            let first = true;
            let currentTag =''; 
            return cell.value.map(tag => {
                currentTag = first ? tag.tagName : ', ' + tag.tagName;
                first = false;
                return currentTag;
            });
        } else return cell.value;
    }


    function handleDelete(selectedProjects) {
        selectedProjects.map(async(project) => {
            const currentId = project.id;
            try {
                console.log(currentId);
                await axios.delete(`/user/project/${currentId}`, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
                window.location.reload(true);
            } catch(error) {
                console.log(error);
            }
        });
    }

    const handlePaginationChange = event => {
        setPage(event.page);
        setPageSize(event.pageSize);
    };


    function handleModifyProject() {
    }

    return (

        <>
        <DataTable headers={headers} rows={projects} >
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

                <Modal open={modalOpen}
                    danger
                    size='sm'
                    modalHeading='Are you sure you want to delete the currently selected project(s)? This action is irreversible.'
                    modalLabel='Delete Projects'
                    primaryButtonText='Delete'
                    secondaryButtonText='Cancel'
                    onRequestClose={() => setModalOpen(false)}
                    onRequestSubmit={() => handleDelete(selectedRows)}
                />
                    <TableToolbar >
                        <TableBatchActions {...batchActionProps}>
                            <TableBatchAction {...getToolbarProps({onClick: () => setModalOpen(modalOpen => !modalOpen)})}
                                tabIndex={batchActionProps.shouldShowBatchActions ? 0 : -1}
                                renderIcon={TrashCan}
                                >
                                Delete
                            </TableBatchAction>
                            <TableBatchAction {...getToolbarProps({onClick: () => handleModifyProject()})}
                                tabIndex={batchActionProps.shouldShowBatchActions ? 0 : -1}
                                renderIcon={Edit}
                                >
                                Modify Project
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
                            <TableRow key={rows.id} {...getRowProps({ row })}>
                            <TableSelectRow {...getSelectionProps({ row })} />
                            {row.cells.map((cell) => (
                                <TableCell key={cell.id}>
                                    {(cell.info.header==='date'||cell.info.header==='tags') ? handleCell(cell) : cell.value}
                                </TableCell>
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

export default ManageProjectsPage;