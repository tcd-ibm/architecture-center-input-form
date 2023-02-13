import { SideNav, Search } from '@carbon/react';
import './ProjectQuerySidePanel.scss'

function ProjectQuerySidePanel() {
    return (
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}>

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