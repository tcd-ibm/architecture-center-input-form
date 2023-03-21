import { Heading, FileUploader, Form, Stack, ComboBox, Checkbox, Button, Tile } from '@carbon/react';
import { useState } from 'react';
import { storage } from './../../firebase';
import { ref, uploadBytes } from 'firebase/storage';

function ShowcaseSettingsPage() {

    const [headerImage, setHeaderImage] = useState(null);
    const url = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/logo.png?alt=media&token=9f7ab576-c49a-40ec-879a-152942825667';
    const uploadImage = () => {
        if (headerImage == null) return;
        const imageRef = ref(storage, 'logo.png');
        uploadBytes(imageRef, headerImage).then((snapshot) => {
            window.location.reload(true);
        });
    };

    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Showcase Settings</Heading>
        <Form>
            <Stack gap={5}>
                <Tile style = {{maxWidth: '500px', paddingBottom: '10px', marginBottom: '5px '}}>
                    <img src={url} style={{maxWidth: '100%', marginBottom: '10px'}} onError={(event) => event.target.style.display = 'none'} />
                    <FileUploader
                        labelTitle='Upload header image'
                        labelDescription='Max file size is 10mb. Only .png files are supported.'
                        buttonLabel='Add file'
                        buttonKind='secondary'
                        filenameStatus='edit'
                        accept={['.png']}
                        multiple={false}
                        disabled={false}
                        iconDescription='Delete file'
                        name=''
                        onChange={(event) => {
                            setHeaderImage(event.target.files[0]);
                        }}
                    />
                </Tile>
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
                <Checkbox 
                    labelText='Show project preview images on the showcase page' 
                    id='new-projects-approved-checkbox' 
                />
                <Checkbox 
                    labelText='Show featured project at top of page' 
                    id='project-edits-approved-checkbox' 
                />
                <Button onClick={uploadImage} style={{marginTop: '10px', marginBottom: '50px'}}>Save</Button>
            </Stack>
        </Form>
        </>
    );
}

export default ShowcaseSettingsPage;