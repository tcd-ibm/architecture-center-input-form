import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import axios from 'axios';
import MainHeader from '@/Components/MainHeader';
import { Tile, Content, Link, Grid, Column, Tag } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
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
                    <Tile className={styles.titleBox}>
                        <h1 className={styles.titleHeading}>{project.title}</h1>
                        <Link href={project.link} size='lg' renderIcon={ArrowRight}>Project link</Link>
                    </Tile>
                    <Grid className={styles.contentsGrid}>
                        <Column sm={4} md={6} lg={12}>
                            <div className={styles.descriptionBody} dangerouslySetInnerHTML={{ __html: asciidoctor.convert(project.content) }} />
                        </Column>
                        <Column sm={0} md={2} lg={4}>
                            <Tile>
                                <h3>Tags</h3>
                                <div className='tags'>
                                    {project.tags.map(tagItem => 
                                        <Tag type='magenta' title='Clear Filter' key={tagItem.tagId}>{tagItem.tagName}</Tag>
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