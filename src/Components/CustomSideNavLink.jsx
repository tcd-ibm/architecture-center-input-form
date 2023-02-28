import { useNavigate } from 'react-router';
import { SideNavLink } from '@carbon/react';

function CustomSideNavLink(props) {
    const { href, children, ...remainingProps } = props;

    const navigate = useNavigate();

    return (
        <SideNavLink
            onClick={() => navigate(href)}
            style={{cursor: 'pointer'}}
            {...remainingProps}
        >
            {children}
        </SideNavLink>
    );
}

export default CustomSideNavLink;