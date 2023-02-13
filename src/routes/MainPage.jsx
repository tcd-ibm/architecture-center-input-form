import { useState } from 'react';
import './MainPage.scss';
import SearchBar from '../Components/SearchBar';
import AsciidocEditor from '../Components/AsciidocEditor';
import Card from '../Components/Card';
import { Button } from '@carbon/react';

function MainPage() {

    const [isEditorOn, SetIsEditorOn] = useState(false);

    const editor = isEditorOn ? <AsciidocEditor /> : null;

    return (
        <div id="bodyContainer">
            {editor}
            <div id="sidebarContainer">
            <div class="fixed_elements">
                <SearchBar />
                <Button onClick={() => SetIsEditorOn(() => !isEditorOn)}>Editor</Button>
            </div>
            </div>

            <div /* separator */ />

            <div id="cardContainer">
            <Card />
            </div>

        </div>
    );
}

export default MainPage;