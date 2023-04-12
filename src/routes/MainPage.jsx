import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Content, Loading, Search, Pagination } from '@carbon/react';
import styles from './MainPage.module.scss';
import { useMediaQuery } from 'react-responsive';

import MainHeader from '@/Components/MainHeader';
import ProjectQuerySidePanel from '@/Components/ProjectQuerySidePanel';
import Card from '@/Components/Card';
import FeaturedCard from '../Components/FeaturedCard';
import { Filter } from '@carbon/icons-react';

function MainPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [projects, setProjects] = useState([]);
  const [featuredProject, setFeaturedProject] = useState();
  const [queryMenuContent, setQueryMenuContent] = useState([]);
  const [sideBarExpanded, setSideBarExpanded] = useState(true);
  const queryMenuRef = useRef();
  const isOnMobile = useMediaQuery({ query: '(max-width: 760px)' });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(2);
  const [pageNum, setPageNum] = useState(0);
  const [numberOfEntries, setNumberOfEntries] = useState();
  
  useEffect(() => {
    // sets the sidebar to be hidden by default on mobile
    if (isOnMobile) {
      setSideBarExpanded(false);
    }
  }, []);

  useEffect(() => {
    axios
      .get('/tags')
      .then((res) => {
        const content = res.data.map((item) => ({
          title: item.categoryName,
          tags: item.tags.map((tagItem) => ({
            id: String(tagItem.tagId),
            name: tagItem.tagName,
          })),
        }));
        setQueryMenuContent(content);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const requestConfig = { 
    params: {
      per_page: pageSize,
      page: page
    } 
  };

  useEffect(() => {
    axios
      .get('/projects', requestConfig)
      .then((res) => {
        setProjects(res.data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  useEffect(() => {
    axios
      .get('/project/featured')
      .then((res) => {
        setFeaturedProject(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const handleSearchAndFilterChange = () => {
    const params = {
      keyword: document.querySelector('input').value,
      tags: queryMenuRef.current.selectedTagList.join(','),
    };

    axios
      .get('./projects', { params })
      .then((res) => {
        setProjects(res.data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const getExpandedState = () => {
    return sideBarExpanded;
  };

  const toggleExpandedState = () => {
    setSideBarExpanded(!sideBarExpanded);
  };

  const handlePaginationChange = event => {
    setPage(event.page);
    setPageSize(event.pageSize);
};

  return (
    <>
      <MainHeader />
      <ProjectQuerySidePanel
        menuContent={queryMenuContent}
        ref={queryMenuRef}
        getExpandedState={getExpandedState}
        toggleExpandedState={toggleExpandedState}
        onChange={handleSearchAndFilterChange}
      />
      <Content
        style={
          isOnMobile ? { padding: '16px', margin: 0, 'marginTop': '64px' } : {}
        }
      >
        {isOnMobile ? (
          <Search
            labelText='Search'
            placeholder='Search'
            onChange={handleSearchAndFilterChange}
          />
        ) : null}

        {isOnMobile ? (
          <p
            id={styles.filtersBtn}
            onClick={() => {
              toggleExpandedState();
            }}
          >
            <span>Filters</span>
            <Filter />
          </p>
        ) : null}

        {isLoading ? (
          <Loading
            withOverlay={false}
            style={{ margin: 'auto', marginTop: '30px' }}
          />
        ) : (
          <div id={styles.cardContainer}>
            {featuredProject && (
              <FeaturedCard project={featuredProject} isOnMobile={isOnMobile} />
            )}
            {projects.map((projectData, index) => (
              <Card projectData={projectData} key={index} />
            ))}
          </div>
        )}
        { isLoading ? null: 
          <Pagination 
            backwardText='Previous page'
            forwardText='Next page'
            itemsPerPageText='Items per page:'
            onChange={handlePaginationChange}
            page={page}
            pageSize={pageSize}
            pageSizes={[4, 6, 8, 10 ]}
            size='lg'
            totalItems={10}
          />
        }
      </Content>
    </>
  );
}

export default MainPage;
