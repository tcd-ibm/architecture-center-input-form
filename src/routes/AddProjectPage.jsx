import { Tile, Content, Tag, FormGroup, Stack, TextInput, Button } from '@carbon/react';

import MainHeader from '@/Components/MainHeader';
import DocEditor from '@/Components/AsciidocEditor';

function AddProjectPage() {
    return (
        <>
        <MainHeader />
        <Content style={{marginLeft: '20px', marginRight: '20px'}}>
            <h1 style={{marginBottom: '10px'}}>Add New Project</h1>
            <FormGroup>
                <Stack gap={5}>
                    <TextInput id="one" labelText="Project Title" />
                    <TextInput id="two" labelText="Link to Project" />
                    <Tile>
                        <h4 style={{marginBottom: '10px'}}>Main Content</h4>
                        <DocEditor />
                    </Tile>
                    <Button>Submit</Button>
                </Stack>
            </FormGroup>
        </Content>
        </>
    );
}

export default AddProjectPage;