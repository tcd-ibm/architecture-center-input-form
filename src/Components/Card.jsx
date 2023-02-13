import { Tag } from '@carbon/react';
import './card.scss';

const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/";

export default function Card({projectData}) {

  if(!projectData.islive) return null;
  
  return (
    <div className='card'>
      <img src={CARD_IMG_URL + projectData.Image1Url} className='cardImage' />
      <h4 className='cardHeader'>{projectData.Heading}</h4>
      <div className='cardContent'>{projectData.Summary}</div>

      {
        projectData.ProductType.split(",").map(typetag =>
          <Tag type="red" title="Clear Filter" key={projectData.ppid + typetag}></Tag>
        )}
      {
        projectData.Solutions.split(",").map(solutiontag =>
          <Tag type="magenta" title="Clear Filter" key={projectData.ppid + solutiontag}>{solutiontag}</Tag>
        )}
      {
        projectData.Vertical.split(",").map(verticaltag =>
          <Tag type="warm-gray" title="Clear Filter" key={projectData.ppid + verticaltag} >{verticaltag}</Tag>
        )}
      {
        projectData.Product.split(",").map(producttag =>
          <Tag type="cool-gray" title="Clear Filter" key={projectData.ppid + producttag}>{producttag}</Tag>
        )}

    </div>
  );
}