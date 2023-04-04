import { Tag } from '@carbon/react';
import styles from './Card.module.scss';
import { Star } from '@carbon/icons-react';

import { CustomClickableTile, CustomLink } from './CustomCarbonNavigation';

//const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/";

export default function FeaturedCard({project}) {

	return (
		<CustomClickableTile className={styles.featuredTile} href={`./details/${project.id}`} >
			{/* <img src={CARD_IMG_URL + projectData.Image1Url} className='cardImage' /> */}
			<CustomLink size='lg' className={styles.titleLink}>{project.title}</CustomLink>
			<Tag type='red' className={styles.featuredTag} renderIcon={Star}>FEATURED PROJECT</Tag>
			<p className={styles.description}>{project.description}</p>
			<div className={styles.tags}>
				{project.tags.map(tagItem => 
					<Tag type='magenta' title='Clear Filter' style={{marginLeft: '0px', marginRight: '5px'}} key={tagItem.tagId}>{tagItem.tagName}</Tag>
				)}
			</div>
		</CustomClickableTile>
	);
}