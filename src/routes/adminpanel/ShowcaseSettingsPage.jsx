import { Heading, FileUploader, Form, Stack, Dropdown, Checkbox, Button } from '@carbon/react';

function ShowcaseSettingsPage() {
    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Showcase Settings</Heading>
        <Form>
            <Stack gap={5}>
                <FileUploader
                    labelTitle='Upload header image'
                    labelDescription='Max file size is 100mb. Only .png files are supported.'
                    buttonLabel='Add file'
                    buttonKind='primary'
                    size='md'
                    filenameStatus='edit'
                    accept={['.jpg', '.png']}
                    multiple={true}
                    disabled={false}
                    iconDescription='Delete file'
                    name=''
                />
                <Checkbox 
                    labelText='Show project preview images on the showcase page' 
                    id='new-projects-approved-checkbox' 
                    checked={true}
                />
                <Checkbox 
                    labelText='Project edits have to be approved by an admin' 
                    id='project-edits-approved-checkbox' 
                    checked={true}
                />
                <Button>Save</Button>
            </Stack>
        </Form>
        </>
    );
}

export default ShowcaseSettingsPage;