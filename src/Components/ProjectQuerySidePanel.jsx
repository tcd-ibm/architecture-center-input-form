import { useState, useRef, useImperativeHandle, forwardRef, useEffect } from 'react';
import { SideNav, Stack, Search, Accordion, AccordionItem, Checkbox } from '@carbon/react';
import styles from './ProjectQuerySidePanel.module.scss';

function ProjectQuerySidePanel(props, ref) {
    const { menuContent, onChange } = props;

    const selectedTagListRef = useRef([]);
    const [selectedTagList, setSelectedTagList] = useState([]);
    const [isOnMobile, setIsOnMobile] = useState([]);

    useEffect(() => {
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        const handleResize = () => {
            if (mediaQuery.matches) {
                setIsOnMobile(true);
            } else {
                setIsOnMobile(false);
            }
        };
        handleResize();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const url = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/logo.png?alt=media&token=9f7ab576-c49a-40ec-879a-152942825667';

    useImperativeHandle(ref, () => ({
        get selectedTagList() {
            return selectedTagListRef.current;
        }
    }), []);

    const handleFilterChange = event => {
        const { checked, id } = event.target;
        if (checked) {
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
        onChange();
    };

    return (
        <SideNav
            className='sideNav1'
            isFixedNav
            expanded={isOnMobile ? false : true}
            isChildOfHeader={false}
            aria-label='Search and filter'>

            <Stack gap={5} className={styles.innerContainer}>
                <Search
                    labelText='Search'
                    placeholder='Search'
                    onChange={handleSearch}
                />
                {menuContent && <Accordion>
                    {menuContent.map((item, index) => <AccordionItem title={item.title} key={index} open>
                        <fieldset className='cds--fieldset'>
                            {item.tags.map((tagItem, index) =>
                                <Checkbox labelText={tagItem.name} id={tagItem.id} checked={selectedTagList.includes(tagItem.id)} onChange={handleFilterChange} key={index} />
                            )}
                        </fieldset>
                    </AccordionItem>)}
                </Accordion>}
                {/*
                <img src={url} style={{maxWidth: '50%', marginLeft: 'auto', marginRight: 'auto', marginTop: '20px'}} onError={(event) => event.target.style.display = 'none'} />
                */}
            </Stack>

        </SideNav>
    );
}

export default forwardRef(ProjectQuerySidePanel);