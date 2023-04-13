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
  const [pageSize, setPageSize] = useState(6);
  const [totalProjects, setTotalProjects] = useState();

  useEffect(() => {
    // sets the sidebar to be hidden by default on mobile
    if (isOnMobile) {
      setSideBarExpanded(false);
    } else {
      setSideBarExpanded(true);
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

  const handlePaginationChange = (event) => {
    setPage(event.page);
    setPageSize(event.pageSize);
  };

  const requestConfig = {
    params: {
      per_page: pageSize,
      page: page,
    },
  };

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

  useEffect(() => {
    axios
      .get('/projects', requestConfig)
      .then((res) => {
        setProjects(res.data.filter(proj => ((!featuredProject.id) || proj.id !== featuredProject.id)));
        setIsLoading(false);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [page, pageSize]);

  useEffect(() => {
    axios
      .get('/projects')
      .then((res) => {
        setTotalProjects(res.data.length);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [totalProjects]);

  const handleSearchAndFilterChange = () => {
    const params = {
      keyword: document.querySelector('#searchBox').value,
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

  return (
    <>
      <MainHeader toggleSideBar={toggleExpandedState} />
      <ProjectQuerySidePanel
        menuContent={queryMenuContent}
        ref={queryMenuRef}
        getExpandedState={getExpandedState}
        toggleExpandedState={toggleExpandedState}
        onChange={handleSearchAndFilterChange}
      />
      <Content style={isOnMobile ? { padding: '0px', margin: '0px', marginTop: '15px' } : { padding: '0px', paddingTop: '5px' }}
      >
        <div style={{ margin: '20px' }}>
          {isOnMobile ? (
            <div className={styles.searchBar}>
              <Search
                id='searchBox'
                labelText='Search'
                placeholder='Search'
                onChange={handleSearchAndFilterChange}
              />
            </div>
          ) : null}

          {/* {isOnMobile ? (
          <p
            id={styles.filtersBtn}
            onClick={() => {
              toggleExpandedState();
            }}
          >
            <span>Filters</span>
            <Filter />
          </p>
        ) : null} */}

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
        </div>
        <Pagination
          className={styles.pagination}
          backwardText='Previous page'
          forwardText='Next page'
          itemsPerPageText='Items per page:'
          onChange={handlePaginationChange}
          page={page}
          pageSize={pageSize}
          pageSizes={[10, 20, 30]}
          size='lg'
          totalItems={projects.length}
        />
      </Content>
    </>
  );
}

export default MainPage;
