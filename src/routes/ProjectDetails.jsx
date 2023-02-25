import { useState } from 'react';
import MainHeader from '@/Components/MainHeader';
import { Tile, Content, Link, Grid, Column, Tag } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import Asciidoctor from 'asciidoctor';
import './ProjectDetails.scss';

const asciidoctor = Asciidoctor();

function ProjectDetails() {

    const [desc, setDesc] = useState(`=== Section Title\nHello 123\n\n_test_\n\n*Testing*`);

    return (
        <>
            <MainHeader />
            <Content className="contentBox">
                <Tile className="titleBox">
                    <h1>Sample Heading</h1>
                    <Link href="https://google.com" size="lg" renderIcon={ArrowRight}>Project link</Link>
                </Tile>
                <Grid className="contentsGrid">
                    <Column sm={4} md={6} lg={12}>
                        <div className='descriptionBody' dangerouslySetInnerHTML={{ __html: asciidoctor.convert(desc) }} />
                    </Column>
                    <Column sm={0} md={2} lg={4}>
                        <Tile>
                            <h3>Tags</h3>
                            <div className='tags'>
                                
                                <Tag type="red">{'Example tag'}</Tag>
                                <Tag type="magenta">{'Example tag'}</Tag>
                                <Tag type="red">{'Example'}</Tag>
                                <Tag type="cool-gray">{'Example tag 123'}</Tag>
                                <Tag type="blue">{'Examples'}</Tag>
                                <Tag type="magenta">{'Tag'}</Tag>
                                {/* {projectData.ProductType.split(",").map(typetag =>
                                    <Tag type="red" title="Clear Filter" key={projectData.ppid + typetag}>{typetag}</Tag>
                                )}
                                {projectData.Solutions.split(",").map(solutiontag =>
                                    <Tag type="magenta" title="Clear Filter" key={projectData.ppid + solutiontag}>{solutiontag}</Tag>
                                )}
                                {projectData.Vertical.split(",").map(verticaltag =>
                                    <Tag type="warm-gray" title="Clear Filter" key={projectData.ppid + verticaltag} >{verticaltag}</Tag>
                                )}
                                {projectData.Product.split(",").map(producttag =>
                                    <Tag type="cool-gray" title="Clear Filter" key={projectData.ppid + producttag}>{producttag}</Tag>
                                )} */}
                            </div>
                        </Tile>
                    </Column>
                </Grid>
            </Content>
        </>
    );
}

export default ProjectDetails;