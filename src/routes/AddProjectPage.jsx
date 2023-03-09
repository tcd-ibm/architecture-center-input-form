import axios from 'axios';
import { useEffect, useContext, useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Content, Form, TextInput, Stack, Tile, TextArea, Button } from '@carbon/react';

import MainHeader from '@/Components/MainHeader';
import DocEditor from '@/Components/AsciidocEditor';

import AuthContext from '@/context/AuthContext';

// ==============================================================
//                              NOTE                             
// ==============================================================
// the following implementation is NOT complete
// only basic request logic for submitting the form is implemented to test the API communication
// layout, styling and form logic has NOT been implemented
// ==============================================================

function AddProjectPage() {

    const [user, setUser] = useContext(AuthContext);
    const navigate = useNavigate();

    const [tags, setTags] = useState(null);

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
                <Tile style={{paddingBottom: '0px', paddingTop: '5px', paddingRight: '0px'}}>
                    {/* <h4 style={{marginBottom: '10px'}}>Main Content</h4> */}
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