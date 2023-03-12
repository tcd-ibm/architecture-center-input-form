import { useState, useRef, useImperativeHandle, forwardRef } from 'react';
import { SideNav, Stack, Search, Accordion, AccordionItem, Checkbox } from '@carbon/react';
import styles from './ProjectQuerySidePanel.module.scss';

function ProjectQuerySidePanel(props, ref) {
    const { menuContent, onChange } = props;

    const selectedTagListRef = useRef([]);
    const [selectedTagList, setSelectedTagList] = useState([]);

    useImperativeHandle(ref, () => ({
        get selectedTagList() {
            return selectedTagListRef.current;
        }
    }), []);

    const handleFilterChange = event => {
        const { checked, id } = event.target;
        if(checked) {
            const newState = [...selectedTagList, id];
            selectedTagListRef.current = newState;
            setSelectedTagList(newState);
        } else {
            const newState = selectedTagList.filter(item => item !== id);
            selectedTagListRef.current = newState;
            setSelectedTagList(newState);
        }
        onChange();
    };

    const handleSearch = (event) => {
        if (event.key === 'Enter' || document.querySelector('input').value === '') {
            onChange();
        }
    };

    return (
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}
            aria-label='Search and filter'>

            <Stack gap={5} className={styles.innerContainer}>
                <Search
                    labelText='Search'
                    placeholder='Search'
                    onKeyUp={handleSearch}
                />
                {menuContent && <Accordion>
                    {menuContent.map((item, index) => <AccordionItem title={item.title} key={index}>
                        <fieldset className='cds--fieldset'>
                            {item.tags.map((tagItem, index) => 
                                <Checkbox labelText={tagItem.name} id={tagItem.id} checked={selectedTagList.includes(tagItem.id)} onChange={handleFilterChange} key={index} />
                            )}
                        </fieldset>
                    </AccordionItem>)}
                </Accordion>}
            </Stack>
            
        </SideNav>
    );
}

export default forwardRef(ProjectQuerySidePanel);