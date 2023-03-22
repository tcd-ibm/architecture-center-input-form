import axios from 'axios';
import { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Content, Form, TextInput, Stack, Tile, TextArea, Button, Tag } from '@carbon/react';

import MainHeader from '@/Components/MainHeader';
import DocEditor from '@/Components/AsciidocEditor';

import useAuth from '@/hooks/useAuth';

// ==============================================================
//                              NOTE                             
// ==============================================================
// the following implementation is NOT complete
// only basic request logic for submitting the form is implemented to test the API communication
// layout, styling and form logic has NOT been implemented
// ==============================================================

function AddProjectPage() {

    const { user } = useAuth();
    const navigate = useNavigate();

    const [input, setInput] = useState('');
    const [tags, setTags] = useState([]);

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
            setTags(res.data);
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
            tags: [1,2]
        };

        try {
            await axios.post('/user/project', requestBody, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
            navigate('/');
        } catch(error) {
            console.log(error);
        }
    };

    const handleClick = () => {
        const id = tags.length + 1;
        setTags((prev) => [
          ...prev,
          {
            id: id,
            task: input,
            complete: false,
          }
        ]);
        setInput('');
    };

    const handleComplete = id => {
        setTags(tags.filter(item => item.id !== id));
    };

    return (
        <>
        <MainHeader />
        <Content style={{marginLeft: '5%', marginRight: '5%'}}>
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
                    <div style={{display: 'flex', alignItems: 'center', flexDirection: 'row', marginBottom: '10px'}}>
                        <TextInput placeholder='Enter tag here' value={input} onInput={(e) =>setInput(e.target.value)} style={{marginRight: '10px'}} />
                        <Button onClick={() => handleClick()} size='md' kind='secondary' >Add</Button>
                    </div>
                    <div>
                      {tags.map((todo) => {
                        return (
                          <Tag
                            type='magenta'
                            title='Clear Filter'
                            key={todo.id}
                            onClick={() => handleComplete(todo.id)}
                          >
                            {todo.task}
                          </Tag>
                        );
                      })}
                    </div>
                </Tile>
                <Tile>
                    <h4 style={{marginBottom: '10px'}}>Main Content</h4>
                    <DocEditor />
                </Tile>
                <Button type='submit'>Save</Button>
            </Stack>
            </Form>
            {/* <DocEditor /> */}
        </Content>
        </>
    );
}

export default AddProjectPage;