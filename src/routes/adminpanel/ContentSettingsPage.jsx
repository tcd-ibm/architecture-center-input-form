import { useEffect, useState } from 'react';
import axios from 'axios';
import { Accordion, AccordionItem, Heading, Form, Stack, Dropdown, Checkbox, Button, Tag } from '@carbon/react';

import AddTagForm from '@/Components/AddTagForm';

import styles from './ContentSettingsPage.module.scss';

function ContentSettingsPage() {
    const items = [
        {
          id: 'everyone',
          text: 'Everyone',
        },
        {
          id: 'users',
          text: 'Users',
        },
        {
          id: 'admins',
          text: 'Admins',
        }
    ];

    const [tags, setTags] = useState([]);

    const fetchTags = () => {
        axios.get('/tags').then(res => {
            setTags(res.data);
        })
        .catch(err => {
            console.log(err);
        });
    };

    useEffect(fetchTags, []);

    const handleAddTag = (categoryId, tagName) => {
        console.log(categoryId, tagName);
    };

    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Content Settings</Heading>
        <Form>
            <Stack gap={5} className={styles.stackContainer}>
                <Dropdown
                    id='inline'
                    titleText='Who can add new projects'
                    label='Who can add new projects'
                    initialSelectedItem={items[1]}
                    type='inline'
                    items={items}
                    itemToString={(item) => (item ? item.text : '')}
                    disabled={true}
                />
                <Checkbox 
                    labelText='New projects have to be approved by an admin' 
                    id='new-projects-approved-checkbox' 
                    checked={true}
                    disabled={true}
                />
                <Checkbox 
                    labelText='Project edits have to be approved by an admin' 
                    id='project-edits-approved-checkbox' 
                    checked={true}
                    disabled={true}
                />
                <Button style={{marginTop: '10px', marginBottom: '50px'}} disabled={true}>Save</Button>
            </Stack>
        </Form>
        <Heading style={{marginBottom: '20px'}}>Project Tags</Heading>
        <Accordion style={{maxWidth: '400px'}}>
            {tags.map(category => 
                <AccordionItem key={category.categoryId} title={category.categoryName}>
                    <div style={{width: '100%'}}>
                        {category.tags.map(tag => 
                            <Tag type='magenta' title='Clear Filter' key={tag.tagId}>{tag.tagName}</Tag>    
                        )}
                        <AddTagForm onSubmit={tagName => handleAddTag(category.categoryId, tagName)} />
                    </div>
                </AccordionItem>
            )}
        </Accordion>
        </>
    );
}

export default ContentSettingsPage;