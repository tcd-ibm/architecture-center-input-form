import { SideNav, Stack, Search, Accordion, AccordionItem, Checkbox } from '@carbon/react';
import './ProjectQuerySidePanel.scss'

function ProjectQuerySidePanel({menuContent, filterTagList, handleFilterChange}) {
    return (
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}
            aria-label="Search and filter">

            <Stack gap={5} className='innerContainer'>
                <Search
                    labelText="Search"
                    placeholder="Search"
                />
                {menuContent && <Accordion>
                    {menuContent.map((item, index) => <AccordionItem title={item.title} key={index}>
                        <fieldset className='cds--fieldset'>
                            {item.tags.map((tagItem, index) => <Checkbox labelText={tagItem.name} id={tagItem.id} checked={filterTagList.includes(tagItem.id)} onChange={handleFilterChange} key={index} />)}
                        </fieldset>
                    </AccordionItem>)}
                </Accordion>}
            </Stack>
            
        </SideNav>
    );
}

export default ProjectQuerySidePanel;