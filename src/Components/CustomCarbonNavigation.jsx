import { useNavigate } from 'react-router';
import { HeaderMenuItem } from '@carbon/react';

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

export const CustomHeaderMenuItem = props => <ComponentWrapper Component={HeaderMenuItem} {...props} />;