import { Heading, FileUploader, Form, Stack, ComboBox, Checkbox, Button, Tile } from '@carbon/react';

function ShowcaseSettingsPage() {
    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Showcase Settings</Heading>
        <Form>
            <Stack gap={5}>
                <Tile style = {{maxWidth: '500px', paddingBottom: '2px', marginBottom: '5px '}}>
                    <FileUploader
                        labelTitle='Upload header image'
                        labelDescription='Max file size is 10mb. Only .png files are supported.'
                        buttonLabel='Add file'
                        buttonKind='secondary'
                        filenameStatus='edit'
                        accept={['.jpg', '.png']}
                        multiple={false}
                        disabled={false}
                        iconDescription='Delete file'
                        name=''
                    />
                </Tile>
                <Checkbox 
                    labelText='Show project preview images on the showcase page' 
                    id='new-projects-approved-checkbox' 
                    checked={true}
                />
                <Checkbox 
                    labelText='Show featured project at top of page' 
                    id='project-edits-approved-checkbox' 
                    checked={true}
                />
                <div style = {{maxWidth: '500px'}}>
                <ComboBox
                    id='featured-project-dropdown'
                    label='Featured project'
                    titleText='Featured project'
                    helperText='Select the project to be featured on the showcase page'
                    items={['Project 1', 'Project 2', 'Project 3']}
                    size = 'lg'
                />
                </div>
                <Button>Save</Button>
            </Stack>
        </Form>
        </>
    );
}

export default ShowcaseSettingsPage;