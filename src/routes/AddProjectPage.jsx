import axios from 'axios';
import { useEffect, useContext, useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Content, Form, TextInput, Stack, Tile, TextArea, Button, Tag } from '@carbon/react';

import MainHeader from '@/Components/MainHeader';
import DocEditor from '@/Components/AsciidocEditor';
import styles from './AddProjectPage.module.scss';

import AuthContext from '@/context/AuthContext';

function AddProjectPage() {

    const [user, setUser] = useContext(AuthContext);
    const navigate = useNavigate();

    const [tags, setTags] = useState([]);
    //const [input, setInput] = useState('');

    const titleInputRef = useRef();
    const linkInputRef = useRef();
    const completionDateInputRef = useRef();
    const previewDescriptionInputRef = useRef();
    const contentInputRef = useRef();

    useEffect(() => {
        if(!user) {
            navigate('/login', { replace: true });
        }

        axios.get('/tags').then(res => {
            setTags( 
                res.data.map(categoryItem => categoryItem.tags).flat()
            );
        })
        .catch(error => {
            console.log(error);
        });
    }, [navigate, user]);

    const handleSubmit = async event => {
        event.preventDefault();
        const requestBody = {
            title: titleInputRef.current.value,
            link: linkInputRef.current.value,
            description: previewDescriptionInputRef.current.value,
            content: contentInputRef.current.value,
            date: new Date(completionDateInputRef.current.value),
            tags: tags.filter(item => item?.selected).map(item => item.tagId)
        };

        try {
            console.log(requestBody);
            await axios.post('/user/project', requestBody, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
            navigate('/');
        } catch(error) {
            console.log(error);
        }
    };

    const handleTagAdd = tagId => {
        setTags(tags.map(item => 
            (item.tagId === tagId ? { ...item, selected: true } : item)
        ));
    };

    const handleTagRemove = tagId => {
        setTags(tags.map(item => 
            (item.tagId === tagId ? { ...item, selected: false } : item)
        ));
    };

    return (
        <>
        <MainHeader />
        <Content className={styles.contentBody}>
            <Form onSubmit={handleSubmit}>
            <Stack gap={6}>
                <h1>Add New Project</h1>
                <TextInput labelText='Project Title' id='title' ref={titleInputRef} required />
                <TextInput labelText='Link to Project' id='link' ref={linkInputRef} placeholder='https://example.com'/>
                <TextInput labelText='Completion Date' id='date' ref={completionDateInputRef} placeholder='2023-01-01' />
                <TextArea
                    labelText='Preview description'
                    rows={4}
                    id='previewDescription'
                    ref={previewDescriptionInputRef}
                    disabled={false}
                    placeholder='An omnichannel approach provides a unified customer experience across platforms, creating a single view for customers to interact with their own information.'
                />
                <Tile style={{padding: '20px'}}>
                    <h4 style={{marginBottom: '10px'}}>Add Tags</h4>
                    {/* <div style={{display: 'flex', alignItems: 'center', flexDirection: 'row', marginBottom: '10px'}}>
                        <TextInput placeholder='Enter tag here' value={input} onInput={(e) =>setInput(e.target.value)} style={{marginRight: '10px'}} />
                        <Button onClick={() => handleClick()} size='md' kind='secondary' >Add</Button>
                    </div> */}
                    <div>
                        {tags.filter(item => !item?.selected).map(item => {
                            return (
                            <Tag
                                type='magenta'
                                title='Clear Filter'
                                key={item.tagId}
                                onClick={() => handleTagAdd(item.tagId)}
                            >
                                {item.tagName}
                            </Tag>
                            );
                        })}
                    </div>
                    <h4 style={{marginBottom: '10px', marginTop: '10px'}}>Currently selected</h4>
                    <div>
                        {tags.filter(item => item?.selected).map(item => {
                            return (
                            <Tag
                                type='magenta'
                                title='Clear Filter'
                                key={item.tagId}
                                onClick={() => handleTagRemove(item.tagId)}
                            >
                                {item.tagName}
                            </Tag>
                            );
                        })}
                    </div>
                </Tile>
                <Tile style={{paddingBottom: '0px', paddingTop: '10px', paddingRight: '0px'}}>
                    {/* <h4 style={{marginBottom: '10px'}}>Main Content</h4> */}
                    <DocEditor />
                </Tile>
                <Button type='submit'>Save</Button>
            </Stack>
            </Form>
        </Content>
        </>
    );
}

export default AddProjectPage;