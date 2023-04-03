import axios from 'axios';
import { useEffect, useState, useRef, useImperativeHandle  } from 'react';
import { Content, Form, TextInput, Stack, Tile, TextArea, Button, Tag, DatePicker, DatePickerInput } from '@carbon/react';
import { useNavigate } from 'react-router';

import DocEditor from '@/Components/AsciidocEditor';
import styles from './EditProject.module.scss';

export default function EditProject({projectData, user, isEdit}) {

	const navigate = useNavigate();

	const [tags, setTags] = useState([]);
    const [date, setDate] = useState(projectData.date);

    const titleInputRef = useRef();
    const linkInputRef = useRef();
    const completionDateInputRef = useRef();
    const previewDescriptionInputRef = useRef();
    const contentInputRef = useRef();
    const [content, setContent] = useState(projectData.content);

	useEffect(() => {
        if(!user) {
			navigate('/login', { replace: true });
		}
        try {
            axios.get('/tags').then(res => {
                const tempTags = res.data.map(categoryItem => categoryItem.tags).flat();
                if (isEdit) {
                    setTags(tempTags.map(item =>
                        (projectData.tags.some(selectedTag => selectedTag.tagId === item.tagId) ? { ...item, selected: true } : item)
                    ));
                } else {
                    setTags(tempTags);
                }
            });
        } catch (error) {
            console.error(error);
        }
    }, [navigate, user]);

    const handleSubmit = async event => {
        event.preventDefault();
        const requestBody = {
            title: titleInputRef.current.value,
            link: linkInputRef.current.value,
            description: previewDescriptionInputRef.current.value,
            content: contentInputRef.current.value,
            date: date,
            tags: tags.filter(item => item?.selected).map(item => item.tagId)
        };

        try {
            console.log(requestBody);
            if (isEdit) { // If editing an existing project
                await axios.put(`/user/project/${projectData.id}`, requestBody, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
            } else {      // If creating a new project
                await axios.post('/user/project', requestBody, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } });
            }
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
    
    const [invalidText, setInvalidText] = useState(null);

    const validateLink = () => {
        if(!linkInputRef.current.value) {
            setInvalidText('Link is required');
            return false;
        }
        if(!/^(http(s):\/\/.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$/.test(linkInputRef.current.value)) {
            setInvalidText('Enter a valid link');
            return false;
        }
        setInvalidText(null);
        return true;
    };

	return (
		<>
        <Content className={styles.contentBody}>
            <Form onSubmit={handleSubmit}>
            <Stack gap={6}>
                <h1>Add New Project</h1>
                <TextInput labelText='Project Title' id='title' ref={titleInputRef} defaultValue={projectData.title} required />
                <TextInput labelText='Link to Project' placeholder='https://example.com' defaultValue={projectData.link} id='link' invalid={Boolean(invalidText)} invalidText={invalidText} ref={linkInputRef} onBlur={validateLink}/>
                {/*<TextInput labelText='Completion Date' id='date' ref={completionDateInputRef} placeholder='2023-01-01' />*/}
                <DatePicker datePickerType='single' dateFormat='d/m/Y' value={date} onChange={date => setDate(date)}>
                    <DatePickerInput
                      placeholder='dd/mm/yyyy'
                      labelText='Completion Date'
                      id='date'
                      ref={completionDateInputRef}
                      style={{margin: '0px'}}
                    />
                </DatePicker>

                <TextArea
                    labelText='Preview description'
                    rows={4}
                    id='previewDescription'
                    ref={previewDescriptionInputRef}
					defaultValue={projectData.description}
                    disabled={false}
                    placeholder='An omnichannel approach provides a unified customer experience across platforms, creating a single view for customers to interact with their own information.'
                />

                <Tile style={{padding: '20px'}}>
                    <h4 style={{marginBottom: '10px'}}>Add Tags</h4>
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
                    <DocEditor code={content} ref={contentInputRef} />
                </Tile>
                <Button type='submit'>Save</Button>
            </Stack>
            </Form>
        </Content>
		</>
	);
}