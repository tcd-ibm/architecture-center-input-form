import { SideNav } from '@carbon/react';
import './ProjectQuerySidePanel.scss'

import SearchBar from '../Components/SearchBar';

function ProjectQuerySidePanel() {
    return (
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}>

            <div className='innerContainer'>
                <SearchBar />
            </div>
            
        </SideNav>
    );
}

export default ProjectQuerySidePanel;