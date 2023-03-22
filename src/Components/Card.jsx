import { useNavigate } from 'react-router';
import { ClickableTile, Link, Tag } from '@carbon/react';
import styles from './Card.module.scss';

//const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/";

export default function Card({projectData}) {
  const navigate = useNavigate();

  return (
    <ClickableTile className={styles.tile} onClick={() => navigate(`./details/${projectData.id}`)} >
      {/* <img src={CARD_IMG_URL + projectData.Image1Url} className='cardImage' /> */}
      <Link size='lg' className={styles.titleLink}>{projectData.title}</Link>
      <p>{projectData.description}</p>
      <div className={styles.tags}>
        {projectData.tags.map(tagItem => 
          <Tag type='magenta' title='Clear Filter' key={tagItem.tagId}>{tagItem.tagName}</Tag>
        )}
      </div>
    </ClickableTile>
  );
}