import { Heading, Form, Stack, Dropdown, Checkbox, Button } from '@carbon/react';

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
                />
                <Checkbox 
                    labelText='New projects have to be approved by an admin' 
                    id='new-projects-approved-checkbox' 
                    checked={true}
                />
                <Checkbox 
                    labelText='Project edits have to be approved by an admin' 
                    id='project-edits-approved-checkbox' 
                    checked={true}
                />
                <Button style={{marginTop: '10px', marginBottom: '50px'}}>Save</Button>
            </Stack>
        </Form>
        </>
    );
}

export default ContentSettingsPage;