import {
  useState,
  useRef,
  useImperativeHandle,
  forwardRef,
  useEffect,
} from 'react';
import {
  SideNav,
  Stack,
  Search,
  Accordion,
  AccordionItem,
  Checkbox,
  DatePicker,
  DatePickerInput,
  Tile,
  Toggle,
} from '@carbon/react';
import styles from './ProjectQuerySidePanel.module.scss';
import { useMediaQuery } from 'react-responsive';

function ProjectQuerySidePanel(props, ref) {
  const { menuContent, onChange, getExpandedState, toggleExpandedState } =
    props;
  const selectedTagListRef = useRef([]);
  const [selectedTagList, setSelectedTagList] = useState([]);
  const isOnMobile = useMediaQuery({ query: '(max-width: 760px)' });

  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [filterDate, setFilterDate] = useState(false);

  useImperativeHandle(
    ref,
    () => ({
      get selectedTagList() {
        return selectedTagListRef.current;
      },
    }),
    []
  );

  const handleFilterChange = (event) => {
    const { checked, id } = event.target;
    if (checked) {
      const newState = [...selectedTagList, id];
      selectedTagListRef.current = newState;
      setSelectedTagList(newState);
    } else {
      const newState = selectedTagList.filter((item) => item !== id);
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
      expanded={getExpandedState()}
      isChildOfHeader={false}
      aria-label='Search and filter'
    >
      <Stack gap={5} className={styles.innerContainer}>
        {isOnMobile ? null : (
          <Search
            labelText='Search'
            placeholder='Search'
            onChange={handleSearch}
          />
        )}

        {menuContent && (
          <Accordion>
            {menuContent.map((item, index) => (
              <AccordionItem title={item.title} key={index} open>
                <fieldset className='cds--fieldset'>
                  {item.tags.map((tagItem, index) => (
                    <Checkbox
                      labelText={tagItem.name}
                      id={tagItem.id}
                      checked={selectedTagList.includes(tagItem.id)}
                      onChange={handleFilterChange}
                      key={index}
                    />
                  ))}
                </fieldset>
              </AccordionItem>
            ))}
          </Accordion>
        )}
        <Tile style={{ border: '1px solid gray' }}>
          <DatePicker
            style={{ marginBottom: '20px' }}
            datePickerType='single'
            dateFormat='d/m/Y'
            value={startDate}
            onChange={(date) => setStartDate(new Date(date))}
          >
            <DatePickerInput
              id='date-picker-input-id-start'
              placeholder='dd/mm/yyyy'
              labelText='Start date'
              size='sm'
              style={{ width: '190px' }}
            />
          </DatePicker>
          <DatePicker
            style={{ marginBottom: '20px' }}
            datePickerType='single'
            dateFormat='d/m/Y'
            value={endDate}
            onChange={(date) => setEndDate(new Date(date))}
          >
            <DatePickerInput
              id='date-picker-input-id-finish'
              placeholder='dd/mm/yyyy'
              labelText='End date'
              size='sm'
              style={{ width: '190px' }}
            />
          </DatePicker>
          <Toggle
            labelText='Apply Date Filter'
            labelA='Off'
            labelB='On'
            id='toggle-1'
            size='sm'
            onToggle={(event) => setFilterDate(event)}
          />
        </Tile>
      </Stack>

      {isOnMobile ? (
        <div id={styles.filterOptions}>
          <button
            id={styles.applyFiltersBtn}
            onClick={() => {
              setSelectedTagList([]);
              selectedTagListRef.current = [];
            }}
          >
            Reset
          </button>
          <button
            id={styles.applyFiltersBtn}
            onClick={() => {
              toggleExpandedState();
            }}
          >
            Apply
          </button>
        </div>
      ) : null}
    </SideNav>
  );
}

export default forwardRef(ProjectQuerySidePanel);
