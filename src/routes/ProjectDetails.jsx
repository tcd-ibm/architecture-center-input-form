import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import axios from 'axios';
import MainHeader from '@/Components/MainHeader';
import { Tile, Content, Link, Grid, Column, Tag } from '@carbon/react';
import { ArrowRight, LogoGithub, DataDefinition, Calendar, Document } from '@carbon/icons-react';
import Asciidoctor from 'asciidoctor';
import styles from './ProjectDetails.module.scss';

const asciidoctor = Asciidoctor();

function ProjectDetails() {

    const { projectId } = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [project, setProject] = useState();

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
                    <div className={styles.tileContainer}>
                        {/*Project heading*/}
                        <Tile style = {{maxWidth: '1100px', minWidth: '900px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', marginLeft: '10px', flex: '80%'}}>
                            <div className={styles.divCenter}>
                                <h1>{project.title}</h1>
                            </div>
                        </Tile>
                        {/*Project Icon*/}
                        <Tile style = {{maxWidth: '200px', minWidth: '50px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '20%'}}>
                            <div className={styles.divCenter}>
                                <img src={`http://localhost:5297/api/v1/project/${projectId}/image`} style={{width:'100%', maxWidth: '200px'}} alt='Project'
                                onError={event => event.target.style.display = 'none'} />
                            </div>
                        </Tile>
                    </div>

                    <br></br>

                    <Grid className={styles.contentsGrid}>
                        <Column sm={0} md={2} lg={4}>
                            <Tile>
                                <div className={styles.divCenter}>
                                    <h3>Project Link<LogoGithub style = {{height: '23px', width: '40px'}}></LogoGithub></h3>
                                </div>
                                <br></br>
                                <div className={styles.divCenter}>
                                    <Link href={project.link} size='lg' renderIcon={ArrowRight}>Click Here</Link>
                                </div>
                            </Tile>
                            <br></br>
                            <Tile>
                                <div className={styles.divCenter}>
                                    <h3>Description<Document style = {{height: '23px', width: '40px'}}></Document></h3>
                                </div>
                                <br></br>
                                <div className={styles.divCenter}>
                                    <h4>{project.description}</h4>
                                </div>
                            </Tile>
                            <br></br>
                            <Tile>
                                <div className={styles.divCenter}>
                                    <h3>Tags<DataDefinition style = {{height: '23px', width: '40px'}}></DataDefinition></h3>
                                </div>
                                <br></br>
                                <div className='tags'>
                                    {project.tags.map(tagItem => 
                                        <Tag type='magenta' title='Clear Filter' key={tagItem.tagId}>{tagItem.tagName}</Tag>
                                    )}
                                </div>
                            </Tile>
                        </Column>
                        <Column sm={4} md={6} lg={12}>
                            <div className={styles.descriptionBody} dangerouslySetInnerHTML={{ __html: asciidoctor.convert(project.content) }} />
                            <img src={`http://localhost:5297/api/v1/project/${projectId}/image`} style={{width:'100%', maxWidth: '600px'}} alt='Project'
                                onError={event => event.target.style.display = 'none'} />
                        </Column>
                    </Grid>


                    <br></br>
                    </>
                }
            </Content>
        </>
    );
}

export default ProjectDetails;