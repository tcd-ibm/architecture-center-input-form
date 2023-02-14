import { Content } from '@carbon/react';

import MainHeader from '@/Components/MainHeader';
import DocEditor from '@/Components/AsciidocEditor';

function AddProjectPage() {
    return (
        <>
        <MainHeader />
        <Content>
            <DocEditor />
        </Content>
        </>
    );
}

export default AddProjectPage;