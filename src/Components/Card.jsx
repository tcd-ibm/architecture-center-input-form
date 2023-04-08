import { Tag } from '@carbon/react';
import styles from './Card.module.scss';

import { CustomClickableTile, CustomLink } from './CustomCarbonNavigation';

//const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/";

export default function Card({projectData}) {

	return (
		<CustomClickableTile className={styles.tile} href={`./details/${projectData.id}`} >
			{/* <img src={CARD_IMG_URL + projectData.Image1Url} className='cardImage' /> */}
			<img src={`http://localhost:5297/api/v1/project/${projectData.id}/image`} alt='Project' className={styles.cardImage}
                                onError={event => event.target.style.display = 'none'} />
			<CustomLink size='lg' className={styles.titleLink}>{projectData.title}</CustomLink>
			<p className={styles.description}>{projectData.description}</p>
			<div className={styles.tags}>
				{projectData.tags.map(tagItem => 
					<Tag type='magenta' title='Clear Filter' style={{marginLeft: '0px', marginRight: '5px'}} key={tagItem.tagId}>{tagItem.tagName}</Tag>
				)}
			</div>
		</CustomClickableTile>
	);
}