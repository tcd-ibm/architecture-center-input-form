import renderer from 'react-test-renderer';

import ProjectQuerySidePanel from '../../Components/ProjectQuerySidePanel';

describe('ProjectQuerySidePanel', () => {
    it('renders an Accordion with categories and tags', () => {
        const menuContent = [
            {
                title: 'Category 1',
                tags: [
                    {id: 'tag1-1', name: 'Tag 1-1 name'},
                    {id: 'tag1-2', name: 'Tag 1-2 name'}
                ]
            },
            {
                title: 'Category 2',
                tags: [
                    {id: 'tag2-1', name: 'Tag 2-1 name'},
                    {id: 'tag2-2', name: 'Tag 2-2 name'},
                    {id: 'tag2-3', name: 'Tag 2-3 name'}
                ]
            }
        ];

        const component = renderer.create(
            <ProjectQuerySidePanel menuContent={menuContent} filterTagList={[]} handleFilterChange={() => {}} />
        );

        let tree = component.toJSON();
        expect(tree).toMatchSnapshot();
    });
});