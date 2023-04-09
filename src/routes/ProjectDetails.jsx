import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import axios from 'axios';
import MainHeader from '@/Components/MainHeader';
import { Tile, Content, Grid, Column, Tag, Button } from '@carbon/react';
import { ArrowRight, LogoGithub, DataDefinition, Document, Link} from '@carbon/icons-react';
import Asciidoctor from 'asciidoctor';
import styles from './ProjectDetails.module.scss';
import { useMediaQuery } from 'react-responsive';

const asciidoctor = Asciidoctor();

function ProjectDetails() {

    const tagColors = ['red', 'magenta', 'purple', 'blue', 'cyan', 'teal', 'green', 'gray', 'cool-gray', 'warm-gray', 'high-contrast'];
    const { projectId } = useParams();
    const [isLoading, setIsLoading] = useState(true);
    const [project, setProject] = useState();
    const isOnMobile = useMediaQuery({ query: '(max-width: 671px)' });

    useEffect(() => {
        axios.get(`/project/${projectId}`).then(res => {
            setProject(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    }, [projectId]);

    return (
        <>
            <MainHeader />
            <Content className={styles.contentBox}>
                { isLoading ? <div>Loading...</div> : 
                    <>
                    <br></br>
                        {/*Project heading*/}
                        <Tile className={styles.tileContainer} style = {{paddingBottom: '20px', marginRight: '15px', marginLeft: '15px'}}>
                            <div className={styles.divCenter}>
                                <h2>{project.title}</h2>
                            </div>
                        </Tile>

                    <br></br>

                    <Grid>
                        <Column sm={4} md={6} lg={12} style={isOnMobile ? {} : {marginLeft: '0px', marginBottom: '20px'}} >
                            <div className={styles.descriptionBody} dangerouslySetInnerHTML={{ __html: asciidoctor.convert(project.content) }} />
                            
                        </Column>
                        <Column sm={4} md={2} lg={4} className={isOnMobile ? styles.mobileGrid : styles.normalGrid}>
                            <Tile className={styles.tileContainer}>
                                <img src={`http://localhost:5297/api/v1/project/${projectId}/image`} style={{width:'100%', maxWidth: '600px',marginBottom: '15px'}} alt='Project'
                                onError={event => event.target.style.display = 'none'} />
                                <Button href={project.link} size='lg' kind='tertiary' renderIcon={Link} style={{width: '100%', maxWidth: '100%'}}>Link to Project</Button>
                            </Tile>
                            <br></br>
                            <Tile className={styles.tileContainer}>
                                    <h5 style={{marginBottom: '5px'}}>Description</h5>
                                    <div style={{fontSize: '100%'}}>{project.description}</div>
                            </Tile>
                            <br></br>
                            <Tile className={styles.tileContainer}>
                                <h5 style={{marginBottom: '8px'}}>Tags</h5>
                                <div className='tags'>
                                    {project.tags.map(tagItem => 
                                        <Tag type={tagColors[tagItem.categoryId % 10]} title='Clear Filter' key={tagItem.tagId}>{tagItem.tagName}</Tag>
                                    )}
                                </div>
                            </Tile>
                        </Column>
                    </Grid>
                    </>
                }
            </Content>
        </>
    );
}

export default ProjectDetails;