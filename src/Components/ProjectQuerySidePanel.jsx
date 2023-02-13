import { SideNav, Search } from '@carbon/react';
import './ProjectQuerySidePanel.scss'

function ProjectQuerySidePanel() {
    return (
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}
            aria-label="Search and filter">

            <div className='innerContainer'>
                <Search
                    labelText="Search"
                    placeholder="Search"
                />
            </div>
            
        </SideNav>
    );
}

export default ProjectQuerySidePanel;