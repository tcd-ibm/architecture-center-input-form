import axios from 'axios';
import { useEffect, useContext, useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Content, Form, TextInput, TextArea, Button } from '@carbon/react';

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
    }, []);

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
            const response = await axios.post('/user/project', requestBody, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
            navigate('/');
        } catch(error) {
            console.log(error);
        }
    }

    return (
        <>
        <MainHeader />
        <Content>
            <Form onSubmit={handleSubmit}>
                <TextInput labelText='Project title' id='title' ref={titleInputRef} disabled={true} value='Test' />
                <TextInput labelText='github link' id='link' ref={linkInputRef} disabled={true} value='https://example.com' />
                <TextInput labelText='Completion date' id='date' ref={completionDateInputRef} disabled={true} value='2023-01-01' />
                <TextArea
                    labelText='Preview description'
                    rows={4}
                    id='previewDescription'
                    ref={previewDescriptionInputRef}
                    disabled={true}
                    value='An omnichannel approach provides a unified customer experience across platforms, creating a single view for customers to interact with their own information.'
                />
                <TextArea
                    labelText='Main content'
                    rows={8}
                    id='mainContent'
                    ref={contentInputRef}
                    disabled={true}
                    value={`This is an interactive editor.\nUse it to try https://asciidoc.org[AsciiDoc].\n\n== Section Title\n\n* A list item\n* Another list item\n\n[,ruby]\n----\nputs 'Hello, World!'\n----`}
                />
                <Button type='submit'>Save</Button>
            </Form>
            {/* <DocEditor /> */}
        </Content>
        </>
    );
}

export default AddProjectPage;