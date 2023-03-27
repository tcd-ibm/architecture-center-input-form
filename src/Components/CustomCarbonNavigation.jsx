import { useNavigate } from 'react-router';
import { ClickableTile, HeaderGlobalAction, HeaderMenuItem, HeaderName, Link, SwitcherItem } from '@carbon/react';

function ComponentWrapper(props) {
    const { href, Component, children, ...remainingProps } = props;

    const navigate = useNavigate();

    return (
        <Component 
            onClick={() => navigate(href)}
            style={{cursor: 'pointer'}}
            {...remainingProps}
        >
            {children}
        </Component>
    );
}

export const CustomClickableTile = props => <ComponentWrapper Component={ClickableTile} {...props} />;
export const CustomHeaderGlobalAction = props => <ComponentWrapper Component={HeaderGlobalAction} {...props} />;
export const CustomHeaderMenuItem = props => <ComponentWrapper Component={HeaderMenuItem} {...props} />;
export const CustomHeaderName = props => <ComponentWrapper Component={HeaderName} {...props} />;
export const CustomLink = props => <ComponentWrapper Component={Link} {...props} />;
export const CustomSwitcherItem = props => <ComponentWrapper Component={SwitcherItem} {...props} />;