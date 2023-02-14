import { Tile, Link, Tag } from '@carbon/react';
import './card.scss';

const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/";

export default function Card({projectData}) {

  if(!projectData.islive) return null;
  
  return (
    <Tile className='tile'>
      {/* <img src={CARD_IMG_URL + projectData.Image1Url} className='cardImage' /> */}
      <Link size='lg' className='titleLink'>{projectData.Heading}</Link>
      <p>{projectData.Summary}</p>
      <div className='tags'>
        { projectData.ProductType.split(",").map(typetag =>
            <Tag type="red" title="Clear Filter" key={projectData.ppid + typetag}>{typetag}</Tag>
        )}
        { projectData.Solutions.split(",").map(solutiontag =>
            <Tag type="magenta" title="Clear Filter" key={projectData.ppid + solutiontag}>{solutiontag}</Tag>
        )}
        { projectData.Vertical.split(",").map(verticaltag =>
            <Tag type="warm-gray" title="Clear Filter" key={projectData.ppid + verticaltag} >{verticaltag}</Tag>
        )}
        { projectData.Product.split(",").map(producttag =>
            <Tag type="cool-gray" title="Clear Filter" key={projectData.ppid + producttag}>{producttag}</Tag>
        )}
      </div>
    </Tile>
  );
}